
import pytest
from ragger.data_manager.reader import Literature
from pydantic import ValidationError


def test_literature_creation_correct():
    literature = Literature(
        title='Test title',
        authors=['Test author'],
        summary='Test summary',
        text='Test text'
    )

    assert literature.title == 'Test title'
    assert literature.authors == ['Test author']
    assert literature.summary == 'Test summary'
    assert literature.text == 'Test text'


def test_literature_creation_incorrect():
    with pytest.raises(ValidationError):
        Literature(
            title='Test title',
            authors='Test author',  # Incorrect type
            summary='Test summary',
            text='Test text'
        )
