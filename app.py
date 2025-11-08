#!/usr/bin/env python3
from flask import Flask, render_template_string, jsonify
import log_reader
import os
from datetime import datetime

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🔒 Security Monitoring Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css">
    <style>
        :root {
            --primary-dark: #1a1d29;
            --secondary-dark: #252936;
            --accent-blue: #4facfe;
            --accent-green: #00f2c3;
            --text-light: #e1e8ed;
            --text-muted: #8899a6;
            --danger-red: #ff6b6b;
            --warning-orange: #ffa502;
            --success-green: #2ecc71;
        }
        
        body {
            background: linear-gradient(135deg, var(--primary-dark) 0%, #2d3561 100%);
            color: var(--text-light);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
            padding: 20px 0;
        }
        
        .dashboard-header {
            background: linear-gradient(135deg, rgba(74, 172, 254, 0.2) 0%, rgba(0, 242, 195, 0.2) 100%);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            border: 1px solid rgba(74, 172, 254, 0.3);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        }
        
        .dashboard-header h1 {
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 10px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-green));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stats-card {
            background: var(--secondary-dark);
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stats-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.3);
        }
        
        .stats-icon {
            font-size: 2.5rem;
            margin-bottom: 15px;
            display: inline-block;
        }
        
        .stats-value {
            font-size: 3rem;
            font-weight: 700;
            margin: 10px 0;
            display: block;
        }
        
        .stats-label {
            color: var(--text-muted);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .safe-card {
            border-left: 4px solid var(--success-green);
        }
        
        .damaged-card {
            border-left: 4px solid var(--danger-red);
        }
        
        .anomaly-card {
            border-left: 4px solid var(--warning-orange);
        }
        
        .log-container {
            background: var(--secondary-dark);
            border-radius: 15px;
            padding: 25px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
            max-height: 600px;
            overflow-y: auto;
        }
        
        .log-container h2 {
            color: var(--accent-blue);
            margin-bottom: 20px;
            font-size: 1.5rem;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .log-entry {
            padding: 10px 15px;
            margin-bottom: 8px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            font-size: 0.9rem;
            border-left: 3px solid transparent;
            transition: all 0.2s ease;
        }
        
        .log-entry:hover {
            background: rgba(255, 255, 255, 0.05);
            transform: translateX(5px);
        }
        
        .log-info {
            border-left-color: var(--success-green);
            background: rgba(46, 204, 113, 0.1);
        }
        
        .log-warning {
            border-left-color: var(--warning-orange);
            background: rgba(255, 165, 2, 0.1);
        }
        
        .log-alert {
            border-left-color: var(--danger-red);
            background: rgba(255, 107, 107, 0.1);
        }
        
        .badge-custom {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .auto-refresh {
            background: rgba(74, 172, 254, 0.2);
            border: 1px solid var(--accent-blue);
            color: var(--accent-blue);
            padding: 10px 20px;
            border-radius: 25px;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        
        .auto-refresh:hover {
            background: var(--accent-blue);
            color: white;
        }
        
        .pulse {
            animation: pulse 2s infinite;
        }
        
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        
        .last-update {
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 10px;
        }
        
        /* Scrollbar styling */
        .log-container::-webkit-scrollbar {
            width: 8px;
        }
        
        .log-container::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
        }
        
        .log-container::-webkit-scrollbar-thumb {
            background: var(--accent-blue);
            border-radius: 10px;
        }
        
        .log-container::-webkit-scrollbar-thumb:hover {
            background: var(--accent-green);
        }
        
        .status-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-right: 8px;
            animation: blink 2s infinite;
        }
        
        .status-active {
            background: var(--success-green);
            box-shadow: 0 0 10px var(--success-green);
        }
        
        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.3; }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="dashboard-header text-center">
            <h1><i class="bi bi-shield-lock-fill"></i> Security Monitoring Dashboard</h1>
            <p class="mb-0">
                <span class="status-indicator status-active"></span>
                Real-time File Integrity Monitoring System
            </p>
            <p class="last-update">Last Update: <span id="lastUpdate">{{ current_time }}</span></p>
        </div>
        
        <!-- Stats Cards -->
        <div class="row mb-4">
            <div class="col-md-4">
                <div class="stats-card safe-card text-center">
                    <i class="bi bi-check-circle-fill stats-icon text-success"></i>
                    <div class="stats-label">Files Verified</div>
                    <span class="stats-value text-success" id="safeCount">{{ safe }}</span>
                    <div class="text-muted">No integrity issues detected</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stats-card damaged-card text-center">
                    <i class="bi bi-exclamation-triangle-fill stats-icon text-danger"></i>
                    <div class="stats-label">Compromised Files</div>
                    <span class="stats-value text-danger" id="damagedCount">{{ damaged }}</span>
                    <div class="text-muted">Integrity verification failed</div>
                </div>
            </div>
            <div class="col-md-4">
                <div class="stats-card anomaly-card text-center">
                    <i class="bi bi-clock-history stats-icon text-warning"></i>
                    <div class="stats-label">Last Anomaly</div>
                    <span class="stats-value" style="font-size: 1.5rem;" id="lastAnomaly">
                        {{ last_anomaly }}
                    </span>
                    <div class="text-muted">Most recent security event</div>
                </div>
            </div>
        </div>
        
        <!-- Controls -->
        <div class="text-center mb-4">
            <button class="btn auto-refresh" onclick="toggleAutoRefresh()">
                <i class="bi bi-arrow-clockwise"></i> 
                <span id="refreshStatus">Auto-Refresh: ON</span>
            </button>
            <button class="btn auto-refresh ms-2" onclick="manualRefresh()">
                <i class="bi bi-arrow-repeat"></i> Refresh Now
            </button>
        </div>
        
        <!-- Logs -->
        <div class="log-container">
            <h2>
                <i class="bi bi-file-text-fill"></i> 
                Security Logs
                <span class="badge badge-custom bg-primary ms-2">Last 200 entries</span>
            </h2>
            <div id="logContent">
                {{ logs_html|safe }}
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let autoRefresh = true;
        let refreshInterval;
        
        function updateDashboard() {
            fetch('/api/stats')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('safeCount').textContent = data.safe;
                    document.getElementById('damagedCount').textContent = data.damaged;
                    document.getElementById('lastAnomaly').textContent = data.last_anomaly;
                    document.getElementById('logContent').innerHTML = data.logs_html;
                    document.getElementById('lastUpdate').textContent = new Date().toLocaleString();
                })
                .catch(error => console.error('Error fetching stats:', error));
        }
        
        function toggleAutoRefresh() {
            autoRefresh = !autoRefresh;
            const statusText = document.getElementById('refreshStatus');
            
            if (autoRefresh) {
                statusText.textContent = 'Auto-Refresh: ON';
                refreshInterval = setInterval(updateDashboard, 5000); // Refresh every 5 seconds
            } else {
                statusText.textContent = 'Auto-Refresh: OFF';
                clearInterval(refreshInterval);
            }
        }
        
        function manualRefresh() {
            updateDashboard();
        }
        
        // Start auto-refresh on page load
        if (autoRefresh) {
            refreshInterval = setInterval(updateDashboard, 5000);
        }
        
        // Scroll to bottom of logs
        const logContainer = document.querySelector('.log-container');
        if (logContainer) {
            logContainer.scrollTop = logContainer.scrollHeight;
        }
    </script>
