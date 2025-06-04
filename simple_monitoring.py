import time
import json
import os
import threading
import psutil
from functools import wraps
from datetime import datetime
import csv
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("monitoring.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("monitoring")

# Metrics storage
METRICS_DIR = "metrics"
os.makedirs(METRICS_DIR, exist_ok=True)

# Metric files
LLM_LATENCY_FILE = os.path.join(METRICS_DIR, "llm_latency.csv")
RAG_STAGE_LATENCY_FILE = os.path.join(METRICS_DIR, "rag_stage_latency.csv")
RESOURCE_USAGE_FILE = os.path.join(METRICS_DIR, "resource_usage.csv")
CUSTOM_EVENTS_FILE = os.path.join(METRICS_DIR, "custom_events.csv")
QUERY_PROCESSING_FILE = os.path.join(METRICS_DIR, "query_processing.csv")

# Initialize CSV files with headers
def init_csv_files():
    if not os.path.exists(LLM_LATENCY_FILE):
        with open(LLM_LATENCY_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'model', 'operation', 'latency_seconds', 'status'])
    
    if not os.path.exists(RAG_STAGE_LATENCY_FILE):
        with open(RAG_STAGE_LATENCY_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'stage', 'latency_seconds', 'status'])
    
    if not os.path.exists(RESOURCE_USAGE_FILE):
        with open(RESOURCE_USAGE_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'service', 'memory_bytes', 'cpu_percent'])
    
    if not os.path.exists(CUSTOM_EVENTS_FILE):
        with open(CUSTOM_EVENTS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'event_type', 'status'])
    
    if not os.path.exists(QUERY_PROCESSING_FILE):
        with open(QUERY_PROCESSING_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'query_type', 'processing_time_seconds'])

# Record LLM latency
def record_llm_latency(model, operation, latency, status="success"):
    timestamp = datetime.now().isoformat()
    with open(LLM_LATENCY_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, model, operation, latency, status])
    logger.info(f"LLM Latency: {model} - {operation} - {latency:.4f}s - {status}")

# Record RAG stage latency
def record_rag_stage_latency(stage, latency, status="success"):
    timestamp = datetime.now().isoformat()
    with open(RAG_STAGE_LATENCY_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, stage, latency, status])
    logger.info(f"RAG Stage Latency: {stage} - {latency:.4f}s - {status}")

# Record resource usage
def record_resource_usage(service, memory_bytes, cpu_percent):
    timestamp = datetime.now().isoformat()
    with open(RESOURCE_USAGE_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, service, memory_bytes, cpu_percent])
    logger.debug(f"Resource Usage: {service} - Memory: {memory_bytes/1024/1024:.2f}MB - CPU: {cpu_percent:.2f}%")

# Record custom event
def record_event(event_type, status="success"):
    timestamp = datetime.now().isoformat()
    with open(CUSTOM_EVENTS_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, event_type, status])
    logger.info(f"Custom Event: {event_type} - {status}")

# Record query processing time
def record_query_processing(query_type, processing_time):
    timestamp = datetime.now().isoformat()
    with open(QUERY_PROCESSING_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, query_type, processing_time])
    logger.info(f"Query Processing: {query_type} - {processing_time:.4f}s")

# Monitor resources
def monitor_resources(interval=5):
    """
    Start a background thread to monitor system resources
    Args:
        interval: Time in seconds between measurements
    """
    def _monitor_resources():
        while True:
            # Memory usage for the current process
            process = psutil.Process()
            memory_info = process.memory_info()
            cpu_percent = process.cpu_percent(interval=0.1)
            
            record_resource_usage('app', memory_info.rss, cpu_percent)
            
            # Try to get Ollama process if running locally
            try:
                for proc in psutil.process_iter(['name', 'cmdline']):
                    proc_name = proc.info.get('name', '')
                    proc_cmdline = proc.info.get('cmdline', [])
                    
                    if proc_name and 'ollama' in proc_name.lower():
                        ollama_memory = proc.memory_info().rss
                        ollama_cpu = proc.cpu_percent(interval=0.1)
                        record_resource_usage('ollama', ollama_memory, ollama_cpu)
                    elif proc_cmdline and any('ollama' in cmd.lower() for cmd in proc_cmdline if isinstance(cmd, str)):
                        ollama_memory = proc.memory_info().rss
                        ollama_cpu = proc.cpu_percent(interval=0.1)
                        record_resource_usage('ollama', ollama_memory, ollama_cpu)
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess, AttributeError, TypeError):
                pass
            
            time.sleep(interval)
    
    thread = threading.Thread(target=_monitor_resources, daemon=True)
    thread.start()
    return thread

