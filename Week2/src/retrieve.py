import ollama


def retrieve(query: str, collection, k: int = 5):
    q_embedding = ollama.embeddings(model="all-minilm", prompt=query)["embedding"]
    results = collection.query(query_embeddings=[q_embedding], n_results=k)
    return results
