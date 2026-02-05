"""Tiny HTTP server to receive JSON data from browser."""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os

OUTPUT_DIR = r"C:\Users\user\.openclaw\workspace\tmp"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length)
        filepath = os.path.join(OUTPUT_DIR, "all_blocks.json")
        with open(filepath, 'wb') as f:
            f.write(data)
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        self.wfile.write(f"Saved {length} bytes".encode())
        print(f"Received {length} bytes, saved to {filepath}")
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        print(format % args)

server = HTTPServer(('127.0.0.1', 19876), Handler)
print("Listening on http://127.0.0.1:19876")
server.handle_request()  # Handle one request then exit
print("Done!")
