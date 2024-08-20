import os
import logging

from ragger.data_manager import TextReader

cur_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


def test_text_reader_read():
    text_reader = TextReader(
        r'.\test\data_manager_test\reader_test\test_files\test.txt',
        False
    )

    assert text_reader.read() == 'Test\ntseT'
