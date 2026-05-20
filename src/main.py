import tkinter as tk
from tkinter import ttk
import sys
import os

# Add modules path
sys.path.append(os.path.dirname(__file__))

from modules.dashboard import DashboardFrame
from modules.planner import PlannerFrame
from modules.timer import TimerFrame
from modules.notes import NotesFrame
from modules.analytics import AnalyticsFrame
from modules.settings import SettingsFrame
from database.db_manager import init_db, get_connection

class WeatherDashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Initialize DB
        init_db()
        
        self.title("Weather Dashboard & Study Planner")
        self.geometry("1000x700")
        
        # Configure grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Style
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        
        # Read Theme
        theme = "dark"
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key='theme'")
            row = cursor.fetchone()
            if row:
                theme = row[0]
            conn.close()
        except:
            pass

        if theme == "light":
            self.bg_color = "#F0F0F0"
            self.sidebar_color = "#E0E0E0"
            self.fg_color = "#000000"
            self.accent_color = "#005A9E"
        else:
            self.bg_color = "#1E1E1E"
            self.sidebar_color = "#252526"
            self.fg_color = "#FFFFFF"
            self.accent_color = "#007ACC"
        
        self.configure(bg=self.bg_color)
        
        self.create_sidebar()
        self.create_main_frame()
        
        # Show default frame
        self.show_frame("Dashboard")

    def create_sidebar(self):
        self.sidebar = tk.Frame(self, bg=self.sidebar_color, width=200)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)
        
        title_lbl = tk.Label(self.sidebar, text="StudyDash", bg=self.sidebar_color, fg=self.accent_color, font=("Segoe UI", 20, "bold"))
        title_lbl.pack(pady=30)
        
        buttons = [
            "Dashboard",
            "Study Planner",
            "Focus Timer",
            "Notes",
            "Analytics",
            "Settings"
        ]
        
        self.nav_buttons = {}
        for btn_text in buttons:
            btn = tk.Button(self.sidebar, text=btn_text, bg=self.sidebar_color, fg=self.fg_color, 
                            bd=0, font=("Segoe UI", 12), cursor="hand2", anchor="w", padx=20,
                            activebackground=self.accent_color, activeforeground="white",
                            command=lambda b=btn_text: self.show_frame(b))
            btn.pack(fill="x", pady=2)
            self.nav_buttons[btn_text] = btn
            
    def create_main_frame(self):
        self.container = tk.Frame(self, bg=self.bg_color)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}
        
        # Map frame names to classes
        frame_classes = {
            "Dashboard": DashboardFrame,
            "Study Planner": PlannerFrame,
            "Focus Timer": TimerFrame,
            "Notes": NotesFrame,
            "Analytics": AnalyticsFrame,
            "Settings": SettingsFrame
        }
        
        for name, F in frame_classes.items():
            frame = F(parent=self.container, controller=self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
    def show_frame(self, name):
        frame = self.frames[name]
        
        # Call an update method if the frame has one, to refresh data
        if hasattr(frame, "on_show"):
            frame.on_show()
            
        frame.tkraise()
        
        # Highlight active button
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name:
                btn.configure(bg=self.accent_color)
            else:
                btn.configure(bg=self.sidebar_color)

if __name__ == "__main__":
    app = WeatherDashboardApp()
    app.mainloop()
