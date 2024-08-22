
import os
import logging
import fitz
import pytesseract
from pdf2image import convert_from_path

from pydantic import BaseModel
from typing import List, Optional

from ragger.utils import get_config_variables, setup_logger

current_directory = os.path.dirname(__file__)


logger = setup_logger('Reader Logger', 'logs.log', logging.INFO)


class Literature(BaseModel):
    title: str
    text: str
    authors: Optional[List] = None
    summary: Optional[str] = None


class ReadManager:
    _pdf_reader = None
    _text_reader = None

    @property
    def pdf_reader(self):
        if self._pdf_reader is None:
            self._pdf_reader = PDFReader()
        return self._pdf_reader

    @property
    def text_reader(self):
        if self._text_reader is None:
            self._text_reader = TextReader(self.data_path)
        return self._text_reader

    @staticmethod
    def _is_path_valid(data_path: str) -> bool:
        return os.path.exists(data_path)

    @staticmethod
    def _is_directory_or_file(data_path: str) -> bool:
        FileTypeRecon.is_directory_or_file(data_path)

    def read(self, data_path: str) -> List[Literature]:
        if self.is_target_directory(data_path):
            return self._read_directory(data_path)
        else:
            return [self._read_file(data_path)]

    def _read_directory(self, directory_path: str) -> List[Literature]:
        for file_name in os.listdir(directory_path):
            file_path = os.path.join(directory_path, file_name)
            text = self._read_file(file_path)

            yield Literature(title=file_name, text=text)

    def _read_file(self, file_path: str) -> Literature:
        file_type = FileTypeRecon.recognize_type(file_path)

        if file_type == 'txt':
            text = self.pdf_reader.read(file_path)
        elif file_type == 'pdf':
            text = self.text_reader.read(file_path)

        return Literature(title=file_path, text=text)


class TextReader:

    @staticmethod
    def read(data_path: str):
        with open(data_path, 'r') as file:
            return file.read()


class PDFReader:
    """
    PDFReader class handles the reading of both difital and scanned PDF files
    with PyMuPDF and pytesseract libraries. If the document is scanned, the
    text is extracted using OCR.
    """
    def __init__(self):
        self.tesseract_path = ""
        self.poppler_path = ""
        self._setup_paths_from_config()

    def _setup_paths_from_config(self):
        """
        Assures that if the paths are not set in the environment variables,
        they are set from the config file. After sercond iteration it
        should not be necessary, as the paths should be set in the
        environment variables.

        To wokr properly, the config.ini file should be in the same
        directory as the script that is being run with paths to tesseract
        and poppler bin folder (NOT TO EXECUTABLES, BUT FOLDERS).
        """
        if not os.getenv("POPPLER_PATH") or not os.getenv("TESSERACT_PATH"):
            self.tesseract_path, self.poppler_path = get_config_variables()

        if os.getenv("POPPLER_PATH"):
            self.poppler_path = os.getenv("POPPLER_PATH")
        else:
            os.environ["POPPLER_PATH"] = self.poppler_path

        if os.getenv("TESSERACT_PATH"):
            self.tesseract_path = os.getenv("TESSERACT_PATH")
        else:
            os.environ["TESSERACT_PATH"] = self.tesseract_path

        pytesseract.pytesseract.tesseract_cmd = os.path.join(
            self.tesseract_path, "tesseract"
        )

    def read(self, data_path: str) -> str:
        doc = fitz.open(data_path)
        text = ""

        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            text += page_text

        doc.close()

        if text == "":
            logger.info(
                'No text found in document which indicates scan, trying OCR'
            )
            text = self._read_file_ocr(data_path)

        return text

    def _read_file_ocr(self, file_path):

        pages = convert_from_path(file_path, 300)

        text = ""

        for page in pages:
            page_text = pytesseract.image_to_string(page)
            text += page_text + "\n"

        return text


class FileTypeRecon:
    file_type_classes = {
        'txt',
        'pdf'
    }

    @staticmethod
    def is_path_valid(data_path: str) -> bool:
        return os.path.exists(data_path)

    @staticmethod
    def is_directory_or_file(data_path: str) -> bool:
        if os.path.isdir(data_path):
            return True
        elif os.path.isfile(data_path):
            return False

    @staticmethod
    def recognize_type(data_path):
        for file_type in FileTypeRecon.file_type_classes:
            if data_path.endswith(file_type):
                return file_type
        else:
            raise ValueError('Unsupported file type')


if __name__ == '__main__':
    data_path = r"E:\Projects\ContextSearch\test\data_manager_test\reader_test\test_files\test_scanned.pdf"
    read_manager = PDFReader(data_path, False)
    print(read_manager.read())
