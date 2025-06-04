import time
import random
from prometheus_client import Counter, Histogram, Gauge, Summary, start_http_server
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

# Simulate RAG pipeline stages
def simulate_embedding_generation():
    # Simulate embedding generation with random latency
    latency = random.uniform(0.1, 0.5)
    time.sleep(latency)
    
    # Record metrics
    RAG_STAGE_LATENCY.labels(stage="embedding_generation").observe(latency)
    RAG_STAGE_SUCCESS.labels(stage="embedding_generation").inc()
    
    # Occasionally simulate failures
    if random.random() < 0.05:  # 5% chance of failure
        RAG_STAGE_FAILURES.labels(stage="embedding_generation", error_type="timeout").inc()
        CUSTOM_EVENTS.labels(event_type="embedding_generated", status="failure").inc()
    else:
        CUSTOM_EVENTS.labels(event_type="embedding_generated", status="success").inc()

def simulate_vector_search():
    # Simulate vector search with random latency
    latency = random.uniform(0.05, 0.2)
    time.sleep(latency)
    
    # Record metrics
    RAG_STAGE_LATENCY.labels(stage="vector_search").observe(latency)
    RAG_STAGE_SUCCESS.labels(stage="vector_search").inc()
    
    # Occasionally simulate failures
    if random.random() < 0.03:  # 3% chance of failure
        RAG_STAGE_FAILURES.labels(stage="vector_search", error_type="index_error").inc()
        CUSTOM_EVENTS.labels(event_type="vector_search_completed", status="failure").inc()
    else:
        CUSTOM_EVENTS.labels(event_type="vector_search_completed", status="success").inc()

def simulate_llm_generation():
    # Simulate LLM generation with random latency
    latency = random.uniform(0.5, 2.0)
    time.sleep(latency)
    
    # Record metrics
    LLM_LATENCY.labels(model="mistral", operation="generation").observe(latency)
    
    # Occasionally simulate failures
    if random.random() < 0.02:  # 2% chance of failure
        LLM_REQUESTS.labels(model="mistral", operation="generation", status="failure").inc()
        CUSTOM_EVENTS.labels(event_type="llm_response_generated", status="failure").inc()
    else:
        LLM_REQUESTS.labels(model="mistral", operation="generation", status="success").inc()
        CUSTOM_EVENTS.labels(event_type="llm_response_generated", status="success").inc()

def simulate_pdf_processing():
    # Simulate PDF processing
    CUSTOM_EVENTS.labels(event_type="pdf_processed", status="success").inc()

def simulate_resource_usage():
    while True:
        # Simulate memory usage (100-500 MB)
        memory_usage = random.randint(100_000_000, 500_000_000)
        MEMORY_USAGE.labels(service="app").set(memory_usage)
        
        # Simulate Ollama memory usage (1-2 GB)
        ollama_memory = random.randint(1_000_000_000, 2_000_000_000)
        MEMORY_USAGE.labels(service="ollama").set(ollama_memory)
        
        # Simulate CPU usage (5-30%)
        cpu_usage = random.uniform(5, 30)
        CPU_USAGE.labels(service="app").set(cpu_usage)
        
        # Simulate Ollama CPU usage (10-80%)
        ollama_cpu = random.uniform(10, 80)
        CPU_USAGE.labels(service="ollama").set(ollama_cpu)
        
        time.sleep(2)

def simulate_query():
    # Simulate a complete query
    with QUERY_PROCESSING_TIME.labels(query_type="rag_query").time():
        simulate_embedding_generation()
        simulate_vector_search()
        simulate_llm_generation()

def main():
    # Start the Prometheus metrics server
    start_http_server(8000)
    print("Metrics server started on port 8000")
    
    # Start resource usage simulation in a background thread
    resource_thread = threading.Thread(target=simulate_resource_usage, daemon=True)
    resource_thread.start()
    
    # Simulate initial PDF processing
    simulate_pdf_processing()
    
    print("Starting simulation of RAG queries...")
    print("Press Ctrl+C to stop")
    
    try:
        query_count = 0
        while True:
            # Simulate a query every 3-8 seconds
            time.sleep(random.uniform(3, 8))
            query_count += 1
            print(f"Simulating query #{query_count}")
            simulate_query()
    except KeyboardInterrupt:
        print("Simulation stopped")

if __name__ == "__main__":
    main()
