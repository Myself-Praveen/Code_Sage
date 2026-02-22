from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from config import MODEL_NAME, OLLAMA_BASE_URL


def run_analysis(retriever, query):
    docs = retriever.invoke(query)

    context_parts = []
    for doc in docs:
        path = doc.metadata.get("path", "unknown")
        context_parts.append(f"# File: {path}\n{doc.page_content}")

    context = "\n\n---\n\n".join(context_parts)

    llm = ChatOllama(model=MODEL_NAME, base_url=OLLAMA_BASE_URL, temperature=0.2)

    messages = [
        SystemMessage(content="You are an expert code reviewer. Analyze the provided code context and answer the user's question with specific, actionable insights. Reference file paths when relevant."),
        HumanMessage(content=f"Code context:\n\n{context}\n\nQuestion: {query}")
    ]

    response = llm.invoke(messages)
    return response.content
