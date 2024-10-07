
import pytest
import os
from data_manager.preprocessor.text_splitter import TextSplitter

cwd = os.getcwd()
test_text = ""
with open(f"{cwd}/test/unit_tests/data_manager_test/test_data/text/ml_article_text.txt", "r") as f:
    test_text = f.read()


def test_text_splitter_correct_overlap_margin():
    splitter = TextSplitter()
    chunk_size = 100
    overlap = 10
    margin = 10

    splits = splitter.split(test_text, chunk_size, overlap, margin)
    assert len(splits) == 74
    assert [len(split) for split in splits] ==\
        [
            42, 83, 85, 89, 82, 83, 84, 88, 84, 86, 80, 90, 89, 85,
            82, 85, 84, 87, 89, 89, 83, 89, 81, 86, 88, 90, 82, 82,
            82, 84, 87, 87, 86, 84, 89, 86, 87, 80, 81, 86, 89, 81,
            89, 84, 82, 85, 88, 85, 85, 88, 89, 80, 90, 87, 80, 88,
            84, 87, 84, 82, 87, 83, 83, 89, 88, 87, 87, 89, 85, 80, 90
        ]


def test_text_splitter_correct_overlap():
    splitter = TextSplitter()
    chunk_size = 100
    overlap = 10
    margin = None

    splits = splitter.split(test_text, chunk_size, overlap, margin)


def test_text_splitter_correct():
    splitter = TextSplitter()
    chunk_size = 100
    overlap = None
    margin = None

    splits = splitter.split(test_text, chunk_size, overlap, margin)


def test_text_splitter_incorrect():
    splitter = TextSplitter()
    chunk_size = 0
    overlap = 10
    margin = 10

    with pytest.raises(ValueError):
        splitter.split(test_text, chunk_size, overlap, margin)


if __name__ == "__main__":
    test_text_splitter_correct()
