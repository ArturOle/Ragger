import numpy as np
from functools import singledispatchmethod
from copy import copy
import re

from abc import ABC, abstractmethod


def find_end_of_sentence(text, start):
    end = start
    while end < len(text) and text[end] not in '.!?':
        end += 1
    return end


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
    white_space_pattern = re.compile('\s')

    @staticmethod
    def splits(text_length, chunk_size):
        return np.arange(chunk_size, text_length-chunk_size+1, chunk_size)

    @staticmethod
    def _overlap_splits(text_length, chunk_size, overlap):
        return np.arange(chunk_size, text_length-chunk_size+1, chunk_size-overlap)

    @singledispatchmethod
    def _split_dispatcher(self, overlap, text, chunk_size, margin):
        raise ValueError(f"Invalid overlap type: {type(overlap)}")

    @singledispatchmethod
    def _overlap_splits_dispatcher(self, margin, overlap, data_size, chunk_size):
        raise ValueError(f"Invalid overlap type: {type(margin)}")

    @_overlap_splits_dispatcher.register
    def _(self, margin: None, overlap: int, data_size, chunk_size):
        return TextSplitter.overlap_splits(data_size, chunk_size, overlap)

    @_overlap_splits_dispatcher.register
    def _(self, margin: int, overlap: int, data_size, chunk_size):
        overlaps = []

    @_split_dispatcher.register
    def _(self, overlap: int, text, chunk_size, margin):
        max_chunk_size = chunk_size - overlap
        remaining_text = copy(text)
        split_positions = []
        text_length = len(remaining_text)
        static_split_pos = text_length - max_chunk_size
        positive_margin_subset = text[static_split_pos:static_split_pos+margin]
        new_pos = self.split_pos(positive_margin_subset, static_split_pos)
        split_positions.insert(0, (new_pos, len(remaining_text)))
        remaining_text = remaining_text[:new_pos]
        while True:
            text_length = len(remaining_text)
            static_split_pos = text_length - max_chunk_size
            positive_margin_subset = text[static_split_pos:static_split_pos+margin]
            new_pos = self.split_pos(positive_margin_subset, static_split_pos)
            split_positions.insert(0, (new_pos, len(remaining_text)+overlap))
            remaining_text = remaining_text[:new_pos]

            if len(remaining_text) < max_chunk_size:
                break

        split_positions.insert(0, (0, len(remaining_text)+overlap))

        return {key:text[i:j] for key, (i, j) in enumerate(split_positions)}

    @_split_dispatcher.register
    def _(self, overlap: None, text, chunk_size, margin):
        split_pos = self.splits(len(text), chunk_size)
        split_pos = np.insert(split_pos, 0, 0)
        return {key:text[i:i+chunk_size] for key, i in enumerate(split_pos)}

    @_split_dispatcher.register
    def _(self, overlap: float, text, chunk_size, margin):
        return self.overlap_splits(len(text), chunk_size, int(chunk_size*overlap))

    def split_pos(self, string, current_position):
        for i, letter in enumerate(string):
            if letter == '.':
                return current_position + i + 1

        for i, letter in enumerate(string):
            if not isinstance(self.white_space_pattern.match(letter), type(None)):
                return current_position + i + 1

        return current_position


    def split_neg(self, string, current_position):
        inv_string = string[::-1]
        for i, letter in enumerate(inv_string):
            if letter == '.':
                return current_position + (len(string)-i)

        for i, letter in enumerate(inv_string):
            if not isinstance(self.white_space_pattern.match(letter), type(None)):
                return current_position + (len(string)-i)

        return current_position

    def split(self, text, chunk_size=100, overlap: None = None, margin: int = 10):
        return self._split_dispatcher(overlap, text, chunk_size, margin)

    def overlap_splits(self, text_length, chunk_size, overlap, margin=None):
        return self._overlap_splits_dispatcher(margin, overlap, text_length, chunk_size)
