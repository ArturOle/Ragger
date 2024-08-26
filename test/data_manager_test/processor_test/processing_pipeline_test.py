
from ragger.data_manager.processor.processor import ProcessingPipeline
from ragger.data_manager.data_classes import Literature
import numpy as np
import random
import pytest

random.seed(0)
np.random.seed(0)


def test_processing_pipeline():
    pipeline = ProcessingPipeline()
    texts = Literature(
        filename="name",
        text="This is a test text.",
        text_position=0,
        page_number=0
    )

    literature = pipeline.process(texts)
    literature.embeddings = literature.embeddings[:2]

    assert literature.keywords == [['a test text', 0.25], ['This', 0.0]]
    assert literature.embeddings == pytest.approx([-0.18107341, -0.24594933], 0.1e-6)