</body>
</html>
"""

def format_log_line(line):
    """Format log line with HTML styling based on level"""
    line = line.strip()
    if not line:
        return ""
    
    # Determine log level
    if "INFO:" in line:
        level_class = "log-info"
        badge = '<span class="badge badge-custom bg-success">INFO</span>'
    elif "WARNING:" in line:
        level_class = "log-warning"
        badge = '<span class="badge badge-custom bg-warning">WARNING</span>'
    elif "ALERT:" in line:
        level_class = "log-alert"
        badge = '<span class="badge badge-custom bg-danger">ALERT</span>'
    else:
        level_class = ""
        badge = ""
    
    # Extract timestamp and message
    if "]" in line:
        parts = line.split("]", 1)
        timestamp = parts[0] + "]"
        message = parts[1] if len(parts) > 1 else ""
        
        # Highlight filenames in quotes
        import re
        message = re.sub(r'"([^"]+)"', r'<strong>"\1"</strong>', message)
        
        return f'<div class="log-entry {level_class}">{badge} <span class="text-muted">{timestamp}</span> {message}</div>'
    
    return f'<div class="log-entry {level_class}">{line}</div>'

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
    last_anom = last_anomaly_ts.strftime("%Y-%m-%d %H:%M:%S") if last_anomaly_ts else "No anomalies"
    
    # Format logs with HTML
    logs_html = "\n".join([format_log_line(line) for line in lines])
    
    return safe, damaged, last_anom, logs_html

@app.route("/")
def index():
    safe, damaged, last_anom, logs_html = get_stats_and_logs()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return render_template_string(
        TEMPLATE, 
        safe=safe, 
        damaged=damaged, 
        last_anomaly=last_anom, 
        logs_html=logs_html,
        current_time=current_time
    )

@app.route("/api/stats")
def api_stats():
    """API endpoint for AJAX updates"""
    safe, damaged, last_anom, logs_html = get_stats_and_logs()
    return jsonify({
        "safe": safe,
        "damaged": damaged,
        "last_anomaly": last_anom,
        "logs_html": logs_html
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)
