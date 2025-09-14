#!/usr/bin/env python3
"""
Simple CORS proxy for local AI servers.
This proxy adds CORS headers to allow web pages to access your local AI server.
"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import json
import sys

# Configuration
LOCAL_AI_URL = "http://127.0.0.1:1234"  # Your AI server URL
PROXY_PORT = 8000  # Port for this proxy server

class CORSProxyHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        """Send CORS headers to allow cross-origin requests"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.send_header('Access-Control-Max-Age', '3600')
    
    def do_OPTIONS(self):
        """Handle preflight OPTIONS requests"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()
    
    def do_POST(self):
        """Proxy POST requests to the AI server"""
        try:
            # Read the request body
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            # Forward the request to the AI server
            headers = {'Content-Type': 'application/json'}
            if 'Authorization' in self.headers:
                headers['Authorization'] = self.headers['Authorization']
                
            response = requests.post(
                f"{LOCAL_AI_URL}{self.path}",
                data=post_data,
                headers=headers,
                timeout=60
            )
            
            # Send response back with CORS headers
            self.send_response(response.status_code)
            self._send_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(response.content)
            
        except requests.exceptions.ConnectionError:
            self.send_response(503)
            self._send_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({
                "error": f"Cannot connect to AI server at {LOCAL_AI_URL}. Please check if it's running."
            })
            self.wfile.write(error_response.encode())
            
        except Exception as e:
            self.send_response(500)
            self._send_cors_headers()
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            error_response = json.dumps({"error": str(e)})
            self.wfile.write(error_response.encode())

if __name__ == '__main__':
    print(f"Starting CORS proxy server on port {PROXY_PORT}")
    print(f"Proxying requests to: {LOCAL_AI_URL}")
    print(f"Update your HTML file to use: http://127.0.0.1:{PROXY_PORT}/v1/chat/completions")
    print("Press Ctrl+C to stop")
    
    server = HTTPServer(('127.0.0.1', PROXY_PORT), CORSProxyHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down proxy server...")
        server.server_close() 