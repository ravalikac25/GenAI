import ollama
from src.retrieve import retrieve
from src.utils import logger


def rag_pipeline(query: str, collection):
    results = retrieve(query, collection)
    context = "\n".join(results["documents"][0])
    logger.info(f"Retrieved chunks {results['ids'][0]}")

    prompt = f"""You are a helpful assistant.
Use the context below to answer the question.

Context:
{context}

Question: {query}
"""
    
    logger.info(f"Final prompt:\n{prompt}")

    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    answer = response["message"]["content"]
    
    logger.info(f"Answer:\n{answer}")
