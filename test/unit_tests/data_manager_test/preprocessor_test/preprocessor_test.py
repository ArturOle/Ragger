from ragger.data_manager.preprocessor import Preprocessor
from ragger.data_manager.data_classes import LiteratureDTO, Chunk

import pytest


def test_produce_chunks(mocker):
    pipeline = Preprocessor()
    splitter_mock = mocker.patch('ragger.data_manager.preprocessor.RecursiveCharacterTextSplitter')
    splitter_mock.return_value.split_text.return_value = ['This is a test text']
    texts = ['This is a test text']
    chunks = pipeline.produce_chunks(texts)

    assert len(chunks) == 1
    assert isinstance(chunks[0], Chunk)
