import unittest
import os
import sys

# Add root project path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from modules.timer import TimerFrame
import tkinter as tk

class TestTimer(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.bg_color = "black"
        self.root.fg_color = "white"
        self.root.accent_color = "blue"
        self.timer = TimerFrame(self.root, self.root)
        
    def tearDown(self):
        self.root.destroy()
        
    def test_initial_state(self):
        self.assertEqual(self.timer.time_left, 25 * 60)
        self.assertFalse(self.timer.is_running)

if __name__ == '__main__':
    unittest.main()
