#!/usr/bin/env python3
from flask import Flask, render_template_string
import log_reader

app = Flask(__name__)

TEMPLATE = """
<!doctype html>
<title>Monitoring Integritas - Mini</title>
<h1>Monitoring Integritas File</h1>
<ul>
  <li>Jumlah file aman: {{ safe }}</li>
  <li>Jumlah file rusak: {{ damaged }}</li>
  <li>Waktu terakhir anomali: {{ last_anomaly }}</li>
</ul>
<h2>Log (last 200 lines)</h2>
<pre>{{ logs }}</pre>
"""

def get_stats_and_logs():
    # reuse log_reader.parse_line
    lines = []
    try:
        with open("security.log","r") as f:
            lines = f.readlines()[-200:]
    except:
        lines = []
    # generate stats using log_reader logic
    last_status = {}
    last_anomaly_ts = None
    for line in lines:
        p = log_reader.parse_line(line)
        if not p or not p["file"]:
            continue
        last_status[p["file"]] = (p["level"], p["ts"])
        if p["level"] in ("WARNING","ALERT"):
            if last_anomaly_ts is None or p["ts"] > last_anomaly_ts:
                last_anomaly_ts = p["ts"]
    safe = sum(1 for v in last_status.values() if v[0]=="INFO")
    damaged = sum(1 for v in last_status.values() if v[0]=="WARNING")
    last_anom = last_anomaly_ts.strftime("%Y-%m-%d %H:%M:%S") if last_anomaly_ts else "Tidak ada"
    return safe, damaged, last_anom, "".join(lines)

@app.route("/")
def index():
    safe, damaged, last_anom, logs = get_stats_and_logs()
    return render_template_string(TEMPLATE, safe=safe, damaged=damaged, last_anomaly=last_anom, logs=logs)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
