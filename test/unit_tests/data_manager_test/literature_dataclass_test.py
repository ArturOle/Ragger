
import pytest
from ragger.data_manager.data_classes import (
    Literature,
    Chunk,
    Tag,
    RelationWeight,
    LiteratureDTO,
    LiteratureGraph,
    Embeddable
)

from pydantic import ValidationError


def test_literature_creation_correct():
    literature = Literature(
        filename='filename',
        filepath=r'f:\ile\pat.h'
    )

    assert literature.filename == 'filename'
    assert literature.filepath == r'f:\ile\pat.h'


def test_literature_creation_incorrect():
    with pytest.raises(ValidationError):
        Literature(
            filename='filename',
            filepath=[r'f:\ile\pat.h']  # should be a string
        )


def test_chunk_creation_correct():
    chunk = Chunk(
        text='text',
        page_number=1
    )

    assert chunk.text == 'text'
    assert chunk.page_number == 1


def test_chunk_creation_incorrect():
    with pytest.raises(ValidationError):
        #  TODO: Description: Extreme! Pydantic accepts "1" as integer?! Task: Reasearch
        Chunk(
            text='text',
            page_number='One'  # should be an integer
        )


def test_tag_creation_correct():
    tag = Tag(
        text='text',
        description='description'
    )

    assert tag.text == 'text'
    assert tag.description == 'description'


def test_tag_creation_incorrect():
    with pytest.raises(ValidationError):
        Tag(
            text='text',
            description=['description']  # should be a string
        )


def test_relation_weight_creation_correct():
    relation_weight = RelationWeight(
        literature='literature',
        tag='tag',
        weight=0.5
    )

    assert relation_weight.literature == 'literature'
    assert relation_weight.tag == 'tag'
    assert relation_weight.weight == 0.5


def test_relation_weight_creation_incorrect():
    with pytest.raises(ValidationError):
        RelationWeight(
            literature='literature',
            tag='tag',
            weight='Zero point five'  # should be a float
        )


def test_literature_dto_creation_correct():
    literature_dto = LiteratureDTO(
        filename='filename',
        filepath=r'f:\ile\pat.h',
        text=['text']
    )

    assert literature_dto.filename == 'filename'
    assert literature_dto.filepath == r'f:\ile\pat.h'
    assert literature_dto.text == ['text']


def test_literature_dto_creation_incorrect():
    with pytest.raises(ValidationError):
        LiteratureDTO(
            filename='filename',
            filepath=r'f:\ile\pat.h',
            text='text'  # should be a list
        )


def test_literature_graph_creation_correct():
    literature_graph = LiteratureGraph(
        literature=Literature(
            filename='filename',
            filepath=r'f:\ile\pat.h'
        ),
        chunks=[Chunk(text='text')],
        tags=[Tag(text='text')],
        relation_weights=[RelationWeight(
            literature='literature',
            tag='tag',
            weight=0.5
        )]
    )

    assert literature_graph.literature.filename == 'filename'
    assert literature_graph.literature.filepath == r'f:\ile\pat.h'
    assert len(literature_graph.chunks) == 1
    assert len(literature_graph.tags) == 1
    assert len(literature_graph.relation_weights) == 1


def test_literature_graph_creation_incorrect():
    with pytest.raises(ValidationError):
        LiteratureGraph(
            literature=Literature(
                filename='filename',
                filepath=r'f:\ile\pat.h'
            ),
            chunks=[Chunk(text='text')],
            tags=[Chunk(text='text')], # should be a list of Tag
            relation_weights=[RelationWeight(
                literature='literature',
                tag='tag',
                weight='0.5'
            )]
        )


def test_embeddable_creation_correct():
    embeddable = Embeddable(
        embeddings=['embeddings']
    )

    assert embeddable.embeddings == ['embeddings']
    assert isinstance(Tag(text=":)"), Embeddable)
    assert isinstance(Chunk(text=":)"), Embeddable)
    assert not isinstance(RelationWeight(literature=":(", tag=":(", weight=0.5), Embeddable)
