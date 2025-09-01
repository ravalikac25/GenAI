import os
import glob
from src.utils import logger


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    chunks, start = [], 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def save_chunks(file_id: str, chunks, output_dir: str, base_filename: str):
    os.makedirs(output_dir, exist_ok=True)

    # 🧹 Cleanup old chunks for this file (idempotency)
    old_files = glob.glob(os.path.join(output_dir, f"*.txt"))
    for old_file in old_files:
        os.remove(old_file)
        logger.info(f"Removed old chunk file: {old_file}")

    # Write new chunks
    paths = []
    for i, chunk in enumerate(chunks):
        file_path = os.path.join(output_dir, f"{base_filename}_chunk_{i}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chunk)
        paths.append(file_path)
        logger.info(f"Saved chunk #{i} from file {file_id} to {file_path}")

    return paths
