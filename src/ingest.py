import os
from pypdf import PdfReader

DATA_FOLDER = "data"

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200


def extract_pdf(file_path):

    pages = []

    reader = PdfReader(file_path)

    for i, page in enumerate(reader.pages):

        text = page.extract_text()

        if text and text.strip():

            pages.append({
                "text": text,
                "metadata": {
                    "source": os.path.basename(file_path),
                    "page": i + 1
                }
            })

    return pages


def chunk_pages(pages):

    chunks = []

    for page in pages:

        text = page["text"]

        metadata = page["metadata"]

        start = 0

        while start < len(text):

            end = start + CHUNK_SIZE

            chunk_text = text[start:end]

            chunks.append({
                "text": chunk_text,
                "metadata": metadata
            })

            start += (CHUNK_SIZE - CHUNK_OVERLAP)

    return chunks


all_pages = []

for file in os.listdir(DATA_FOLDER):

    if file.endswith(".pdf"):

        path = os.path.join(DATA_FOLDER, file)

        pages = extract_pdf(path)

        all_pages.extend(pages)

chunks = chunk_pages(all_pages)

print("Total Pages:", len(all_pages))

print("Total Chunks:", len(chunks))

print("\nSample Chunk Metadata:")

print(chunks[0]["metadata"])

print("\nSample Chunk Text:\n")

print(chunks[0]["text"][:500])