import os
import logging

from ragger.data_manager import PDFReader

cur_dir = os.path.dirname(__file__)
logger = logging.getLogger(__name__)


def test_pdf_reader_read():
    logger.info(cur_dir)
    pdf_reader = PDFReader(
        r'.\test\data_manager_test\reader_test\test_files\test.pdf',
        False
    )
    assert pdf_reader.read() == 'Test\ntseT\n'


# def test_pdf_reader_scanned_read():
#     logger.info(cur_dir)
#     pdf_reader = PDFReader(
#         r'test\data_manager_test\reader_test\test_files\test_scanned.pdf',
#         False
#     )
#     assert pdf_reader.read() == 'Test\ntseT\n'
