import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 150
RETRIEVER_K = 6
SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".java"}
