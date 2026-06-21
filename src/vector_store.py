import chromadb
from sentence_transformers import SentenceTransformer
from ingest import chunks

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

print("Connecting to ChromaDB...")

client = chromadb.PersistentClient(path="db")

# Delete existing collection if it already exists
try:
    client.delete_collection("documents")
    print("Old collection deleted.")
except:
    print("No existing collection found.")

# Create fresh collection
collection = client.create_collection(
    name="documents"
)

texts = [chunk["text"] for chunk in chunks]
metadatas = [chunk["metadata"] for chunk in chunks]

print(f"Total Chunks: {len(texts)}")

print("Generating embeddings...")

# Batch embedding (assignment requirement)
embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True
).tolist()

print("Storing embeddings in ChromaDB...")

collection.add(
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=[str(i) for i in range(len(texts))]
)

print("\nDatabase Created Successfully!")
print(f"Chunks Stored: {len(texts)}")