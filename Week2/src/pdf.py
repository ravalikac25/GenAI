import os
from pypdf import PdfReader
from src.utils import logger


def load_pdfs(folder_path: str):
    docs = []
    for file in os.listdir(folder_path):
        if file.endswith(".pdf"):
            reader = PdfReader(os.path.join(folder_path, file))
            text = ""
            for i, page in enumerate(reader.pages):
                text += page.extract_text() + "\n"
            docs.append({"id": file, "text": text})
            logger.info(f"Loaded file {file}")
    return docs
