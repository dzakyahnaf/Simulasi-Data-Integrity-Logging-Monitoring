#!/usr/bin/env python3
import re
from datetime import datetime

LOG_FILE = "security.log"

# contoh line: [2025-10-30 13:26:02] WARNING: File "data.txt" integrity failed!
LINE_RE = re.compile(r'^\[(?P<ts>[\d\- :]+)\]\s+(?P<level>\w+):\s+(?P<msg>.+)$')
FILENAME_RE = re.compile(r'["\'](?P<fn>[^"\']+)["\']')

def parse_line(line):
    m = LINE_RE.match(line.strip())
    if not m:
        return None
    ts = datetime.strptime(m.group("ts"), "%Y-%m-%d %H:%M:%S")
    level = m.group("level")
    msg = m.group("msg")
    fn_m = FILENAME_RE.search(msg)
    filename = fn_m.group("fn") if fn_m else None
    return {"ts": ts, "level": level, "msg": msg, "file": filename}

def summarize():
    try:
        with open(LOG_FILE, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print("No log file found.")
        return

    last_status = {}  # file -> (level, ts)
    last_anomaly_ts = None
    for line in lines:
        p = parse_line(line)
        if not p or not p["file"]:
            continue
        fname = p["file"]
        last_status[fname] = (p["level"], p["ts"])
        if p["level"] in ("WARNING", "ALERT"):
            if last_anomaly_ts is None or p["ts"] > last_anomaly_ts:
                last_anomaly_ts = p["ts"]

    safe = sum(1 for v in last_status.values() if v[0] == "INFO")
    damaged = sum(1 for v in last_status.values() if v[0] == "WARNING")
    print("Summary:")
    print(f"  Jumlah file yang aman : {safe}")
    print(f"  Jumlah file rusak     : {damaged}")
    if last_anomaly_ts:
        print(f"  Waktu terakhir anomali: {last_anomaly_ts.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print("  Tidak ada anomali tercatat.")

if __name__ == "__main__":
    summarize()
