from ..data_classes import (
    LiteratureDTO,
    Literature,
    LiteratureGraph,
)
from .extractor import Extractor
from .embedder import Embedder
from .text_splitter import TextSplitter


class Preprocessor:
    def __init__(self):
        self.embedder = Embedder()
        self.extractor = Extractor()
        self.splitter = TextSplitter(
            order="any",
            separators=['\.', '\n\n', '\n', '\s'],
            is_separator_regex=True
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
