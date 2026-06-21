import chromadb
import ollama
from sentence_transformers import SentenceTransformer

print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="db")

collection = client.get_collection("documents")


def ask_question(question):

    # Create query embedding
    query_embedding = model.encode(question).tolist()

    # Retrieve relevant chunks
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5,
        include=["documents", "metadatas", "distances"]
    )

    # Similarity check
    best_distance = results["distances"][0][0]

    print(f"\nBest Distance: {best_distance}")

    # Threshold
    if best_distance > 1.2:
        return (
            "I could not find the answer in the provided documents.\n\n"
            "Sources Used: None"
        )

    contexts = []

    for doc, meta in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        contexts.append(
            f"""
Source: {meta['source']}
Page: {meta['page']}

{doc}
"""
        )

    context = "\n\n".join(contexts)

    prompt = f"""
You are a document question answering assistant.

Answer ONLY using the information provided in the context.

If the answer is not present in the context, reply exactly:

I could not find the answer in the provided documents.

Do not use your own knowledge.
Do not make up information.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model="tinyllama",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response["message"]["content"]

    sources = []

    for meta in results["metadatas"][0]:
        source_text = (
            f"{meta['source']} (Page {meta['page']})"
        )

        if source_text not in sources:
            sources.append(source_text)

    answer += "\n\nSources Used:\n\n"
    answer += "\n".join(sources)

    return answer


while True:

    q = input("\nAsk Question: ")

    if q.lower() == "exit":
        break

    answer = ask_question(q)

    print("\nAnswer:\n")
    print(answer)