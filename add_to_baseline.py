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

def load_baseline():
    """Load existing baseline"""
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_baseline(data):
    """Save baseline to file"""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_file_to_baseline(filepath):
    """Add a specific file to baseline"""
    baseline = load_baseline()
    
    # Check if file exists
    if not os.path.exists(filepath):
        print(f"[ERROR] File not found: {filepath}")
        return False
    
    # Get relative path
    try:
        if filepath.startswith(TARGET_DIR):
            rel_path = os.path.relpath(filepath, TARGET_DIR)
        else:
            rel_path = filepath
            filepath = os.path.join(TARGET_DIR, filepath)
            if not os.path.exists(filepath):
                print(f"[ERROR] File not found in {TARGET_DIR}: {rel_path}")
                return False
    except ValueError:
        print(f"[ERROR] File must be inside {TARGET_DIR} directory")
        return False
    
    # Calculate hash
    try:
        file_hash = sha256_file(filepath)
        file_mtime = os.path.getmtime(filepath)
        
        # Check if file already in baseline
        if rel_path in baseline:
            old_hash = baseline[rel_path]["hash"] if isinstance(baseline[rel_path], dict) else baseline[rel_path]
            if old_hash == file_hash:
                print(f"[INFO] File '{rel_path}' already in baseline with same hash.")
                return True
            else:
                print(f"[UPDATE] Updating hash for '{rel_path}'")
                print(f"  Old hash: {old_hash[:16]}...")
                print(f"  New hash: {file_hash[:16]}...")
        else:
            print(f"[ADD] Adding new file '{rel_path}' to baseline")
        
        # Add/update file in baseline
        baseline[rel_path] = {
            "hash": file_hash,
            "mtime": file_mtime
        }
        
        # Save baseline
        save_baseline(baseline)
        print(f"[SUCCESS] Baseline updated successfully!")
        print(f"  Total files in baseline: {len(baseline)}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Failed to process file: {e}")
        return False

def add_all_new_files():
    """Add all files in secure_files that are not in baseline"""
    baseline = load_baseline()
    added_count = 0
    updated_count = 0
    
    for root, _, files in os.walk(TARGET_DIR):
        for fname in files:
            rel = os.path.relpath(os.path.join(root, fname), TARGET_DIR)
            path = os.path.join(root, fname)
            
            try:
                file_hash = sha256_file(path)
                file_mtime = os.path.getmtime(path)
                
                if rel in baseline:
                    old_hash = baseline[rel]["hash"] if isinstance(baseline[rel], dict) else baseline[rel]
                    if old_hash != file_hash:
                        print(f"[UPDATE] '{rel}'")
                        updated_count += 1
                else:
                    print(f"[ADD] '{rel}'")
                    added_count += 1
                
                baseline[rel] = {
                    "hash": file_hash,
                    "mtime": file_mtime
                }
            except Exception as e:
                print(f"[ERROR] Failed to process '{rel}': {e}")
    
    save_baseline(baseline)
    print(f"\n[SUCCESS] Baseline updated!")
    print(f"  Files added: {added_count}")
    print(f"  Files updated: {updated_count}")
    print(f"  Total files in baseline: {len(baseline)}")

def list_baseline_files():
    """List all files in baseline"""
    baseline = load_baseline()
    if not baseline:
        print("Baseline is empty. Run 'python init_baseline.py' first.")
        return
    
    print(f"\n{'='*70}")
    print(f"Files in Baseline ({len(baseline)} total)")
    print(f"{'='*70}")
    for i, (filepath, data) in enumerate(sorted(baseline.items()), 1):
        if isinstance(data, dict):
            hash_val = data.get("hash", "N/A")[:16]
            mtime = datetime.fromtimestamp(data.get("mtime", 0)).strftime("%Y-%m-%d %H:%M:%S")
        else:
            hash_val = data[:16]
            mtime = "N/A"
        print(f"{i:3}. {filepath}")
        print(f"     Hash: {hash_val}... | Modified: {mtime}")
    print(f"{'='*70}\n")

def remove_from_baseline(filepath):
    """Remove a file from baseline"""
    baseline = load_baseline()
    
    # Try as relative path first
    if filepath in baseline:
        del baseline[filepath]
        save_baseline(baseline)
        print(f"[SUCCESS] Removed '{filepath}' from baseline")
        print(f"  Total files in baseline: {len(baseline)}")
        return True
    
    # Try to find by filename
    rel_path = os.path.relpath(filepath, TARGET_DIR) if filepath.startswith(TARGET_DIR) else filepath
    if rel_path in baseline:
        del baseline[rel_path]
        save_baseline(baseline)
        print(f"[SUCCESS] Removed '{rel_path}' from baseline")
        print(f"  Total files in baseline: {len(baseline)}")
        return True
    
    print(f"[ERROR] File '{filepath}' not found in baseline")
    return False

def show_help():
    """Show help message"""
    print("""
╔════════════════════════════════════════════════════════════════╗
║          Baseline Management Tool - Add Verified Files         ║
╚════════════════════════════════════════════════════════════════╝

Usage:
    python add_to_baseline.py [command] [arguments]

Commands:
    add <filepath>      Add specific file to baseline
                        Example: python add_to_baseline.py add demo.txt
                                python add_to_baseline.py add secure_files/demo.txt

    add-all            Add ALL files in secure_files/ to baseline
                        Example: python add_to_baseline.py add-all

    list               List all files currently in baseline
                        Example: python add_to_baseline.py list

    remove <filepath>   Remove file from baseline
                        Example: python add_to_baseline.py remove demo.txt

    help               Show this help message

Examples:
    # Add single file
    python add_to_baseline.py add halo.js
    
    # Add all new files
    python add_to_baseline.py add-all
    
    # List baseline
    python add_to_baseline.py list
    
    # Remove file
    python add_to_baseline.py remove malicious.exe

Note:
    - Files must be inside 'secure_files/' directory
    - Adding existing file will update its hash
    - Use 'add-all' to verify all current files at once
""")

if __name__ == "__main__":
    import sys
    
    if not os.path.isdir(TARGET_DIR):
        print(f"[ERROR] Directory '{TARGET_DIR}' not found!")
        print(f"Please create it first: mkdir {TARGET_DIR}")
        sys.exit(1)
    
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == "help" or command == "-h" or command == "--help":
        show_help()
    
    elif command == "add":
        if len(sys.argv) < 3:
            print("[ERROR] Please specify a file to add")
            print("Usage: python add_to_baseline.py add <filepath>")
        else:
            filepath = sys.argv[2]
            add_file_to_baseline(filepath)
    
    elif command == "add-all":
        print("Adding all files in secure_files/ to baseline...")
        add_all_new_files()
    
    elif command == "list":
        list_baseline_files()
    
    elif command == "remove":
        if len(sys.argv) < 3:
            print("[ERROR] Please specify a file to remove")
            print("Usage: python add_to_baseline.py remove <filepath>")
        else:
            filepath = sys.argv[2]
            remove_from_baseline(filepath)
    
    else:
        print(f"[ERROR] Unknown command: {command}")
        print("Run 'python add_to_baseline.py help' for usage information")
        sys.exit(1)
