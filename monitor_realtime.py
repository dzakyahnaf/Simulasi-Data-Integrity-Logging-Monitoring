#!/usr/bin/env python3
import os, json, hashlib, logging, time
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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

def simulate_alert_send(level, filename, detail=""):
    # Simulasi: print ke console / bisa diganti kirim email dummy
    print(f"[SIMULATED ALERT] {level}: {filename} {detail}")

def check_file_integrity(filepath):
    """Check integrity of a single file against baseline"""
    baseline = load_baseline()
    
    # Get relative path
    try:
        rel_path = os.path.relpath(filepath, TARGET_DIR)
    except ValueError:
        # File is not in TARGET_DIR
        return
    
    # Skip if file doesn't exist (might be deleted)
    if not os.path.exists(filepath):
        if rel_path in baseline:
            alert(f'File "{rel_path}" missing (possibly deleted).')
            simulate_alert_send("ALERT", rel_path, "file deleted")
        return
    
    try:
        current_hash = sha256_file(filepath)
        
        if rel_path in baseline:
            # File exists in baseline - check integrity
            stored = baseline[rel_path]["hash"] if isinstance(baseline[rel_path], dict) and "hash" in baseline[rel_path] else baseline[rel_path]
            
            if stored == current_hash:
                logger.info(f'File "{rel_path}" verified OK.')
            else:
                logger.warning(f'File "{rel_path}" integrity failed!')
                simulate_alert_send("WARNING", rel_path, "hash mismatch")
        else:
            # New file not in baseline
            alert(f'Unknown file "{rel_path}" detected.')
            simulate_alert_send("ALERT", rel_path, "unknown file")
    except Exception as e:
        logger.error(f'Error checking file "{rel_path}": {e}')

def perform_full_scan():
    """Perform a full scan of all files in TARGET_DIR"""
    logger.info("Starting full integrity scan...")
    baseline = load_baseline()
    
    current_files = {}
    for root, _, files in os.walk(TARGET_DIR):
        for fname in files:
            rel = os.path.relpath(os.path.join(root, fname), TARGET_DIR)
            path = os.path.join(root, fname)
            try:
                current_files[rel] = sha256_file(path)
            except Exception as e:
                logger.warning(f"Failed hashing {rel}: {e}")
    
    baseline_files = set(baseline.keys())
    current_files_set = set(current_files.keys())
    
    # 1) files present & checked
    for f in sorted(baseline_files & current_files_set):
        stored = baseline[f]["hash"] if isinstance(baseline[f], dict) and "hash" in baseline[f] else baseline[f]
        now = current_files[f]
        if stored == now:
            logger.info(f'File "{f}" verified OK.')
        else:
            logger.warning(f'File "{f}" integrity failed!')
            simulate_alert_send("WARNING", f, "hash mismatch")
    
    # 2) new unknown files
    for f in sorted(current_files_set - baseline_files):
        alert(f'Unknown file "{f}" detected.')
        simulate_alert_send("ALERT", f, "unknown file")
    
    # 3) deleted/missing files
    for f in sorted(baseline_files - current_files_set):
        alert(f'File "{f}" missing (possibly deleted).')
        simulate_alert_send("ALERT", f, "file deleted")
    
    logger.info("Full integrity scan completed.")

class FileIntegrityHandler(FileSystemEventHandler):
    """Handler for file system events"""
    
    def __init__(self):
        super().__init__()
        self.last_check = {}
        self.debounce_time = 1  # seconds
    
    def should_check(self, filepath):
        """Debounce mechanism to avoid multiple checks for same file"""
        now = time.time()
        last = self.last_check.get(filepath, 0)
        if now - last > self.debounce_time:
            self.last_check[filepath] = now
            return True
        return False
    
    def on_modified(self, event):
        if event.is_directory:
            return
        if self.should_check(event.src_path):
            logger.info(f"Detected modification: {event.src_path}")
            check_file_integrity(event.src_path)
    
    def on_created(self, event):
        if event.is_directory:
            return
        if self.should_check(event.src_path):
            logger.info(f"Detected new file: {event.src_path}")
            check_file_integrity(event.src_path)
    
    def on_deleted(self, event):
        if event.is_directory:
            return
        logger.info(f"Detected deletion: {event.src_path}")
        check_file_integrity(event.src_path)
    
    def on_moved(self, event):
        if event.is_directory:
            return
        logger.info(f"Detected file move: {event.src_path} -> {event.dest_path}")
        check_file_integrity(event.src_path)
        check_file_integrity(event.dest_path)

def main():
    if not os.path.isdir(TARGET_DIR):
        print(f"Target dir {TARGET_DIR} missing. Create and add files.")
        return
    
    # Perform initial full scan
    perform_full_scan()
    
    # Set up file system monitoring
    event_handler = FileIntegrityHandler()
    observer = Observer()
    observer.schedule(event_handler, TARGET_DIR, recursive=True)
    observer.start()
    
    print(f"\n{'='*60}")
    print(f"Real-time monitoring started for: {TARGET_DIR}")
    print(f"Logs written to: {LOG_FILE}")
    print(f"Press Ctrl+C to stop monitoring")
    print(f"{'='*60}\n")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping monitoring...")
        observer.stop()
    
    observer.join()
    print("Monitoring stopped.")

if __name__ == "__main__":
    main()
