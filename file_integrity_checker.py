import hashlib
import os
import json

MONITOR_DIR = 'files_to_monitor'
HASHES_FILE = 'hashes.json'

def calculate_hash(filepath):
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def load_hashes():
    if not os.path.exists(HASHES_FILE):
        return {}
    with open(HASHES_FILE, 'r') as f:
        return json.load(f)

def save_hashes(hashes):
    with open(HASHES_FILE, 'w') as f:
        json.dump(hashes, f, indent=4)

def scan_and_compare():
    current_hashes = {}
    old_hashes = load_hashes()

    for root, _, files in os.walk(MONITOR_DIR):
        for filename in files:
            path = os.path.join(root, filename)
            rel_path = os.path.relpath(path, MONITOR_DIR)
            current_hashes[rel_path] = calculate_hash(path)

    print("\n🔍 Integrity Report:")
    for path, current_hash in current_hashes.items():
        if path not in old_hashes:
            print(f"[NEW] {path}")
        elif old_hashes[path] != current_hash:
            print(f"[MODIFIED] {path}")
        else:
            print(f"[UNCHANGED] {path}")

    for path in old_hashes:
        if path not in current_hashes:
            print(f"[DELETED] {path}")

    save_hashes(current_hashes)

if __name__ == "__main__":
    os.makedirs(MONITOR_DIR, exist_ok=True)
    scan_and_compare()
