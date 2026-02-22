import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from ingestion.scanner import scan_directory
from ingestion.chunker import chunk_files
from vectorstore.faiss_store import build_vectorstore, get_retriever
from agent.analyzer import run_analysis
from utils.helpers import print_banner, print_section, fail, status


DEFAULT_QUERY = "Analyze this project and list architectural and logical issues."


def parse_args():
    parser = argparse.ArgumentParser(prog="codesage", description="AI-powered code analysis tool")
    parser.add_argument("path", help="Path to the project directory")
    parser.add_argument("--ask", default=None, help="Question to ask about the codebase")
    return parser.parse_args()


def main():
    args = parse_args()
    query = args.ask if args.ask else DEFAULT_QUERY

    if not os.path.isdir(args.path):
        fail(f"'{args.path}' is not a valid directory")

    print_banner()
    print_section("Scanning project")
    files = scan_directory(args.path)
    if not files:
        fail("No supported source files found in the given directory")
    status(f"Found {len(files)} source files")

    print_section("Chunking code")
    chunks = chunk_files(files)
    status(f"Created {len(chunks)} chunks")

    print_section("Building vector index")
    store = build_vectorstore(chunks)
    retriever = get_retriever(store)
    status("FAISS index ready")

    print_section("Running analysis")
    status(f"Query: {query}")

    result = run_analysis(retriever, query)

    print_section("Result")
    print(f"\n{result}\n")


if __name__ == "__main__":
    main()
