from http.server import BaseHTTPRequestHandler
import json
from api import app  # Import your Flask app

def handler(event, context):
    """Handle the Netlify function request"""
    # Convert Netlify event to Flask request
    path = event.get('path', '')
    method = event.get('httpMethod', 'GET')
    headers = event.get('headers', {})
    body = event.get('body', '')
    
    # Create a mock request environment
    environ = {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'QUERY_STRING': event.get('queryStringParameters', ''),
        'CONTENT_TYPE': headers.get('content-type', ''),
        'CONTENT_LENGTH': str(len(body)),
        'wsgi.input': body,
        'wsgi.url_scheme': 'https',
        'SERVER_NAME': 'localhost',
        'SERVER_PORT': '443',
    }
    
    # Call your Flask app
    response = app(environ, lambda status, headers: None)
    
    # Convert Flask response to Netlify response
    return {
        'statusCode': response.status_code,
        'headers': dict(response.headers),
        'body': response.get_data(as_text=True)
    } 