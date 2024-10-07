import inspect
import re

from abc import ABC, abstractmethod
from ..data_classes import Chunk
from typing import Union, List
from re import Pattern


class AbstractSplitter(ABC):
    """ The abstract class for text splitters. """
    @abstractmethod
    def split(self):
        pass


class TextSplitter(AbstractSplitter):
    """ The dynamic text splitter for dividing text into chunks with
    margin windows.

    <b>Important:</b>
        1) The order of the separators is important for the "sequential" and
        "backward" order. The first separator in the list will be the first
        separator to be checked for in the text. The algorithm will early
        stop when finds the first occurence of the separator.

        2) When initiziled, the class is optimized for the given separators.
        If the separators are changed, the class should be reinitizalized or
        the setup_separators method should be called.

        3) We advise to use a proposed sizes of the chunk size, overlap and
        margin. Refer to the R&D in documentation where experimentation was
        performed.

        4) The results are currently in reverse order.

    Parameters:
        chunk_size: [int | float]
            Requested size of the chunk.
        overlap: int
            The overlap between the chunks
        order: str ["any", "sequntial", "backward"]
            The search strategy for the separators
        separators: List[str]
            List of separators to be used for splitting the text
        is_separator_regex: bool
            If the provided separators are regex or not

    """
    def __init__(
            self,
            chunk_size: int = 1024,
            chunk_overlap: Union[int, float] = 256,
            margin: int = 256,
            order: str = "any",
            separators: List[str] = ['\.', '\n\n', '\n', '\s'],
            is_separator_regex: bool = True,
    ):
        self.chunk_size = chunk_size
        self.overlap = chunk_overlap
        self.margin = margin
        self.order = order
        self._is_separator_regex = is_separator_regex
        self.separators = separators

        if any(property is None for property in self.__dict__.values()):
            raise ValueError(
                "All properties must be set to a value."
            )

        if isinstance(chunk_overlap, float):
            chunk_overlap = int(chunk_overlap * chunk_size)

        if chunk_size <= 0:
            raise ValueError(
                f"Chunk size {chunk_size} must be greater than 0."
            )

        if 0 > chunk_overlap or chunk_overlap >= chunk_size:
            raise ValueError(
                f"Overlap size {chunk_overlap} is greater than the chunk size"
                f" {chunk_size}."
            )

        if 0 > margin or margin > chunk_overlap:
            raise ValueError(
                f"Margin size {margin} is greater than the chunk size"
                f" {chunk_overlap}."
            )

        self.separator_pattern: Union[Pattern, List[Pattern], None] = None
        self.search_func: callable = None
        self.setup_separators(separators)

    def setup_separators(self, separators):
        """ Prepares compiled patterns for efficient search of the separators
        and sets the search function based on the order of the separators.
        """
        match self.order.lower():
            case "any":
                if not self._is_separator_regex:
                    separators = '|'.join([
                        re.escape(separator) for separator in separators
                    ])
                else:
                    separators = '|'.join(separators)
                self.separator_pattern = re.compile(separators)
                self.search_func = self.search_re
            case "sequential":
                if not self._is_separator_regex:
                    self.separator_pattern = [
                        re.compile(re.escape(separator))
                        for separator in separators
                    ]
                else:
                    self.separator_pattern = [
                        re.compile(separator)
                        for separator in separators
                    ]
                self.search_func = self.search_re_list
            case "backward":
                if not self._is_separator_regex:
                    self.separator_pattern = [
                        re.compile(re.escape(separator))
                        for separator in reversed(separators)
                    ]
                else:
                    self.separator_pattern = [
                        re.compile(separator)
                        for separator in reversed(separators)
                    ]
                self.search_func = self.search_re_list
            case _:
                raise ValueError(
                    f"Choosen invalid order: {self.order}"
                    "Choose from: ['any', 'sequential', 'backward']"
                )

    def search_re(self, pattern, string):
        return pattern.search(string)

    def search_re_list(self, pattern, string):
        for p in pattern:
            result = p.search(string)
            if not isinstance(result, type(None)):
                return result
        return None

    def split(self, text):
        """ Splits text into chunks dynamically

        Algorithm:

        0'th iteration:

        1. Calculate the maximum chunk size
            The difference between the chunk size and the overlap
            that assures that the final chunk will not exceed but
            be as high as possible. (We want final chunk sizes as
            close to the chunk size as possible)

        2. Get text length
            The algorithms operates on the text length as the indexing
            medium insted of operating on the text itself. This allows
            us to increase performance by not having to slice the text.

        3. Calculate the starting split position (see _start_split_position)
        4. Creation of the last chunk (we are chunking in reverse)
        5. Update the remaining text length


        The loop:
            While the remaining text length is greater than the maximum chunk
            size~

        1. Calculate the starting split position (see _start_split_position)
        2. Calculate the ending split position (see _end_split_position)
        3. Append the chunk to the chunks with the calculated positions
        4. Update the remaining text length

        The finale:
        1. Append the first chunk to the chunks from last starting split
            positionto the beginning of the text.

        2. Return the chunks in reverse order

        """
        max_chunk_size = self.chunk_size - self.overlap
        remaining_text_length = len(text)

        static_split_position = len(text) - self.chunk_size
        new_start_pos = self._split_pos(
            text[static_split_position:static_split_position+self.margin],
            static_split_position
        )
        split_positions = [text[new_start_pos:remaining_text_length]]

        while new_start_pos > max_chunk_size:
            static_split_position += self.overlap
            new_end_position = self._split_neg(
                text[static_split_position-self.margin:static_split_position],
                static_split_position
            )

            static_split_position -= self.chunk_size
            new_start_pos = self._split_pos(
                text[static_split_position:static_split_position+self.margin],
                static_split_position
            )
            split_positions.append(text[new_start_pos:new_end_position])

        if new_start_pos < 0:
            return split_positions

        static_split_position += self.overlap
        new_end_position = self._split_neg(
            text[static_split_position-self.margin:static_split_position],
            static_split_position
        )
        split_positions.append(text[0:new_end_position])

        return split_positions

    def _split_pos(self, string, current_position):
        offset = self.search_func(self.separator_pattern, string)
        if offset is None:
            return current_position

        return current_position + offset.end()

    def _split_neg(self, string, current_position):
        inverted_string = string[::-1]
        offset = self.search_func(self.separator_pattern, inverted_string)
        if offset is None:
            return current_position

        return current_position - offset.start()

    def produce_chunks(self, text: List[str]) -> List[Chunk]:
        """ Produces chunks from the given pages of text. """
        chunk_dtos = []

        for i, page in enumerate(text):
            chunks = self.split(page)
            for chunk in chunks:
                chunk_dtos.append(Chunk(text=chunk, page_number=i))

        return chunk_dtos
