from context_search.preprocessor import Preprocessor
from context_search.data_classes import Chunk


def test_produce_chunks():
    pipeline = Preprocessor()
    texts = ['This is a test text']
    chunks = pipeline.splitter.produce_chunks(texts)

    assert len(chunks) == 1
    assert isinstance(chunks[0], Chunk)
