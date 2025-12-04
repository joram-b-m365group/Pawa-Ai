"""Simple HTTP server for Genius AI Dashboard"""
import http.server
import socketserver
import os

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

os.chdir(DIRECTORY)

Handler = http.server.SimpleHTTPRequestHandler

print("=" * 70)
print("GENIUS AI DASHBOARD SERVER")
print("=" * 70)
print(f"\nServer running at: http://localhost:{PORT}")
print(f"\nOpen this URL in your browser:")
print(f"  http://localhost:{PORT}/frontend/dashboard.html")
print("\nPress Ctrl+C to stop")
print("=" * 70)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()
