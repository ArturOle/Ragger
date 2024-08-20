# Deletes all trailning white spaces from current directory recurrently for ".py" files

import os
import tqdm


def remove_trailing_whitespace(file_path):
    lines_corrected = 0
    with open(file_path, 'r') as file:
        lines = file.readlines()

    with open(file_path, 'w') as file:
        for line in lines:
            clean_line = line.rstrip() + '\n'
            file.write(clean_line)
            if line != clean_line:
                lines_corrected += 1

    return lines_corrected


def process_directory(directory):
    for root, _, files in tqdm.tqdm(os.walk(directory), desc="Processing files"):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                corrected_lines = remove_trailing_whitespace(file_path)
                tqdm.tqdm.write(f"Processed: {file_path}. Corrected lines: {corrected_lines}")


if __name__ == "__main__":
    current_directory = os.getcwd()
    process_directory(current_directory)
