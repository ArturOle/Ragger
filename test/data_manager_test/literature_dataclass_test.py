
import pytest
from ragger.data_manager.reader import Literature
from pydantic import ValidationError


def test_literature_creation_correct():
    literature = Literature(
        filename='filename',
        text='Test text',
        text_position=0,
        page_number=0,
        keywords=['Test', 'keyword'],
        embeddings=[1, 2]
    )

    assert literature.filename == 'filename'
    assert literature.text == 'Test text'
    assert literature.text_position == 0
    assert literature.page_number == 0
    assert literature.keywords == ['Test', 'keyword']
    assert literature.embeddings == [1, 2]


def test_literature_creation_incorrect():
    with pytest.raises(ValidationError):
        Literature(
            filename='filename',
            text=['Test text'],   # Should be a string
            text_position=0,
            page_number=0,
            keywords=['Test', 'keyword'],
            embeddings=[1, 2]
        )
