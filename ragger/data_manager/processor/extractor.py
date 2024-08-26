
import spacy
import pytextrank

from ..data_classes import Literature
from .embedder import Embedder


class Extractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_keywords(self, text: Literature):
        self.nlp = spacy.load("en_core_web_sm")
        ranked_phrases = []

        self.nlp.add_pipe("textrank")
        doc = self.nlp(text)
        for phrase in doc._.phrases:
            ranked_phrases.append([phrase.text, phrase.rank])

        return ranked_phrases

    def extract_authors(self, text: Literature):
        pass

    def extract_topics(self, text: Literature):
        pass

    # def extract_sentences(self, text: Literature):
    #     return nltk.sent_tokenize(text)
