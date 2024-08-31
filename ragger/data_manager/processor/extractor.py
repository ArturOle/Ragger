
import spacy

from ..data_classes import Literature


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
