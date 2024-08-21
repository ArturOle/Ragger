# PDF Embedding Extraction and Context Search Engine

## Overview

This project prepared as an unified way of setting up knowledge repository for context search and context injection like Retrieval Augmented Generation (RAG) for Large Language Models (LLMs) projects. The package can be used both as a python library as well as a Command-Line Interface (CLI) solution. The system searches for supproted document files in the selected directories, performs the embedding procedure and pushes these embeddings to the neo4j graph database. The algorithm handles the cases of scanned documents by default with Optical Character Recognition (OCR). 


## Features
- **PDF Embedding Extraction**: Extract embeddings from PDF files to capture their semantic content.
- **OCR Integration**: Utilize OCR to process scanned PDFs and extract text for embedding.
- **Neo4j Database Storage**: Store the extracted embeddings in a Neo4j graph database for efficient querying and retrieval.
- **Context Search Engine**: Develop a search engine that leverages the embeddings to provide context-aware search results.

## Future Plans
- **Knowledge Repository**: Build a comprehensive knowledge repository to support the training of Large Language Models (LLMs).
- **Enhanced Search Capabilities**: Improve the search engine to handle more complex queries and provide more accurate results.
- **Scalability**: Ensure the system can handle large volumes of data and provide fast, reliable performance.

## Getting Started
### Prerequisites
- Python 3.8+
- Neo4j Database
- Tesseract OCR (for OCR functionality)
    
    Available:

    Windows -> https://github.com/UB-Mannheim/tesseract/wiki
    
    Linux -> https://tesseract-ocr.github.io/tessdoc/Installation.html

### Manual Installation
1. Clone the repository:
   ```sh
   *ToDo*

2. Install the required dependencies:
    ```sh
    pip install -r requirements/base.txt
3. Set up the Neo4j database:

    * Install Neo4j from Neo4j Download Center
    * Start the Neo4j server and set up your database credentials.

4. Install Tesseract-OCR

5. Configure the project:

    Update the configuration file with your Neo4j database credentials and other settings.

### Docker Installation

1. Update config.ini (Oprional)

2. Run docekr-compose

    ```sh
    docker compose up
    ```
### Usage
    1. Run the embedding extraction script:
    ```sh
    *ToDo

    2. Push the embeddings to the Neo4j database:
    ```sh
    *ToDo

    3. Start the context search engine:
    ```sh
    *ToDo

### Contributing
We welcome contributions to improve this project. Please fork the repository and submit pull requests with your changes.

### License
This project is licensed under the MIT License. See the LICENSE file for details.

### Contact
For any questions or suggestions, please open an issue or contact us at artur.oleksinski99@gmail.com
