#!/usr/bin/env python3
import os, json, hashlib, logging
from datetime import datetime

TARGET_DIR = "secure_files"
DB_FILE = "hash_db.json"
LOG_FILE = "security.log"

# --- custom logger with ALERT level ---
ALERT_LEVEL = 45
logging.addLevelName(ALERT_LEVEL, "ALERT")

logger = logging.getLogger("secmon")
logger.setLevel(logging.DEBUG)
fmt = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
fh = logging.FileHandler(LOG_FILE)
fh.setFormatter(fmt)
logger.addHandler(fh)
# also print to console
ch = logging.StreamHandler()
ch.setFormatter(fmt)
logger.addHandler(ch)

def alert(msg):
    logger.log(ALERT_LEVEL, msg)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

def load_baseline():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def scan_current():
    cur = {}
    for root, _, files in os.walk(TARGET_DIR):
        for fname in files:
            rel = os.path.relpath(os.path.join(root, fname), TARGET_DIR)
            path = os.path.join(root, fname)
            try:
                cur[rel] = sha256_file(path)
            except Exception as e:
                logger.warning(f"Failed hashing {rel}: {e}")
    return cur

def simulate_alert_send(level, filename, detail=""):
    # Simulasi: print ke console / bisa diganti kirim email dummy
    print(f"[SIMULATED ALERT] {level}: {filename} {detail}")

def main():
    baseline = load_baseline()
    current = scan_current()

    baseline_files = set(baseline.keys())
    current_files = set(current.keys())

    # 1) files present & checked
    for f in sorted(baseline_files & current_files):
        stored = baseline[f]["hash"] if isinstance(baseline[f], dict) and "hash" in baseline[f] else baseline[f]
        now = current[f]
        if stored == now:
            logger.info(f'File "{f}" verified OK.')
        else:
            logger.warning(f'File "{f}" integrity failed!')
            simulate_alert_send("WARNING", f, "hash mismatch")
            # You can also call alert(...) depending on your policy (we keep it warning + simulated alert)

    # 2) new unknown files
    for f in sorted(current_files - baseline_files):
        alert(f'Unknown file "{f}" detected.')
        simulate_alert_send("ALERT", f, "unknown file")

    # 3) deleted/missing files
    for f in sorted(baseline_files - current_files):
        alert(f'File "{f}" missing (possibly deleted).')

if __name__ == "__main__":
    if not os.path.isdir(TARGET_DIR):
        print(f"Target dir {TARGET_DIR} missing. Create and add files.")
    else:
        main()
        print("Monitoring run complete. Check", LOG_FILE)
