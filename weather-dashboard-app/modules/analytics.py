import tkinter as tk
from tkinter import ttk
from database.db_manager import get_connection

class AnalyticsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        
        lbl = tk.Label(self, text="Productivity Analytics", font=("Segoe UI", 24, "bold"), bg=controller.bg_color, fg=controller.fg_color)
        lbl.pack(pady=20)
        
        self.stats_lbl = tk.Label(self, text="Total Focus Time: 0 mins", font=("Segoe UI", 16), bg=controller.bg_color, fg=controller.accent_color)
        self.stats_lbl.pack(pady=10)
        
        self.chart_frame = tk.Frame(self, bg=controller.bg_color)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Native Tkinter Canvas for Bar Chart (No matplotlib dependency)
        self.canvas = tk.Canvas(self.chart_frame, bg="#1E1E1E", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
    def load_data(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            
            # Total focus time
            cursor.execute("SELECT SUM(duration_minutes) FROM sessions")
            total_mins = cursor.fetchone()[0] or 0
            self.stats_lbl.config(text=f"Total Focus Time: {total_mins} mins")
            
            # Sessions per day (last 7 days approx)
            cursor.execute("SELECT date(completed_at), SUM(duration_minutes) FROM sessions GROUP BY date(completed_at) ORDER BY completed_at DESC LIMIT 7")
            data = cursor.fetchall()
            conn.close()
            
            self.draw_chart(data)
            
        except Exception as e:
            print("Error loading analytics:", e)

    def draw_chart(self, data):
        self.canvas.delete("all")
        
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            # If canvas not drawn yet, use default sizes
            width = 600
            height = 300
            
        if not data:
            self.canvas.create_text(width/2, height/2, text="No data available yet.", fill="white", font=("Segoe UI", 14))
            return
            
        dates = [row[0] for row in reversed(data)]
        mins = [row[1] for row in reversed(data)]
        max_mins = max(mins) if max(mins) > 0 else 1
        
        # Draw axes
        margin_x = 50
        margin_y = 50
        chart_w = width - 2*margin_x
        chart_h = height - 2*margin_y
        
        self.canvas.create_line(margin_x, height - margin_y, width - margin_x, height - margin_y, fill="white", width=2) # X axis
        self.canvas.create_line(margin_x, margin_y, margin_x, height - margin_y, fill="white", width=2) # Y axis
        
        bar_w = chart_w / len(dates) * 0.6
        spacing = chart_w / len(dates)
        
        for i, (date_str, m) in enumerate(zip(dates, mins)):
            x0 = margin_x + i * spacing + spacing*0.2
            y0 = height - margin_y
            x1 = x0 + bar_w
            y1 = height - margin_y - (m / max_mins * chart_h)
            
            self.canvas.create_rectangle(x0, y0, x1, y1, fill="#007ACC", outline="")
            self.canvas.create_text(x0 + bar_w/2, y1 - 10, text=str(m), fill="white")
            
            # Display MM-DD
            short_date = date_str[5:]
            self.canvas.create_text(x0 + bar_w/2, height - margin_y + 20, text=short_date, fill="white", angle=45)

    def on_show(self):
        # Schedule draw after layout updates sizes
        self.after(100, self.load_data)
