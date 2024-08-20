import os
import logging

from ragger.data_manager import TextReader

cur_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


def test_text_reader_read():
    logger.info(cur_dir)
    try:
        text_reader = TextReader(
            r'test\data_manager_test\reader_test\test_files\test.txt',
            False
        )
        assert text_reader.read() == 'Test\ntseT'
    except Exception as e:
        assert 1 == 0, f"current dir is {cur_dir}, {e}"
    assert text_reader.read() == 'Test\ntseT'
