import os
from config import SUPPORTED_EXTENSIONS


def scan_directory(root_path):
    results = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        dirnames[:] = [d for d in dirnames if d not in {"node_modules", ".git", "__pycache__", ".venv", "venv", "dist", "build"}]
        for fname in filenames:
            ext = os.path.splitext(fname)[1]
            if ext not in SUPPORTED_EXTENSIONS:
                continue
            full_path = os.path.join(dirpath, fname)
            try:
                with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                if content.strip():
                    results.append({"path": full_path, "content": content})
            except Exception:
                pass
    return results
