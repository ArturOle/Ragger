from .extractor import Extractor
from .embedder import Embedder
from ..data_classes import (
    LiteratureDTO,
    Literature,
    Chunk,
    Tag,
    RelationWeight,
    Embeddable,
    LiteratureGraph
)

from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter


class Preprocessor:
    def __init__(self):
        self.embedder = Embedder()
        self.extractor = Extractor()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=200,
            chunk_overlap=40,
            length_function=len,
            is_separator_regex=False
        )

    def process(self, literatures: list[LiteratureDTO]):

        for i, literature in enumerate(literatures):
            literatures[i] = self._process(literature)

        return literatures

    def _process(
            self,
            literaturedto: LiteratureDTO
    ) -> LiteratureGraph:

        chunks = self.produce_chunks(literaturedto.text)
        chunks = self.produce_embeddings(chunks)

        literature = Literature(
            filename=literaturedto.filename,
            filepath=literaturedto.filepath,
            chunks=chunks
        )

        tags, relations = self.produce_tags_and_relations(
            literaturedto
        )
        tags = self.produce_embeddings(tags)

        return LiteratureGraph(
            literature=literature,
            chunks=chunks,
            tags=tags,
            relation_weights=relations
        )

    def produce_chunks(self, text: List[str]) -> List[Chunk]:
        chunk_dtos = []

        for i, page in enumerate(text):
            chunks = self.splitter.split_text(page)
            for chunk in chunks:
                chunk_dtos.append(Chunk(text=chunk, page_number=i))

        return chunk_dtos

    def produce_embeddings(
            self,
            embeddable_objs: List[Embeddable]
    ) -> List[Embeddable]:

        for embeddable_obj in embeddable_objs:
            embeddable_obj.embeddings = self.embedder.embed(
                embeddable_obj.text
            )

        return embeddable_objs

    def produce_tags_and_relations(
            self,
            literature: LiteratureDTO
    ) -> List[Tag]:

        tags = self.extractor.extract_keywords(literature.text)

        tag_dtos = []
        relations = []
        for tag in tags:
            tag_dto = Tag(
                text=tag[0]
            )
            tag_dtos.append(tag_dto)

            relations.append(
                RelationWeight(
                    literature=literature.filename,
                    tag=tag_dto.text,
                    weight=tag[1]
                )
            )

        return tag_dtos, relations
