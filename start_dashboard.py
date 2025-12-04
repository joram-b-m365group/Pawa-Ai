"""
Simple HTTP server to serve the Genius AI dashboard
"""
import http.server
import socketserver
import webbrowser
import os
from pathlib import Path

PORT = 8000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent), **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def main():
    print("=" * 70)
    print("GENIUS AI - Dashboard Server")
    print("=" * 70)
    print(f"\nStarting server on port {PORT}...")
    print(f"Dashboard URL: http://localhost:{PORT}/frontend/dashboard.html")
    print("\nOpening dashboard in your browser...")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 70)

    # Start server
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        # Open browser
        webbrowser.open(f'http://localhost:{PORT}/frontend/dashboard.html')

        # Serve forever
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\nShutting down server...")
            httpd.shutdown()

if __name__ == "__main__":
    main()
