from .extractor import Extractor
from .embedder import Embedder
from ..data_classes import Literature

from langchain.text_splitter import RecursiveCharacterTextSplitter


class ProcessorManager:
    def __init__(self):
        self.pipeline = ProcessingPipeline()

    def process(self, literatures: list[Literature]):
        for literature in literatures:
            literature = self.pipeline.process(literature)

        return literatures


class ProcessingPipeline:
    def __init__(self):
        self.embedder = Embedder()
        self.extractor = Extractor()
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False
        )

    def process(self, literature: Literature):
        keywords = self.extractor.extract_keywords(literature.text)

        chunks = self.splitter.split_text(literature.text)
        embeddings = []
        for chunk in chunks:
            # features = self.nlp(chunk)
            embeddings.extend(self.embedder.embed(chunk))

        literature.keywords = keywords
        literature.embeddings = embeddings

        return literature
