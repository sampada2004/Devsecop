import time
from functools import wraps
from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
import psutil
import threading

# Initialize Prometheus metrics
# LLM Response metrics
LLM_LATENCY = Histogram('llm_response_time_seconds', 'Time spent processing LLM responses',
                        ['model', 'operation'])
LLM_REQUESTS = Counter('llm_requests_total', 'Total number of LLM requests',
                      ['model', 'operation', 'status'])

# RAG Pipeline metrics
RAG_STAGE_LATENCY = Histogram('rag_stage_time_seconds', 'Time spent in each RAG pipeline stage',
                             ['stage'])
RAG_STAGE_FAILURES = Counter('rag_stage_failures_total', 'Total number of RAG pipeline stage failures',
                           ['stage', 'error_type'])
RAG_STAGE_SUCCESS = Counter('rag_stage_success_total', 'Total number of successful RAG pipeline stage executions',
                          ['stage'])

# Resource usage metrics
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes', ['service'])
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage', ['service'])

# Custom event metrics
CUSTOM_EVENTS = Counter('custom_events_total', 'Count of custom application events',
                       ['event_type', 'status'])

# Query performance metrics
QUERY_PROCESSING_TIME = Summary('query_processing_seconds', 'Time spent processing queries',
                               ['query_type'])

def start_metrics_server(port=8000):
    """Start the Prometheus metrics server on the specified port"""
    start_http_server(port)
    print(f"Metrics server started on port {port}")

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
            MEMORY_USAGE.labels(service='app').set(memory_info.rss)
            
            # CPU usage for the current process
            CPU_USAGE.labels(service='app').set(process.cpu_percent(interval=0.1))
            
            # Try to get Ollama process if running locally
            try:
                for proc in psutil.process_iter(['name', 'cmdline']):
                    proc_name = proc.info.get('name', '')
                    proc_cmdline = proc.info.get('cmdline', [])
                    
                    # Check if Ollama is in the process name
                    name_match = proc_name and 'ollama' in proc_name.lower()
                    
                    # Check if Ollama is in any command line argument
                    cmd_match = False
                    if proc_cmdline:
                        cmd_match = any('ollama' in cmd.lower() for cmd in proc_cmdline if isinstance(cmd, str))
                    
                    if name_match or cmd_match:
                        MEMORY_USAGE.labels(service='ollama').set(proc.memory_info().rss)
                        CPU_USAGE.labels(service='ollama').set(proc.cpu_percent(interval=0.1))
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
                LLM_REQUESTS.labels(model=model, operation=operation, status="success").inc()
                return result
            except Exception as e:
                LLM_REQUESTS.labels(model=model, operation=operation, status="failure").inc()
                raise e
            finally:
                LLM_LATENCY.labels(model=model, operation=operation).observe(time.time() - start_time)
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
                RAG_STAGE_SUCCESS.labels(stage=stage).inc()
                return result
            except Exception as e:
                RAG_STAGE_FAILURES.labels(stage=stage, error_type=type(e).__name__).inc()
                raise e
            finally:
                RAG_STAGE_LATENCY.labels(stage=stage).observe(time.time() - start_time)
        return wrapper
    return decorator

# Function to record custom events
def record_event(event_type, status="success"):
    """
    Record a custom application event
    Args:
        event_type: Type of event (e.g., "pdf_processed", "query_answered")
        status: Status of the event (e.g., "success", "failure")
    """
    CUSTOM_EVENTS.labels(event_type=event_type, status=status).inc()

# Function to measure query processing time
def measure_query(query_type="general"):
    """
    Decorator to measure query processing time
    Args:
        query_type: Type of query being processed
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with QUERY_PROCESSING_TIME.labels(query_type=query_type).time():
                return func(*args, **kwargs)
        return wrapper
    return decorator
