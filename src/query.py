import chromadb
import ollama
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="db")

collection = client.get_collection("documents")


def ask_question(question):

    query_embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
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
You are a document QA assistant.

Use ONLY the context below.

If the answer is not present in the context,
reply exactly:

I cannot find the answer in the provided documents.

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

    return answer, results["metadatas"][0]


while True:

    q = input("\nAsk Question: ")

    if q.lower() == "exit":
        break

    answer, sources = ask_question(q)

    print("\nAnswer:\n")
    print(answer)

    print("\nSources Used:\n")

    for source in sources:
        print(
            f"{source['source']} (Page {source['page']})"
        )