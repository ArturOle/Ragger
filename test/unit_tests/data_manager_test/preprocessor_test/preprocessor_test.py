from ragger.data_manager.preprocessor import Preprocessor
from ragger.data_manager.data_classes import Chunk

import pytest


def test_produce_chunks():
    pipeline = Preprocessor()
    texts = ['This is a test text']
    chunks = pipeline.splitter.produce_chunks(texts)

    assert len(chunks) == 1
    assert isinstance(chunks[0], Chunk)
