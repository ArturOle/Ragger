
from ragger.data_manager.preprocessor import Preprocessor
from ragger.data_manager.data_classes import LiteratureDTO
import numpy as np
import random
import pytest

random.seed(0)
np.random.seed(0)


def test_processing_pipeline():
    pipeline = Preprocessor()
    texts = LiteratureDTO(
        filename="name",
        text="This is a test text."
    )

    literature = pipeline.process(texts)[0]
    assert literature.literature.filename == "name"
    assert literature.literature.filepath == "path"
    assert len(literature.chunks) == 1
    assert literature.chunks[0].text == "This is a test text"
    assert literature.chunks[0].page_number == 0
    assert len(literature.tags) == 2
    assert literature.tags[0].text == "a test text"
    assert pytest.approx(literature.tags[0].embeddings[:2], 1e-3) ==\
        [-0.23820725, -0.3175099]
    assert literature.relation_weights[0].literature == "name"
    assert literature.relation_weights[0].tag == "a test text"
    assert literature.relation_weights[0].weight == 0.25
