
import spacy
import pytextrank

from typing import List


class Extractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def extract_keywords(self, text_list: List[str]) -> list:
        self.nlp = spacy.load("en_core_web_sm")
        ranked_phrases = []

        self.nlp.add_pipe("textrank")
        doc = self.nlp(''.join(text_list))
        for phrase in doc._.phrases:
            ranked_phrases.append([phrase.text, phrase.rank])

        return ranked_phrases
