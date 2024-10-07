
import re

from abc import ABC, abstractmethod
from functools import singledispatchmethod
from typing import List


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
    """ The text splitter for dividing text into chunks """
    white_space_pattern = re.compile('\s')

    @staticmethod
    def splits(text_length, chunk_size):
        raise NotImplementedError

    @singledispatchmethod
    def _split_dispatcher(self, overlap, text, chunk_size, margin):
        raise ValueError(f"Invalid overlap type: {type(overlap)}")

    @_split_dispatcher.register
    def _(self, overlap: None, text, chunk_size, margin):
        return self.splits(len(text), chunk_size)

    @_split_dispatcher.register
    def _(self, overlap: float, text, chunk_size, margin):
        """ Split text into chunks with overlap as a percentage """
        assert 0 < overlap < 1
        text_length = len(text)
        return self._split_dispatcher(
            int(text_length * overlap),
            text,
            chunk_size,
            margin
        )

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
        1. Append the first chunk to the chunks from last starting split position
            to the beginning of the text.
        2. Return the chunks in reverse order

        """
        max_chunk_size = chunk_size - overlap
        remaining_text_length = len(text)

        start_split_position = self._start_split_position(
            text, margin, remaining_text_length, max_chunk_size
        )
        chunks = [text[start_split_position:remaining_text_length]]
        remaining_text_length = remaining_text_length -\
            (remaining_text_length-start_split_position)

        while True:
            start_split_position = self._start_split_position(
                text, margin, remaining_text_length, max_chunk_size
            )
            end_split_position = self._end_split_position(
                text, margin, remaining_text_length
            )
            chunks.append(
                text[start_split_position:end_split_position]
            )
            remaining_text_length = remaining_text_length -\
                (remaining_text_length-start_split_position)

            if remaining_text_length < max_chunk_size:
                break

        # Here should be correction for new end split position
        chunks.append(text[0:remaining_text_length+overlap])

        return chunks[::-1]

    def _start_split_position(
            self, text, margin, remaining_text_length, max_chunk_size
    ):
        """ Searches for the best left-hand (starting) position for split """
        static_split_pos = remaining_text_length - max_chunk_size
        positive_margin_subset = text[static_split_pos:static_split_pos+margin]
        return self.split_pos(positive_margin_subset, static_split_pos)

    def _end_split_position(
            self, text, margin, remaining_text_length
    ):
        """ Searches for the best right-hand (ending) position for split """
        negative_margin_subset = text[
                remaining_text_length-margin:remaining_text_length
            ]
        return self.split_neg(
            negative_margin_subset,
            remaining_text_length
        )

    def split_pos(self, string, current_position):
        for i, letter in enumerate(string):
            if letter == '.':
                return current_position + i + 1

        for i, letter in enumerate(string):
            if not isinstance(
                self.white_space_pattern.match(letter),
                type(None)
            ):
                return current_position + i + 1

        return current_position

    def split_neg(self, string, current_position):
        inv_string = string[::-1]
        for i, letter in enumerate(inv_string):
            if letter == '.':
                return current_position - i

        for i, letter in enumerate(inv_string):
            if not isinstance(
                self.white_space_pattern.match(letter),
                type(None)
            ):
                return current_position - i

        return current_position

    def split(
            self,
            text,
            chunk_size=100,
            overlap: None = None,
            margin: int = 10
    ) -> List[str]:
        if chunk_size < 1:
            raise ValueError("Chunk size must be greater than 0")

        return self._split_dispatcher(overlap, text, chunk_size, margin)

    def _overlap_splits(self, text_length, chunk_size, overlap, margin=None):
        return self._overlap_splits_dispatcher(
            margin, overlap, text_length, chunk_size
        )
