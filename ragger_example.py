# Onlt for testing purposes

import os

from ragger.data_manager import DataManager


cwd = os.getcwd()

dm = DataManager()
dm.insert([
    cwd + r"/data/pdf-ai-generated/ES_article.pdf",
    cwd + r"/data/pdf-ai-generated/ML_article.pdf",
    cwd + r"/data/pdf-ai-generated/HumanInteligence_article.pdf"
])
