# Ragger - from raw files to LLM-application (WIP)

Start date 22.08.2024

## Overview

This project was prepared as a simplified way of setting up a knowledge repository for context search and context injection, such as Retrieval Augmented Generation (RAG) for Large Language Models (LLMs) projects. The package will be used both as a Python library as well as a Command-Line Interface (CLI) solution. The system searches for supported document files in the selected directories performs the embedding procedure, and pushes these embeddings to the Neo4j graph database. The system handles the cases of scanned documents by default with Optical Character Recognition (OCR).


## Features
- **PDF Embedding Extraction**: Extract embeddings from PDF files to capture their semantic content.
- **OCR Integration**: Utilize OCR to process scanned PDFs and extract text for embedding.
- **Neo4j Database Storage**: Store the extracted embeddings in a Neo4j graph database for efficient querying and retrieval.
- **Context Search Engine**: Develop a search engine that leverages the embeddings to provide context-aware search results.

## Future Plans
- **Knowledge Repository**: Build a comprehensive knowledge repository to support the training of Large Language Models (LLMs).
- **Enhanced Search Capabilities**: Improve the search to handle more complex queries and provide more accurate results.
- **Scalability**: Ensure the system can handle large volumes of data and provide fast, reliable performance.

## Getting Started
### Prerequisites
- Python 3.10+
- Neo4j Database
- Tesseract OCR (for OCR functionality)
    
    Available:

    Windows -> https://github.com/UB-Mannheim/tesseract/wiki
    
    Linux -> https://tesseract-ocr.github.io/tessdoc/Installation.html

- Poppler (for OCR)

    Available:

    Docs -> https://poppler.freedesktop.org/

### Docker Installation

1. Update config.ini (Oprional)

2. Run docker-compose

    ```sh
    docker compose up
    ```

### Contributing
Please, hold on with the contribution until the first major release.

### License
This project is licensed under the GPL-3.0 License. See the LICENSE file for details.

### Contact
For any questions or suggestions, please open an issue or contact us at artur.oleksinski99@gmail.com
