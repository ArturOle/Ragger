from .extractor import Extractor
from .embedder import Embedder
from ..data_classes import (
    LiteratureDTO,
    Literature,
    LiteratureGraph,
    Chunk
)

from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List


class Preprocessor:
    def __init__(self):
        self.embedder = Embedder()
        self.extractor = Extractor()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
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
        chunks = self.embedder.produce_embeddings(chunks)

        literature = Literature(
            filename=literaturedto.filename,
            filepath=literaturedto.filepath
        )

        tags, relations = self.extractor.produce_tags_and_relations(
            chunks=chunks,
            filename=literaturedto.filename
        )
        tags = self.embedder.produce_embeddings(tags)

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