# Decorator for monitoring LLM operations
def monitor_llm(model="mistral", operation="generation"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                latency = time.time() - start_time
                record_llm_latency(model, operation, latency, "success")
                return result
            except Exception as e:
                latency = time.time() - start_time
                record_llm_latency(model, operation, latency, "failure")
                raise e
        return wrapper
    return decorator

# Decorator for monitoring RAG pipeline stages
def monitor_rag_stage(stage):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                latency = time.time() - start_time
                record_rag_stage_latency(stage, latency, "success")
                return result
            except Exception as e:
                latency = time.time() - start_time
                record_rag_stage_latency(stage, latency, "failure")
                raise e
        return wrapper
    return decorator

# Function to measure query processing time
def measure_query(query_type="general"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            processing_time = time.time() - start_time
            record_query_processing(query_type, processing_time)
            return result
        return wrapper
    return decorator

# Initialize the monitoring system
def start_monitoring():
    init_csv_files()
    monitor_thread = monitor_resources()
    logger.info("Monitoring system started")
    return monitor_thread

# Generate a simple HTML report
def generate_html_report():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>RITBuddy Monitoring Report</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            tr:nth-child(even) { background-color: #f9f9f9; }
            .metric-section { margin-bottom: 30px; }
        </style>
    </head>
    <body>
        <h1>RITBuddy Monitoring Report</h1>
        <p>Generated at: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
        
        <div class="metric-section">
            <h2>LLM Response Latency</h2>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>Model</th>
                    <th>Operation</th>
                    <th>Latency (s)</th>
                    <th>Status</th>
                </tr>
    """
    
    # Add LLM latency data
    if os.path.exists(LLM_LATENCY_FILE):
        with open(LLM_LATENCY_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for i, row in enumerate(reader):
                if i >= 100:  # Limit to last 100 entries
                    break
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td></tr>"
    
    html += """
            </table>
        </div>
        
        <div class="metric-section">
            <h2>RAG Pipeline Stage Latency</h2>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>Stage</th>
                    <th>Latency (s)</th>
                    <th>Status</th>
                </tr>
    """
    
    # Add RAG stage latency data
    if os.path.exists(RAG_STAGE_LATENCY_FILE):
        with open(RAG_STAGE_LATENCY_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for i, row in enumerate(reader):
                if i >= 100:  # Limit to last 100 entries
                    break
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
    
    html += """
            </table>
        </div>
        
        <div class="metric-section">
            <h2>Custom Events</h2>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>Event Type</th>
                    <th>Status</th>
                </tr>
    """
    
    # Add custom events data
    if os.path.exists(CUSTOM_EVENTS_FILE):
        with open(CUSTOM_EVENTS_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for i, row in enumerate(reader):
                if i >= 100:  # Limit to last 100 entries
                    break
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    
    html += """
            </table>
        </div>
        
        <div class="metric-section">
            <h2>Query Processing Time</h2>
            <table>
                <tr>
                    <th>Timestamp</th>
                    <th>Query Type</th>
                    <th>Processing Time (s)</th>
                </tr>
    """
    
    # Add query processing data
    if os.path.exists(QUERY_PROCESSING_FILE):
        with open(QUERY_PROCESSING_FILE, 'r') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            for i, row in enumerate(reader):
                if i >= 100:  # Limit to last 100 entries
                    break
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
    
    html += """
            </table>
        </div>
    </body>
    </html>
    """
    
    with open("monitoring_report.html", "w") as f:
        f.write(html)
    
    return "monitoring_report.html"

if __name__ == "__main__":
    start_monitoring()
    print("Monitoring started. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Generating report...")
        report_file = generate_html_report()
        print(f"Report generated: {report_file}")
