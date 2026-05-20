from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import os
import sys

# Add root project path to import database manager
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.db_manager import get_connection

class AnalyticsHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/analytics':
            conn = get_connection()
            cursor = conn.cursor()
            
            # Total focus time
            cursor.execute("SELECT SUM(duration_minutes) FROM sessions")
            total_mins = cursor.fetchone()[0] or 0
            
            # Sessions per day
            cursor.execute("SELECT date(completed_at), SUM(duration_minutes) FROM sessions GROUP BY date(completed_at) ORDER BY completed_at DESC LIMIT 7")
            data = cursor.fetchall()
            conn.close()
            
            response = {
                "total_mins": total_mins,
                "chart_data": data
            }
            
            self._set_headers(200)
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers(404)

    def do_POST(self):
        if self.path == '/sessions':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            duration = data.get('duration_minutes', 0)
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO sessions (duration_minutes) VALUES (?)", (duration,))
            conn.commit()
            conn.close()
            
            self._set_headers(201)
            self.wfile.write(json.dumps({"status": "Session logged"}).encode())
        else:
            self._set_headers(404)

def run(port=8003):
    server_address = ('', port)
    httpd = HTTPServer(server_address, AnalyticsHandler)
    print(f"Analytics Service running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
