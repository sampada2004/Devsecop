# Simplified Monitoring for RITBuddy

This setup provides comprehensive monitoring for your RITBuddy RAG application, tracking:
- LLM response latency
- RAG pipeline stages performance
- Memory/CPU usage of local services (Ollama, FAISS)
- Custom events like "PDF processed," "Query answer failed," etc.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the Monitoring System

```bash
python run_monitoring.py
```

This will:
- Start collecting metrics in the background
- Store all metrics in CSV files in the `metrics` directory
- Log important events to the console and `monitoring.log` file

### 3. View Monitoring Results

When you stop the monitoring script (Ctrl+C), it will automatically:
- Generate an HTML report with all collected metrics
- Open the report in your default web browser

## Monitoring Components

### LLM Response Metrics
- Response time tracking by model and operation
- Success/failure status recording

### RAG Pipeline Metrics
- Latency for each stage (embedding, vector search, etc.)
- Success/failure status for each stage
- Error types by stage

### Resource Usage
- Memory usage for app and Ollama
- CPU usage for app and Ollama

### Custom Events
- Timestamps of events like "PDF processed", "embedding generated", etc.
- Success/failure status for each event

## Adding Custom Metrics

You can add custom metrics to your application by importing from the `simple_monitoring.py` module:

```python
from simple_monitoring import record_event, monitor_rag_stage, monitor_llm

# Record a custom event
record_event("document_indexed", "success")

# Monitor a RAG pipeline stage
@monitor_rag_stage(stage="my_custom_stage")
def my_function():
    # Your code here
    pass

# Monitor LLM operations
@monitor_llm(model="mistral", operation="classification")
def call_llm_for_classification():
    # Your code here
    pass
```

## Troubleshooting

If metrics aren't being recorded:
1. Check that the `metrics` directory exists and is writable
2. Look at the `monitoring.log` file for any errors
3. Restart the Flask application to ensure decorators are applied

## Advanced Customization

For advanced customization, you can modify:
- `simple_monitoring.py` - Change the metrics collection logic
- Add additional metrics or custom reports as needed
- Implement data visualization using Python libraries like matplotlib or plotly
