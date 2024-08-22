
import os
import configparser

config = configparser.ConfigParser()
config.read('/ragger/config.ini')

# Loop through the keys and set them as environment variables
for key in config['DEFAULT']:
    os.environ[key.upper()] = config['DEFAULT'][key]

# Optionally, print the environment variables for verification
for key in config['DEFAULT']:
    print(f'{key.upper()}={os.environ[key.upper()]}')