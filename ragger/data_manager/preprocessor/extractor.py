
import spacy
import pytextrank

from typing import List

from ..data_classes import Tag, RelationWeight, LiteratureDTO


class Extractor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("textrank")

    def extract_keywords(self, text_list: List[str]) -> list:
        ranked_phrases = []

        doc = self.nlp(''.join(text_list))
        for phrase in doc._.phrases:
            ranked_phrases.append([phrase.text, phrase.rank])

        return ranked_phrases

    def produce_tags_and_relations(
            self,
            literature: LiteratureDTO
    ) -> List[Tag]:

        tags = self.extract_keywords(literature.text)

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
