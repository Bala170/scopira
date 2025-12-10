import socket
import sys

def test_port(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        result = s.connect_ex((host, port))
        s.close()
        return result == 0
    except:
        return False

def test_simple_server():
    import http.server
    import socketserver
    
    PORT = 5001
    
    try:
        with socketserver.TCPServer(("", PORT), http.server.SimpleHTTPRequestHandler) as httpd:
            print(f"Simple server running at http://localhost:{PORT}")
            httpd.serve_forever()
    except Exception as e:
        print(f"Error starting simple server: {e}")

if __name__ == "__main__":
    print("Testing network connectivity...")
    
    # Test if port 5000 is accessible
    if test_port("localhost", 5000):
        print("Port 5000 is accessible")
    else:
        print("Port 5000 is not accessible")
    
    # Start a simple test server
    test_simple_server()