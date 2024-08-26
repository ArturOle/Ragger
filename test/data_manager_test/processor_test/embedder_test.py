from ragger.data_manager.processor.embedder import Embedder

import numpy as np
import random


random.seed(0)
np.random.seed(0)

text_to_embed = "This is a test text. This is a test text. This is a test text."


def test_creating_embeddings_from_text():
    embedder = Embedder()
    embedding = embedder.embed(text_to_embed)

    assert np.array_equal(
        embedding,
        np.load("test/data_manager_test/processor_test/test_embedding.npy")
    )
