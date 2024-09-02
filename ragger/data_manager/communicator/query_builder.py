from ragger.data_manager.data_classes import Literature, Chunk, Tag


class QueryBuilder:

    @staticmethod
    def add_literature(literature: Literature):
        return f"MERGE (a:Literature {literature.to_dict()})"

    @staticmethod
    def add_chunk(chunk: Chunk):
        return f"MERGE (a:Chunk {chunk.to_dict()})"

    @staticmethod
    def relation_between_chunk_and_literature(
            chunk: Chunk,
            literature: Literature
    ):
        match_chunk = f"MATCH (a:Chunk {chunk.to_dict()})"
        match_literature = f"MATCH (b:Literature {literature.to_dict()})"
        merge = "MERGE (a)-[:CITES]->(b)"
        return f"{match_chunk}, {match_literature}, {merge}"

    @staticmethod
    def add_tag(tag: Tag):
        return f"MERGE (a:Tag {tag.to_dict()})"
