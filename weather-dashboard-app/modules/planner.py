import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import get_connection

class PlannerFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        
        lbl = tk.Label(self, text="Study Planner", font=("Segoe UI", 24, "bold"), bg=controller.bg_color, fg=controller.fg_color)
        lbl.pack(pady=20)
        
        # Input Frame
        input_frame = tk.Frame(self, bg=controller.bg_color)
        input_frame.pack(pady=10)
        
        self.task_entry = tk.Entry(input_frame, font=("Segoe UI", 12), width=30)
        self.task_entry.grid(row=0, column=0, padx=5)
        
        self.priority_var = tk.StringVar(value="Low")
        priority_menu = ttk.Combobox(input_frame, textvariable=self.priority_var, values=["High", "Medium", "Low"], state="readonly", width=10)
        priority_menu.grid(row=0, column=1, padx=5)
        
        add_btn = tk.Button(input_frame, text="Add Task", bg=controller.accent_color, fg="white", font=("Segoe UI", 10), command=self.add_task)
        add_btn.grid(row=0, column=2, padx=5)
        
        # Task List
        self.task_listbox = tk.Listbox(self, font=("Segoe UI", 12), bg="#2D2D30", fg="white", selectbackground=controller.accent_color)
        self.task_listbox.pack(pady=10, padx=20, fill="both", expand=True)
        
        # Delete btn
        del_btn = tk.Button(self, text="Delete Selected", bg="#D32F2F", fg="white", font=("Segoe UI", 10), command=self.delete_task)
        del_btn.pack(pady=5)
        
        self.load_tasks()
        
    def add_task(self):
        title = self.task_entry.get().strip()
        priority_str = self.priority_var.get()
        priority_map = {"High": 1, "Medium": 2, "Low": 3}
        priority = priority_map.get(priority_str, 3)
        
        if not title:
            messagebox.showerror("Error", "Task title cannot be empty.")
            return
            
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tasks (title, priority) VALUES (?, ?)", (title, priority))
            conn.commit()
            conn.close()
            self.task_entry.delete(0, tk.END)
            self.load_tasks()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
    def delete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        task_str = self.task_listbox.get(index)
        
        # Extact ID or just use matching title
        # Since listbox stores string, let's keep it simple: we can map id by storing it in a dictionary, but for now we delete by title
        title = task_str.split("] ")[1]
        
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE title=?", (title,))
            conn.commit()
            conn.close()
            self.load_tasks()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
    def load_tasks(self):
        self.task_listbox.delete(0, tk.END)
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT title, priority FROM tasks ORDER BY priority ASC")
            tasks = cursor.fetchall()
            priority_names = {1: "High", 2: "Medium", 3: "Low"}
            for task in tasks:
                p_name = priority_names.get(task[1], "Low")
                self.task_listbox.insert(tk.END, f"[{p_name}] {task[0]}")
            conn.close()
        except Exception as e:
            print("Error loading tasks:", e)

    def on_show(self):
        self.load_tasks()
