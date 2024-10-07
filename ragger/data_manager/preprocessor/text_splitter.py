
import re

from abc import ABC, abstractmethod
from functools import singledispatchmethod
from typing import Union, List
from re import Pattern


class AbstractSplitter(ABC):
    """ This is how DRY dies, with thunderous applaus of abstract OOP """
    @abstractmethod
    def split(self, data, chunk_size, overlap, margin):
        pass

    @singledispatchmethod
    @abstractmethod
    def _split_dispatcher(self, overlap, data, chunk_size, margin):
        pass


class TextSplitter(AbstractSplitter):
    """ The text splitter for dividing text into chunks
    order: str ["any", "sequntial", "backward"]
    """
    def __init__(
            self,
            order: str = "any",
            separators: List[str] = ['\.', '\n\n', '\n', '\s'],
            is_separator_regex: bool = True
    ):
        self.order = order
        self._is_separator_regex = is_separator_regex
        self.separator_pattern: Union[Pattern, List[Pattern], None] = None
        self.search_func: callable = None
        self.setup_separators(separators)

    def setup_separators(self, separators):
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
                raise ValueError(f"Invalid order: {self.order}")

    def search_re(self, pattern, string):
        return pattern.search(string)

    def search_re_list(self, pattern, string):
        for p in pattern:
            result = p.search(string)
            if not isinstance(result, type(None)):
                return result
        return None

    @staticmethod
    def splits(text_length, chunk_size):
        raise NotImplementedError

    @staticmethod
    def _overlap_splits(text_length, chunk_size, overlap):
        raise NotImplementedError

    @singledispatchmethod
    def _split_dispatcher(self, overlap, text, chunk_size, margin):
        raise ValueError(f"Invalid overlap type: {type(overlap)}")

    @_split_dispatcher.register
    def _(self, overlap: int, text, chunk_size, margin):
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
        While the remaining text length is greater than the maximum chunk size~
        1. Calculate the starting split position (see _start_split_position)
        2. Calculate the ending split position (see _end_split_position)
        3. Append the chunk to the chunks with the calculated positions
        4. Update the remaining text length

        The finale:
        1. Append the first chunk to the chunks from last starting split
            positionto the beginning of the text.

        2. Return the chunks in reverse order

        """
        max_chunk_size = chunk_size - overlap
        remaining_text_length = len(text)

        static_split_pos = len(text) - chunk_size
        new_pos = self.split_pos(
            text[static_split_pos:static_split_pos+margin],
            static_split_pos
        )
        split_positions = [text[new_pos:remaining_text_length]]

        while True:
            static_split_pos += overlap
            new_neg_pos = self.split_neg(
                text[static_split_pos-margin:static_split_pos],
                static_split_pos
            )

            static_split_pos -= chunk_size
            new_pos = self.split_pos(
                text[static_split_pos:static_split_pos+margin],
                static_split_pos
            )
            split_positions.append(text[new_pos:new_neg_pos])

            if new_pos < max_chunk_size:
                break

        static_split_pos += overlap
        new_neg_pos = self.split_neg(
            text[static_split_pos-margin:static_split_pos],
            static_split_pos
        )
        split_positions.append(text[0:new_neg_pos])

        return split_positions

    @_split_dispatcher.register
    def _(self, overlap: None, text, chunk_size, margin):
        raise NotImplementedError

    @_split_dispatcher.register
    def _(self, overlap: float, text, chunk_size, margin):
        raise NotImplementedError

    def split_pos(self, string, current_position):
        offset = self.search_func(self.separator_pattern, string)
        if offset is None:
            return current_position

        return current_position + offset.end()

    def split_neg(self, string, current_position):
        inverted_string = string[::-1]
        offset = self.search_func(self.separator_pattern, inverted_string)
        if offset is None:
            return current_position

        return current_position - offset.start()

    def split(
            self,
            text,
            chunk_size=100,
            overlap: None = None,
            margin: int = 10
    ):
        return self._split_dispatcher(overlap, text, chunk_size, margin)

    def overlap_splits(self, text_length, chunk_size, overlap, margin=None):
        return self._overlap_splits_dispatcher(
            margin, overlap, text_length, chunk_size
        )
