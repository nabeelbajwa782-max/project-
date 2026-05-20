import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import get_connection

class SettingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        
        lbl = tk.Label(self, text="Settings", font=("Segoe UI", 24, "bold"), bg=controller.bg_color, fg=controller.fg_color)
        lbl.pack(pady=20)
        
        self.theme_var = tk.StringVar(value="dark")
        self.load_settings()
        
        frame = tk.Frame(self, bg=controller.bg_color)
        frame.pack(pady=10)
        
        tk.Label(frame, text="Theme:", font=("Segoe UI", 14), bg=controller.bg_color, fg=controller.fg_color).grid(row=0, column=0, padx=10)
        theme_menu = ttk.Combobox(frame, textvariable=self.theme_var, values=["dark", "light"], state="readonly")
        theme_menu.grid(row=0, column=1, padx=10)
        
        save_btn = tk.Button(self, text="Save Settings & Restart", bg=controller.accent_color, fg="white", font=("Segoe UI", 12), command=self.save_settings)
        save_btn.pack(pady=20)
        
    def load_settings(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT value FROM settings WHERE key='theme'")
            row = cursor.fetchone()
            if row:
                self.theme_var.set(row[0])
            conn.close()
        except Exception as e:
            print("Error loading settings:", e)
            
    def save_settings(self):
        theme = self.theme_var.get()
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT OR REPLACE INTO settings (key, value) VALUES ('theme', ?)", (theme,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Settings", "Settings saved. Please restart the application to apply changes.")
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def on_show(self):
        self.load_settings()
