import chromadb
from sentence_transformers import SentenceTransformer
from ingest import chunks

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Creating ChromaDB...")

client = chromadb.PersistentClient(path="db")

collection = client.get_or_create_collection(
    name="documents"
)

texts = [chunk["text"] for chunk in chunks]
metadatas = [chunk["metadata"] for chunk in chunks]

print("Generating embeddings...")

embeddings = model.encode(texts).tolist()

collection.add(
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=[str(i) for i in range(len(texts))]
)

print("Database Created Successfully!")
print("Chunks Stored:", len(texts))