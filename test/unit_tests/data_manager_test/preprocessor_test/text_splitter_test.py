
import pytest
import os
from ragger.data_manager.preprocessor.text_splitter import TextSplitter

cwd = os.getcwd()
test_text = ""
with open(f"{cwd}/test/unit_tests/data_manager_test/test_data/text/ml_article_text.txt", "r") as f:
    test_text = f.read()


def test_text_splitter_correct_overlap_margin():
    chunk_size = 100
    overlap = 10
    margin = 10
    splitter = TextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        margin=margin
    )

    splits = splitter.split(test_text)
    assert len(splits) == 67
    assert [len(split) for split in splits] ==\
        [
            99, 98, 96, 92, 88, 96, 90, 99, 92, 88, 95, 88, 92, 97, 94, 93, 88,
            96, 91, 97, 98, 94, 91, 95, 83, 93, 93, 89, 92, 94, 97, 91, 99, 93,
            89, 92, 94, 89, 95, 94, 91, 91, 90, 96, 92, 99, 94, 93, 94, 90, 93,
            92, 97, 95, 94, 97, 100, 90, 97, 90, 91, 91, 89, 96, 100, 92, 74
        ]

    chunk_size = 100
    overlap = 10
    margin = 10
    splitter = TextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        margin=margin,
        order="sequential"
    )

    splits = splitter.split(test_text)
    assert len(splits) == 67
    assert [len(split) for split in splits] ==\
        [
            99, 98, 92, 91, 88, 96, 90, 99, 92, 88, 95, 88, 92, 97, 94, 93, 88,
            96, 91, 97, 98, 94, 91, 95, 83, 93, 93, 89, 92, 94, 97, 91, 99, 93,
            84, 92, 94, 87, 94, 94, 91, 91, 85, 96, 83, 90, 94, 93, 94, 90, 93,
            92, 97, 95, 94, 97, 100, 90, 97, 90, 87, 91, 89, 96, 100, 92, 74
        ]

    chunk_size = 100
    overlap = 10
    margin = 10
    splitter = TextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        margin=margin,
        order="backward"
    )

    splits = splitter.split(test_text)
    assert len(splits) == 67
    assert [len(split) for split in splits] ==\
        [
            99, 98, 96, 92, 88, 96, 90, 99, 92, 88, 95, 88, 92, 97, 94, 93, 88,
            96, 91, 97, 98, 94, 91, 95, 83, 93, 93, 89, 92, 94, 97, 91, 99, 93,
            89, 87, 94, 89, 95, 94, 91, 90, 90, 96, 92, 90, 85, 93, 94, 90, 93,
            92, 97, 95, 94, 97, 100, 90, 97, 90, 91, 91, 89, 96, 100, 92, 74
        ]


def test_text_splitter_incorrect_margin_none():
    chunk_size = 100
    overlap = 10
    margin = None

    with pytest.raises(ValueError):
        TextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            margin=margin
        )


def test_text_splitter_incorrect_overlap_none():
    chunk_size = 100
    overlap = None
    margin = 10

    with pytest.raises(ValueError):
        TextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            margin=margin
        )


def test_text_splitter_incorrect_margin_out_of_range():
    chunk_size = 100
    overlap = 10
    margin = None

    with pytest.raises(ValueError):
        TextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            margin=margin
        )


def test_text_splitter_incorrect_overlap_out_of_range():
    chunk_size = 100
    overlap = -10
    margin = 10

    with pytest.raises(ValueError):
        TextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            margin=margin
        )

    chunk_size = 100
    overlap = 1e-120
    margin = 10

    with pytest.raises(ValueError):
        TextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            margin=margin
        )

    chunk_size = 100
    overlap = 1.1
    margin = 10

    with pytest.raises(ValueError):
        TextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            margin=margin
        )


def test_text_splitter_incorrect():
    chunk_size = 0
    overlap = 10
    margin = 10

    with pytest.raises(ValueError):
        TextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=overlap,
            margin=margin
        )

if __name__ == "__main__":
    test_text_splitter_incorrect_overlap_out_of_range()
