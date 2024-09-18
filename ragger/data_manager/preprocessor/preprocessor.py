from .extractor import Extractor
from .embedder import Embedder
from ..data_classes import (
    LiteratureDTO,
    Literature,
    LiteratureGraph
)

from .text_splitter import RecursiveCharacterTextSplitter


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

        chunks = self.splitter.produce_chunks(literaturedto.text)
        chunks = self.embedder.produce_embeddings(chunks)

        literature = Literature(
            filename=literaturedto.filename,
            filepath=literaturedto.filepath
        )

        tags, relations = self.extractor.produce_tags_and_relations(
            literaturedto
        )
        tags = self.embedder.produce_embeddings(tags)

        return LiteratureGraph(
            literature=literature,
            chunks=chunks,
            tags=tags,
            relation_weights=relations
        )
