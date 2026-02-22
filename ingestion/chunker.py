from langchain_text_splitters import RecursiveCharacterTextSplitter
from config import CHUNK_SIZE, CHUNK_OVERLAP


def chunk_files(file_list):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\nclass ", "\ndef ", "\n\n", "\n", " ", ""]
    )
    chunks = []
    for file in file_list:
        pieces = splitter.split_text(file["content"])
        for i, piece in enumerate(pieces):
            chunks.append({
                "text": piece,
                "metadata": {"path": file["path"], "chunk_index": i}
            })
    return chunks
