from data_manager.processor.processor import ProcessorManager
from data_manager.data_classes import Literature
import pytest

import numpy as np
import random

random.seed(0)
np.random.seed(0)


def test_multiple_file_processing():
    literatures = [
        Literature(
            filename="test1",
            text="This is a test text 1.",
            text_position=0,
            page_number=0
        ),
        Literature(
            filename="test2",
            text="This is a test text 2.",
            text_position=0,
            page_number=0
        ),
        Literature(
            filename="test3",
            text="This is a test text 3.",
            text_position=0,
            page_number=0
        )
    ]
    processor_manager = ProcessorManager()
    literatures = processor_manager.process(literatures)

    for i, literature in enumerate(literatures):
        assert literature.keywords == [
            ['a test text', 0.25],
            [str(i+1), 0.0],
            ['This', 0.0]
        ]

    assert literatures[0].embeddings[:2] == pytest.approx(
        [-0.1336354, -0.20415184],
        0.1e-6
    )
