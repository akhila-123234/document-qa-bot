# Document QA Bot using RAG

## Project Overview

Document QA Bot is a Retrieval-Augmented Generation (RAG) application that allows users to ask natural language questions about a collection of PDF documents.

The system extracts text from documents, splits the text into chunks, generates embeddings, stores them in a vector database, retrieves the most relevant chunks for a user query, and uses a local Large Language Model (TinyLlama via Ollama) to generate grounded answers with source citations.

---

## Tech Stack

### Programming Language

* Python 3.11

### Libraries

* chromadb
* sentence-transformers
* pypdf
* ollama-python
* tqdm

### Models

* Embedding Model: all-MiniLM-L6-v2
* LLM: TinyLlama (via Ollama)

### Vector Database

* ChromaDB (Persistent Local Storage)

---

## Architecture Overview

The application follows a Retrieval-Augmented Generation (RAG) pipeline:

1. Document Ingestion
2. Text Chunking
3. Embedding Generation
4. Vector Storage using ChromaDB
5. Similarity Search Retrieval
6. Answer Generation using TinyLlama

Pipeline Flow:

Documents (PDFs)
↓
Text Extraction
↓
Chunking
↓
Sentence Transformer Embeddings
↓
ChromaDB Vector Store
↓
User Question
↓
Similarity Search
↓
Retrieved Chunks
↓
TinyLlama (Ollama)
↓
Answer + Citations

---

## Chunking Strategy

This project uses a fixed-size chunking strategy.

Configuration:

* Chunk Size: 1000 characters
* Chunk Overlap: 200 characters

Why?

Large documents cannot be embedded efficiently as a single block of text. Splitting documents into smaller overlapping chunks improves retrieval accuracy and preserves context near chunk boundaries.

Metadata stored for each chunk:

* Source filename
* Page number

---

## Embedding Model and Vector Database

### Embedding Model

Model Used:

all-MiniLM-L6-v2

Reason for Selection:

* Lightweight and fast
* Good semantic search performance
* Suitable for local execution
* Widely used for RAG applications

### Vector Database

Database Used:

ChromaDB

Reason for Selection:

* Simple local setup
* Persistent storage
* Fast similarity search
* Easy integration with Python

Database Path:

db/

---

## Project Structure

document-qa-bot/

├── data/

│   ├── document1.pdf

│   ├── document2.pdf

│   ├── document3.pdf

│   ├── document4.pdf

│   └── document5.pdf

├── db/

├── src/

│   ├── ingest.py

│   ├── vector_store.py

│   ├── query.py

├── requirements.txt

├── README.md

└── .gitignore

---

## Setup Instructions

### 1. Clone Repository

git clone <your-github-repository-url>

cd document-qa-bot

### 2. Create Virtual Environment

Windows:

python -m venv venv

venv\Scripts\activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Install Ollama

Download and install Ollama.

Pull TinyLlama model:

ollama pull tinyllama

Verify installation:

ollama list

### 5. Create Vector Database

Run:

python src/vector_store.py

This step:

* Loads PDF files
* Extracts text
* Creates chunks
* Generates embeddings
* Stores vectors in ChromaDB

### 6. Start Question Answering

Run:

python src/query.py

Ask questions interactively.

Exit using:

exit

---

## Environment Variables

This project does not require any API keys.

The application runs completely offline using:

* TinyLlama via Ollama
* Sentence Transformers
* ChromaDB

Therefore no .env file is required.

---

## Example Queries

### Query 1

What is HTML?

Expected Theme:

Definition and purpose of HTML.

### Query 2

What is CSS?

Expected Theme:

Styling and presentation of web pages.

### Query 3

What is JavaScript Hoisting?

Expected Theme:

Variable and function declaration behavior.

### Query 4

What are Python Lists?

Expected Theme:

Python data structures and list operations.

### Query 5

What is Bootstrap?

Expected Theme:

Responsive web design framework.

---

## Known Limitations

1. Small Language Model

TinyLlama is a lightweight model and may generate less accurate answers than larger models.

2. Retrieval Noise

Sometimes unrelated chunks may be retrieved if they are semantically similar.

3. PDF Extraction Quality

Complex PDF layouts may result in imperfect text extraction.

4. No Reranking

Retrieved chunks are used directly without an additional reranking stage.

5. Limited Context Window

Only the top retrieved chunks are passed to the language model.

---

## Features

* Retrieval-Augmented Generation (RAG)
* PDF Question Answering
* Local LLM Inference
* ChromaDB Vector Search
* Offline Execution
* Source Citations
* Interactive Command Line Interface

---

## Author

Akhila
