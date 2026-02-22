from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from config import EMBEDDING_MODEL, OLLAMA_BASE_URL, RETRIEVER_K


def build_vectorstore(chunks):
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL, base_url=OLLAMA_BASE_URL)
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    store = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    return store


def get_retriever(store):
    return store.as_retriever(search_kwargs={"k": RETRIEVER_K})
