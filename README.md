# CodeSage

A terminal-based AI code analysis tool that scans your project, indexes it using vector embeddings, and answers questions about your codebase using a local LLM via Ollama. No API keys. No billing. Runs entirely on your machine.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Example Queries](#example-queries)
- [Troubleshooting](#troubleshooting)

---

## Overview

CodeSage is a local-first developer tool that lets you ask natural language questions about any codebase. It recursively scans a project directory, chunks source files intelligently, builds a FAISS vector index using Ollama embeddings, retrieves the most relevant code snippets for your query, and sends them as context to a local LLM to generate a detailed analysis.

---

## Demo

![CodeSage in action](demo.gif)

---

## Features

- Recursively scans project directories for source files
- Supports `.py`, `.js`, `.ts`, and `.java` files
- Intelligent code chunking with overlap to preserve context
- Local vector embeddings via `nomic-embed-text` through Ollama
- FAISS-powered semantic search for relevant code retrieval
- LLM analysis via `llama3` (or any Ollama-compatible model)
- Clean terminal output with no external dependencies or API costs
- Simple CLI interface with argparse

---

## Requirements

- Python 3.8 or higher
- [Ollama](https://ollama.com/download) installed and running
- The following Ollama models pulled locally:
  - `llama3` — for code analysis
  - `nomic-embed-text` — for generating embeddings

---

## Installation

**Step 1 — Install Ollama**

Download and install Ollama from https://ollama.com/download

On Windows, the Ollama installer runs it as a background service automatically on startup.

**Step 2 — Pull required models**

Open a terminal and run:

```bash
ollama pull llama3
ollama pull nomic-embed-text
```

This may take a few minutes depending on your internet speed. Models are downloaded once and cached locally.

**Step 3 — Install Python dependencies**

Navigate to the `codesage` directory and run:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
codesage/
│
├── main.py                  # Entry point, CLI argument parsing, orchestration
├── config.py                # Centralized configuration and environment variables
├── requirements.txt         # Python dependencies
├── run.sh                   # One-click runner for Mac/Linux
├── run.bat                  # One-click runner for Windows
│
├── ingestion/
│   ├── __init__.py
│   ├── scanner.py           # Recursively scans directories and reads source files
│   └── chunker.py           # Splits file content into overlapping chunks
│
├── vectorstore/
│   ├── __init__.py
│   └── faiss_store.py       # Builds FAISS index from chunks using Ollama embeddings
│
├── agent/
│   ├── __init__.py
│   └── analyzer.py          # Retrieves relevant chunks and queries the LLM
│
└── utils/
    ├── __init__.py
    └── helpers.py           # Terminal output formatting utilities
```

### Module Responsibilities

**`main.py`**
Parses CLI arguments, orchestrates the full pipeline from scanning to output, and prints results to the terminal.

**`config.py`**
Single source of truth for all configuration values including model names, Ollama base URL, chunk sizes, and supported file extensions. Values can be overridden via a `.env` file.

**`ingestion/scanner.py`**
Walks the given directory recursively, skips irrelevant folders like `node_modules`, `.git`, `__pycache__`, and virtual environments, reads matching source files, and returns their paths and contents.

**`ingestion/chunker.py`**
Uses LangChain's `RecursiveCharacterTextSplitter` to split file contents at natural code boundaries such as class definitions, function definitions, and blank lines. Each chunk retains its source file path as metadata.

**`vectorstore/faiss_store.py`**
Generates embeddings for all chunks using `nomic-embed-text` via Ollama, stores them in a FAISS in-memory vector index, and returns a retriever configured to fetch the top-k most relevant results.

**`agent/analyzer.py`**
Takes the retriever and a user query, fetches the 6 most semantically relevant code chunks, assembles them into a context block with file path annotations, and sends everything to the LLM with a code review system prompt.

**`utils/helpers.py`**
Lightweight terminal formatting helpers for banners, section headers, status messages, and error output.

---

## Configuration

All configuration lives in `config.py` and can be overridden by creating a `.env` file in the project root.

| Variable | Default | Description |
|---|---|---|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama server address |
| `MODEL_NAME` | `llama3` | LLM model used for analysis |
| `EMBEDDING_MODEL` | `nomic-embed-text` | Embedding model for vector indexing |
| `CHUNK_SIZE` | `1200` | Max characters per chunk |
| `CHUNK_OVERLAP` | `150` | Overlap between adjacent chunks |
| `RETRIEVER_K` | `6` | Number of chunks retrieved per query |

**Example `.env` file:**

```
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=llama3
EMBEDDING_MODEL=nomic-embed-text
```

To use a different model, pull it first and update `MODEL_NAME`:

```bash
ollama pull mistral
```

Then in `.env`:
```
MODEL_NAME=mistral
```

---

## Usage

**Basic syntax:**

```bash
python main.py <project_path> [--ask "your question"]
```

**Analyze current directory with default query:**

```bash
python main.py .
```

The default query is: `Analyze this project and list architectural and logical issues.`

**Analyze a specific project with a custom question:**

```bash
python main.py ./my_project --ask "What does this project do?"
```

**Analyze an absolute path:**

```bash
python main.py C:\Users\you\projects\myapp --ask "Are there any security issues?"
```

**Using the run scripts:**

On Windows:
```bash
run.bat
```

On Mac/Linux:
```bash
chmod +x run.sh
./run.sh
```

The run scripts will prompt you interactively for the project path and question.

---

## How It Works

```
Project Directory
      │
      ▼
  scanner.py          Recursively reads .py, .js, .ts, .java files
      │
      ▼
  chunker.py          Splits content into 1200-char chunks with 150-char overlap
      │
      ▼
 faiss_store.py       Embeds chunks using nomic-embed-text → stores in FAISS index
      │
      ▼
  analyzer.py         Query → semantic search → top 6 chunks → LLM context → response
      │
      ▼
  Terminal Output
```

The tool does not write to or modify any files in the scanned project. It is entirely read-only.

---

## Example Queries

```bash
python main.py . --ask "What does this project do?"
python main.py . --ask "List all architectural and logical issues"
python main.py . --ask "Where could this code break in production?"
python main.py . --ask "What functions handle authentication?"
python main.py . --ask "Are there any security vulnerabilities?"
python main.py . --ask "Explain the main entry point"
python main.py . --ask "What dependencies does this project rely on?"
python main.py . --ask "How is error handling implemented?"
python main.py . --ask "Suggest refactoring improvements"
python main.py . --ask "Is there any duplicate or redundant code?"
```

---

## Troubleshooting

**`ModuleNotFoundError: No module named 'langchain_ollama'`**

Run:
```bash
pip install langchain-ollama
```

**`Connection refused` or `httpx.ConnectError`**

Ollama is not running. On Windows, check the system tray for the Ollama icon. If it's not there, launch Ollama from the Start menu or run `ollama serve` in a separate terminal.

**`model not found` error**

The requested model hasn't been pulled yet. Run:
```bash
ollama pull llama3
ollama pull nomic-embed-text
```

**`No supported source files found`**

The directory you pointed to has no `.py`, `.js`, `.ts`, or `.java` files, or they're all inside excluded folders like `node_modules` or `.git`.

**Analysis seems unrelated to your question**

The retriever is fetching chunks by semantic similarity. If your query uses terms that don't appear in or near the relevant code, try rephrasing with more specific technical language matching what's likely in the source.

---

## License

MIT
