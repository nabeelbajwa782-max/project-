import unittest
import os
import sys

# Add root project path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from database.db_manager import init_db, get_connection

class TestDatabase(unittest.TestCase):
    def setUp(self):
        init_db()
        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        
    def tearDown(self):
        self.conn.close()
        
    def test_settings_theme_exists(self):
        self.cursor.execute("SELECT value FROM settings WHERE key='theme'")
        val = self.cursor.fetchone()
        self.assertIsNotNone(val, "Theme setting should exist.")
        
    def test_insert_task(self):
        self.cursor.execute("INSERT INTO tasks (title, priority) VALUES (?, ?)", ("Test Task", 1))
        self.conn.commit()
        
        self.cursor.execute("SELECT title FROM tasks WHERE title='Test Task'")
        val = self.cursor.fetchone()
        self.assertIsNotNone(val)
        
        # Cleanup
        self.cursor.execute("DELETE FROM tasks WHERE title='Test Task'")
        self.conn.commit()

if __name__ == '__main__':
    unittest.main()
