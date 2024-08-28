from neo4j import GraphDatabase
from ..utils import setup_logger
# from ragger.data_manager.data_classes import Literature

logger = setup_logger("Communicator Logger", "logs.log")


class Literature:
    def __init__(self, filename, text, text_position, page_number):
        self.filename = filename
        self.text = text
        self.text_position = text_position
        self.page_number = page_number

    def __eq__(self, other):
        return self.filename == other.filename and self.text == other.text and self.text_position == other.text_position and self.page_number == other.page_number

    def __repr__(self):
        return f"filename: {self.filename}, text: {self.text}, text_position: {self.text_position}, page_number: {self.page_number}"

    def __str__(self):
        return f"filename: {self.filename}, text: {self.text}, text_position: {self.text_position}, page_number: {self.page_number}"


class Communicator:
    def __init__(self, uri, user, password):
        self._uri = uri
        self._user = user
        self._password = password
        self._driver = None

    @property
    def driver(self):
        if self._driver is None:
            self._driver = GraphDatabase.driver(
                self._uri,
                auth=(self._user, self._password)
            )
        return self._driver

    @driver.setter
    def driver(self, driver):
        self._driver = driver

    @driver.deleter
    def driver(self):
        self._driver = None

    @staticmethod
    def connection(func):
        def wrapper(self, *args, **kwargs):
            with self.driver.session(database="neo4j") as session:
                return func(self, session, *args, **kwargs)
        return wrapper

    @connection
    def add_literature(self, session, literature: Literature):
        session.write_transaction(self._add_literature, literature)

    def _add_literature(self, tx, literature: Literature):
        try:
            tx.run(
                "MERGE (a:Literature {filename: $filename, text: $text, text_position: $text_position, page_number: $page_number})",
                filename=literature.filename,
                text=literature.text,
                text_position=literature.text_position,
                page_number=literature.page_number
            )
        except Exception as e:
            logger.error(f"Error while adding literature: {e}")
            tx.rollback()

    @connection
    def get_literature(self, session, filename):
        return session.read_transaction(self._get_literature, filename)

    def _get_literature(self, tx, filename):
        try:
            return tx.run(
                "MATCH (a:Literature) WHERE a.filename = $filename RETURN a",
                filename=filename
            ).single()[0]
        except TypeError:
            logger.info("No literatures found.")
            return None

    @connection
    def get_all_literatures(self, session):
        return session.read_transaction(self._get_all_literatures)

    def _get_all_literatures(self, tx):
        try:
            return [record[0] for record in tx.run(
                "MATCH (a:Literature) RETURN a"
            )]
        except TypeError:
            logger.info("No literatures found.")
            return []

    @connection
    def delete_literature(self, session, filename):
        session.write_transaction(self._delete_literature, filename)

    def _delete_literature(self, tx, filename):
        return tx.run(
            "MATCH (a:Literature) WHERE a.filename = $filename DELETE a",
            filename=filename
        )


if __name__ == "__main__":
    communicator = Communicator("neo4j://localhost:7687", "neo4j", "StrongPsPsP5")
    print("Communicator created.")
    literature = Literature("test", "This is a test text.", 0, 0)
    communicator.add_literature(literature)
    print("Literature added.")
    print(communicator.get_literature("test"))
    print(communicator.get_all_literatures())
    communicator.delete_literature("test")
    print(communicator.get_all_literatures())
