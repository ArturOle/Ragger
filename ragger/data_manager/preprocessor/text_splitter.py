from functools import singledispatchmethod
import re

from abc import ABC, abstractmethod


class AbstractSplitter(ABC):
    """ This is how DRY dies, with thunderous applaus of abstract OOP """
    @abstractmethod
    def split(self, data, chunk_size, overlap, margin):
        pass

    @singledispatchmethod
    @abstractmethod
    def _overlap_splits_dispatcher(self, overlap, data_size, chunk_size):
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

    @staticmethod
    def _overlap_splits(text_length, chunk_size, overlap):
        raise NotImplementedError

    @singledispatchmethod
    def _split_dispatcher(self, overlap, text, chunk_size, margin):
        raise ValueError(f"Invalid overlap type: {type(overlap)}")

    @singledispatchmethod
    def _overlap_splits_dispatcher(
            self, margin, overlap, data_size, chunk_size
    ):
        raise ValueError(f"Invalid overlap type: {type(margin)}")

    @_overlap_splits_dispatcher.register
    def _(self, margin: None, overlap: int, data_size, chunk_size):
        raise NotImplementedError

    @_overlap_splits_dispatcher.register
    def _(self, margin: int, overlap: int, data_size, chunk_size):
        raise NotImplementedError

    # TODO: Task: Break this down into smaller functions
    # Description: The split function is too long and should be broken down
    # into smaller, more manageable functions. This will iprove readablity and
    # maintainability of the code. Tags: refactor

    @_split_dispatcher.register
    def _(self, overlap: int, text, chunk_size, margin):
        max_chunk_size = chunk_size - overlap
        remaining_text_length = len(text)

        static_split_pos = remaining_text_length - max_chunk_size
        positive_margin_subset = text[static_split_pos:static_split_pos+margin]
        new_pos = self.split_pos(positive_margin_subset, static_split_pos)
        split_positions = [text[new_pos:remaining_text_length]]
        remaining_text_length = remaining_text_length -\
            (remaining_text_length-new_pos)
        while True:
            static_split_pos = remaining_text_length - max_chunk_size
            negative_margin_subset = text[
                remaining_text_length-margin:remaining_text_length
            ]
            new_neg_pos = self.split_neg(
                negative_margin_subset,
                remaining_text_length
            )

            positive_margin_subset = text[
                static_split_pos:static_split_pos+margin
            ]
            new_pos = self.split_pos(positive_margin_subset, static_split_pos)
            split_positions.append(text[new_pos:new_neg_pos])
            remaining_text_length = remaining_text_length -\
                (remaining_text_length-new_pos)

            if remaining_text_length < max_chunk_size:
                break

        split_positions.append(text[0:remaining_text_length+overlap])

        return split_positions

    @_split_dispatcher.register
    def _(self, overlap: None, text, chunk_size, margin):
        raise NotImplementedError

    @_split_dispatcher.register
    def _(self, overlap: float, text, chunk_size, margin):
        raise NotImplementedError

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
    ):
        return self._split_dispatcher(overlap, text, chunk_size, margin)

    def overlap_splits(self, text_length, chunk_size, overlap, margin=None):
        return self._overlap_splits_dispatcher(
            margin, overlap, text_length, chunk_size
        )
