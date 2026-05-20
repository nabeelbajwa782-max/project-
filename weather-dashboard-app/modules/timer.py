import tkinter as tk
from tkinter import ttk, messagebox
import urllib.request
import json

class TimerFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        
        lbl = tk.Label(self, text="Focus Timer", font=("Segoe UI", 24, "bold"), bg=controller.bg_color, fg=controller.fg_color)
        lbl.pack(pady=20)
        
        # Mode Selection
        self.mode_var = tk.StringVar(value="Pomodoro (25 min)")
        mode_menu = ttk.Combobox(self, textvariable=self.mode_var, values=["Pomodoro (25 min)", "Short Break (5 min)", "Long Break (15 min)"], state="readonly", font=("Segoe UI", 12))
        mode_menu.pack(pady=10)
        mode_menu.bind("<<ComboboxSelected>>", self.change_mode)
        
        self.time_lbl = tk.Label(self, text="25:00", font=("Segoe UI", 64, "bold"), bg=controller.bg_color, fg=controller.accent_color)
        self.time_lbl.pack(pady=20)
        
        btn_frame = tk.Frame(self, bg=controller.bg_color)
        btn_frame.pack(pady=20)
        
        self.start_btn = tk.Button(btn_frame, text="Start", bg=controller.accent_color, fg="white", font=("Segoe UI", 14), width=10, command=self.start_timer)
        self.start_btn.pack(side="left", padx=10)
        
        self.stop_btn = tk.Button(btn_frame, text="Stop", bg="#D32F2F", fg="white", font=("Segoe UI", 14), width=10, command=self.stop_timer)
        self.stop_btn.pack(side="left", padx=10)
        
        self.is_running = False
        self.time_left = 25 * 60
        self.current_duration = 25
        
    def change_mode(self, event=None):
        if self.is_running:
            self.stop_timer()
            
        mode = self.mode_var.get()
        if "25" in mode:
            self.time_left = 25 * 60
            self.current_duration = 25
        elif "15" in mode:
            self.time_left = 15 * 60
            self.current_duration = 15
        elif "5" in mode:
            self.time_left = 5 * 60
            self.current_duration = 5
            
        self.update_display()
        
    def update_display(self):
        mins, secs = divmod(self.time_left, 60)
        self.time_lbl.config(text=f"{mins:02d}:{secs:02d}")
        
    def update_timer(self):
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.update_display()
            self._timer_id = self.after(1000, self.update_timer)
        elif self.time_left == 0 and self.is_running:
            self.is_running = False
            self.time_lbl.config(text="Time's Up!")
            messagebox.showinfo("Timer", "Session Completed!")
            
            # Save session to Microservice if it was a Pomodoro
            if self.current_duration == 25:
                self.save_session()
                
    def save_session(self):
        try:
            req = urllib.request.Request('http://localhost:8003/sessions', method='POST')
            req.add_header('Content-Type', 'application/json')
            data = json.dumps({"duration_minutes": self.current_duration}).encode()
            with urllib.request.urlopen(req, data=data) as response:
                pass
        except Exception as e:
            print("Error saving session via microservice:", e)
            
    def start_timer(self):
        if not self.is_running:
            if self.time_left == 0:
                self.change_mode() # Reset
            self.is_running = True
            self.update_timer()
            self.start_btn.config(state="disabled")
            
    def stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.after_cancel(self._timer_id)
            self.start_btn.config(state="normal")
            
    def on_show(self):
        pass
