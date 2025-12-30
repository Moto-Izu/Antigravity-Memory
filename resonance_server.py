import http.server
import socketserver
import os
import time
import json
import threading

PORT = 8000
LOG_FILE = "../resonance_log.jsonl" # Relative to public/ dir served or handled carefully

class NeuralHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/public/index.html'
        elif self.path.startswith('/public/'):
            # allow normal serving
            pass
        elif self.path == '/stream':
            self.handle_stream()
            return
        
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

    def handle_stream(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/event-stream')
        self.send_header('Cache-Control', 'no-cache')
        self.send_header('Connection', 'keep-alive')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

        log_path = os.path.abspath("resonance_log.jsonl")
        
        # Initial read: send last 10 lines as 'history'
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                for line in lines[-20:]:
                    if line.strip():
                        self.wfile.write(f"data: {line.strip()}\n\n".encode('utf-8'))
        except FileNotFoundError:
            pass

        # Tail logic
        try:
            f = open(log_path, 'r', encoding='utf-8')
            f.seek(0, 2) # End of file
            
            while True:
                line = f.readline()
                if line:
                    self.wfile.write(f"data: {line.strip()}\n\n".encode('utf-8'))
                    self.wfile.flush()
                else:
                    time.sleep(0.5)
        except Exception as e:
            print(f"Connection closed: {e}")
            try:
                f.close()
            except:
                pass

print(f"Neural Interface Active @ http://localhost:{PORT}")
print(f"Monitoring: resonance_log.jsonl")

# Ensure proper binding
with socketserver.TCPServer(("", PORT), NeuralHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
