from http.server import BaseHTTPRequestHandler
from main import main

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        main()
        self.send_response(200)
        self.end_headers()
        return

    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Bot is running!'.encode())
        return