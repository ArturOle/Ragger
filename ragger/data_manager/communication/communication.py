from neo4j import GraphDatabase


class Comunicator:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.driver.verify_connectivity()


if __name__ == "__main__":
    uri = "neo4j://localhost:7687"
    user = "neo4j"
    password = "neo4j"

    communicator = Comunicator(uri, user, password)
    print("Connected to Neo4j")