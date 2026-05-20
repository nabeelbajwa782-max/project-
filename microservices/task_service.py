from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import urllib.parse
import os
import sys

# Add root project path to import database manager from src
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from database.db_manager import get_connection

class TaskHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/tasks':
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, priority FROM tasks ORDER BY priority ASC")
            tasks = [{"id": row[0], "title": row[1], "priority": row[2]} for row in cursor.fetchall()]
            conn.close()
            
            self._set_headers(200)
            self.wfile.write(json.dumps(tasks).encode())
            
        elif self.path == '/notes':
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, content FROM notes ORDER BY id DESC")
            notes = [{"id": row[0], "title": row[1], "content": row[2]} for row in cursor.fetchall()]
            conn.close()
            
            self._set_headers(200)
            self.wfile.write(json.dumps(notes).encode())
        else:
            self._set_headers(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        if self.path == '/tasks':
            title = data.get('title')
            priority = data.get('priority', 3)
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, priority) VALUES (?, ?)", (title, priority))
            conn.commit()
            conn.close()
            
            self._set_headers(201)
            self.wfile.write(json.dumps({"status": "Task created"}).encode())
            
        elif self.path == '/notes':
            title = data.get('title')
            content = data.get('content')
            note_id = data.get('id')
            
            conn = get_connection()
            cursor = conn.cursor()
            if note_id:
                cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, note_id))
            else:
                cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            conn.commit()
            conn.close()
            
            self._set_headers(201)
            self.wfile.write(json.dumps({"status": "Note saved"}).encode())
        else:
            self._set_headers(404)

    def do_DELETE(self):
        if self.path.startswith('/tasks?title='):
            title = urllib.parse.unquote(self.path.split('=')[1])
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE title=?", (title,))
            conn.commit()
            conn.close()
            
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "Task deleted"}).encode())
            
        elif self.path.startswith('/notes?id='):
            note_id = int(self.path.split('=')[1])
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id=?", (note_id,))
            conn.commit()
            conn.close()
            
            self._set_headers(200)
            self.wfile.write(json.dumps({"status": "Note deleted"}).encode())
        else:
            self._set_headers(404)

def run(port=8002):
    server_address = ('', port)
    httpd = HTTPServer(server_address, TaskHandler)
    print(f"Task Service running on port {port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
