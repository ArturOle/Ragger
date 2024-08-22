import rake_nltk
import nltk

from ..data_classes import Literature


class Extractor:
    def __init__(self):
        self.rake = rake_nltk.Rake()

    def extract_keywords(self, text: Literature):
        return self.rake.run(text)

    def extract_sentences(self, text: Literature):
        return nltk.sent_tokenize(text)
