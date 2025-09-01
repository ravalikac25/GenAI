import chromadb
import ollama
from src.utils import logger


def build_collection(chunks, collection_name: str = "pdf_collection"):
    client = chromadb.Client()
    collection = client.create_collection(collection_name)
    logger.info(f"Created chromaDB collection {collection_name}")

    for chunk in chunks:
        embedding = ollama.embeddings(model="all-minilm", prompt=chunk["text"])["embedding"]
        collection.add(ids=[chunk["id"]], documents=[chunk["text"]], embeddings=[embedding])
        logger.info(f"Embedded chunk {chunk['id']}")

    return collection
