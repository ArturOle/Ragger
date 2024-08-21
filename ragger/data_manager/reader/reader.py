
import os
import sys
import re
import multiprocessing as mp
import logging
import fitz
import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from pydantic import BaseModel
from typing import List, Optional


current_directory = os.path.dirname(__file__)


def setup_logger(name, log_file, level=logging.INFO):
    logging_level = level

    logger = logging.getLogger('Reader Logger')
    logger.setLevel(logging_level)

    file_handler = logging.FileHandler('logs.log')
    console_handler = logging.StreamHandler()

    file_handler.setLevel(logging_level)
    console_handler.setLevel(logging_level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


logger = setup_logger('Reader Logger', 'logs.log', logging.INFO)


class Literature(BaseModel):
    title: str
    text: str
    authors: Optional[List] = None
    summary: Optional[str] = None


class ReadManager:
    def __init__(self, data_path: str):
        if not self._is_path_valid(data_path):
            raise ValueError('Invalid path')

        self.data_path = data_path
        self.is_target_directory = self._is_directory_or_file(data_path)

        self._reader = Reader(
            data_path,
            self.is_target_directory
        )

    @staticmethod
    def _is_path_valid(data_path: str) -> bool:
        return os.path.exists(data_path)

    @staticmethod
    def _is_directory_or_file(data_path: str) -> bool:
        FileTypeRecon.is_directory_or_file(data_path)

    def read(self):
        self._reader.read()

    def _read_directory(self):
        raise NotImplementedError

    def _read_file(self):
        raise NotImplementedError


class Reader:
    def __init__(self, data_path: str, is_target_directory: bool):
        self.data_path = data_path
        self.is_target_directory = is_target_directory

    def read(self):
        raise NotImplementedError


class TextReader(Reader):
    def __init__(self, data_path: str, is_target_directory: bool):
        super().__init__(data_path, is_target_directory)

    def read(self):
        if self.is_target_directory:
            return self._read_directory()
        else:
            return self._read_file()

    def _read_directory(self):
        texts = []
        for root, _, files in os.walk(self.data_path):
            for file in files:
                file_path = os.path.join(root, file)
                texts.append(self._read_file(file_path))
        return texts

    def _read_file(self):
        with open(self.data_path, 'r') as file:
            return file.read()


class PDFReader(Reader):
    def __init__(self, data_path: str, is_target_directory: bool):
        super().__init__(data_path, is_target_directory)
        self.poppler_path = os.getenv("POPPLER_PATH")
        self.tesseract_path = os.getenv("TESSERACT_PATH")
        pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
        print(self.tesseract_path)

    def read(self):
        if self.is_target_directory:
            return self._read_directory()
        else:
            return self._read_file()

    def _read_directory(self):
        texts = []

        for root, _, files in os.walk(self.data_path):
            for file in files:
                file_path = os.path.join(root, file)
                texts.append(self._read_file(file_path))

    def _read_file(self):
        doc = fitz.open(self.data_path)
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
            text = self._read_file_ocr(self.data_path)

        return text

    def _read_file_ocr(self, file_path):
        file_name = os.path.basename(file_path)
        ocr_folder = "/tmp_ocr_images"
        pic_base = f"{current_directory}/{ocr_folder}/{file_name.split('.')[0]}"

        doc = fitz.open(file_path)
        zoom = 4
        mat = fitz.Matrix(zoom, zoom)
        count = 0

        for p in doc:
            count += 1
        for i in range(count):
            val = pic_base+f"_{i+1}.png"
            page = doc.load_page(i)
            pix = page.get_pixmap(matrix=mat)
            pix.save(val)
        doc.close()

        text = ""

        for page in os.listdir(f"{current_directory}/{ocr_folder}"):
            page_data = Image.open(f"{current_directory}/{ocr_folder}/{page}")
            page_text = pytesseract.image_to_string(page_data)
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
