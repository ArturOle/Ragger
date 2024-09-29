
import spacy
import pytextrank   # noqa: F401

from typing import List, Tuple

from ..data_classes import Tag, RelationWeight, Chunk


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
            chunks: List[Chunk],
            filename: str
    ) -> Tuple[List[Tag], List[RelationWeight]]:
        tags = {}
        for chunk in chunks:
            ranked_phrases = self.extract_keywords(chunk.text)

            tags = {
                tag[0]: tag[1] for tag in ranked_phrases
                if tags.get(tag[0], 0) <= tag[1]
            }

        tag_dtos = []
        relations = []
        for tag in tags.items():
            tag_dto = Tag(
                text=tag[0]
            )
            tag_dtos.append(tag_dto)

            relations.append(
                RelationWeight(
                    literature=filename,
                    tag=tag_dto.text,
                    weight=tag[1]
                )
            )

        return tag_dtos, relations
