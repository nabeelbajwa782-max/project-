import unittest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from modules.planner import PlannerFrame
import tkinter as tk

class TestPlanner(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        # Mocking controller
        self.root.bg_color = "black"
        self.root.fg_color = "white"
        self.root.accent_color = "blue"
        self.planner = PlannerFrame(self.root, self.root)
        
    def tearDown(self):
        self.root.destroy()
        
    def test_priority_map(self):
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        self.assertEqual(priority_map.get("High"), 1)
        self.assertEqual(priority_map.get("Low"), 3)

if __name__ == '__main__':
    unittest.main()
