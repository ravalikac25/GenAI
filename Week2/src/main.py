from src.pdf import load_pdfs
from src.chunk import chunk_text, save_chunks
from src.embed import build_collection
from src.rag import rag_pipeline
from src.utils import logger


if __name__ == "__main__":
    # Load PDFs
    raw_docs = load_pdfs("./data/pdfs")

    # Chunk them
    all_chunks = []
    for doc in raw_docs:
        chunks = chunk_text(doc["text"])
        logger.info(f"Chunked file {doc['id']} into {len(chunks)} chunks")
        save_chunks(
            file_id=doc['id'], 
            chunks=chunks, 
            output_dir="./data/chunks", 
            base_filename=doc["id"].replace(".pdf", ""))
        logger.info(f"Saved chunks for {doc['id']} in {len(chunks)} chunks")
        for i, chunk in enumerate(chunk_text(doc["text"])):
            all_chunks.append({"id": f"{doc['id']}_chunk_{i}", "text": chunk})

    # Build Chroma collection
    collection = build_collection(all_chunks)

    # Ask a question
    query = "How was the 2002 Sabarmati Express incident similar to Rwanda 1994?"
    rag_pipeline(query, collection)
