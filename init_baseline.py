#!/usr/bin/env python3
import os, json, hashlib
from datetime import datetime

TARGET_DIR = "secure_files"
DB_FILE = "hash_db.json"

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def build_baseline():
    data = {}
    for root, _, files in os.walk(TARGET_DIR):
        for fname in files:
            rel = os.path.relpath(os.path.join(root, fname), TARGET_DIR)
            path = os.path.join(root, fname)
            data[rel] = {
                "hash": sha256_file(path),
                "mtime": os.path.getmtime(path)
            }
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)
    print(f"[{datetime.now().isoformat()}] Baseline saved to {DB_FILE}, {len(data)} files.")

if __name__ == "__main__":
    if not os.path.isdir(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"Created {TARGET_DIR}. Put files inside and rerun.")
    build_baseline()
