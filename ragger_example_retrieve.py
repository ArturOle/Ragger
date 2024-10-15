# Only for testing purposes

# if you want to test retriving data, first use ragger_example_submit.py to insert data

import os
from pprint import pprint
from ragger.data_manager import DataManager


cwd = os.getcwd()

dm = DataManager()
print(dm.retrieve_data("machine Inteligence", 5))
