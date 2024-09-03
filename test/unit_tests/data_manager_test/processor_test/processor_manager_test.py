from data_manager.processor.processor import ProcessorManager
from data_manager.data_classes import LiteratureDTO, LiteratureGraph
from typing import List

import pytest
import numpy as np
import random


def test_multiple_file_processing():
    literatures = [
        LiteratureDTO(
            filename='test1.txt',
            filepath='test1.txt',
            text=['This is a test text']
        ),
        LiteratureDTO(
            filename='test2.txt',
            filepath='test2.txt',
            text=['This is a test text']
        ),
        LiteratureDTO(
            filename='test3.txt',
            filepath='test3.txt',
            text=['This is a test text']
        )
    ]
    processor_manager = ProcessorManager()
    literatures = processor_manager.process(literatures)

    for i, literature in enumerate(literatures):
        assert literature.literature.filename == f'test{i + 1}.txt'
        assert literature.literature.filepath == f'test{i + 1}.txt'

    assert len(literatures) == 3


if __name__ == '__main__':
    test_multiple_file_processing()
