from flask import Flask, request, jsonify
from flask_cors import CORS
import rag
import time
from monitoring import start_metrics_server, monitor_resources, QUERY_PROCESSING_TIME, record_event

app = Flask(__name__)
CORS(app)

# Start Prometheus metrics server
start_metrics_server(port=8000)

# Start resource monitoring in background
monitor_thread = monitor_resources(interval=5)

@app.route('/ask', methods=['POST'])
def ask():
    start_time = time.time()
    data = request.json
    question = data.get('question', '')
    print(f"Received question: {question}")
    
    if not question:
        record_event("api_request", "failure")
        return jsonify({'error': 'No question provided'}), 400
    
    try:
        # Track the query processing time using Prometheus
        with QUERY_PROCESSING_TIME.labels(query_type="api_request").time():
            answer = rag.ask_question(question)
        
        # Record successful API request
        record_event("api_request", "success")
        
        # Calculate and log total response time
        response_time = time.time() - start_time
        print(f"Total response time: {response_time:.2f} seconds")
        
        return jsonify({
            'answer': answer,
            'response_time_seconds': response_time
        })
    
    except Exception as e:
        # Record failed API request
        record_event("api_request", "failure")
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
