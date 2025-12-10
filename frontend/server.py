import http.server
import socketserver
import os

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Set the directory to the current directory
        super().__init__(*args, directory=os.getcwd(), **kwargs)
    
    def translate_path(self, path):
        # Handle the root path to serve index.html
        if path == '/' or path == '/index.html':
            return os.path.join(os.getcwd(), 'index.html')
        # For other paths, use the default behavior
        return super().translate_path(path)

PORT = 8000

# Change to the frontend directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"Serving frontend at http://localhost:{PORT}")
    httpd.serve_forever()