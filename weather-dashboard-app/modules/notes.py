import tkinter as tk
from tkinter import ttk, messagebox
from database.db_manager import get_connection

class NotesFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.bg_color)
        self.controller = controller
        
        lbl = tk.Label(self, text="Notes", font=("Segoe UI", 24, "bold"), bg=controller.bg_color, fg=controller.fg_color)
        lbl.pack(pady=20)
        
        # Split screen: Left is notes list, Right is text area
        main_frame = tk.Frame(self, bg=controller.bg_color)
        main_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Left Panel (List)
        left_panel = tk.Frame(main_frame, bg=controller.bg_color, width=200)
        left_panel.pack(side="left", fill="y", padx=(0, 10))
        
        self.notes_listbox = tk.Listbox(left_panel, font=("Segoe UI", 12), bg="#2D2D30", fg="white", selectbackground=controller.accent_color)
        self.notes_listbox.pack(fill="both", expand=True)
        self.notes_listbox.bind('<<ListboxSelect>>', self.load_selected_note)
        
        btn_frame = tk.Frame(left_panel, bg=controller.bg_color)
        btn_frame.pack(fill="x", pady=5)
        
        new_btn = tk.Button(btn_frame, text="New", bg=controller.accent_color, fg="white", command=self.clear_text)
        new_btn.pack(side="left", expand=True, fill="x", padx=(0,2))
        
        del_btn = tk.Button(btn_frame, text="Delete", bg="#D32F2F", fg="white", command=self.delete_note)
        del_btn.pack(side="left", expand=True, fill="x", padx=(2,0))
        
        # Right Panel (Editor)
        right_panel = tk.Frame(main_frame, bg=controller.bg_color)
        right_panel.pack(side="right", fill="both", expand=True)
        
        title_frame = tk.Frame(right_panel, bg=controller.bg_color)
        title_frame.pack(fill="x", pady=(0, 5))
        tk.Label(title_frame, text="Title:", bg=controller.bg_color, fg=controller.fg_color).pack(side="left")
        self.title_entry = tk.Entry(title_frame, font=("Segoe UI", 12))
        self.title_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        self.text_area = tk.Text(right_panel, font=("Segoe UI", 12), bg="#2D2D30", fg="white", insertbackground="white")
        self.text_area.pack(fill="both", expand=True)
        
        save_btn = tk.Button(right_panel, text="Save Note", bg=controller.accent_color, fg="white", font=("Segoe UI", 12), command=self.save_note)
        save_btn.pack(pady=10)
        
        self.current_note_id = None
        self.load_notes_list()
        
    def clear_text(self):
        self.current_note_id = None
        self.title_entry.delete(0, tk.END)
        self.text_area.delete("1.0", tk.END)
        
    def load_notes_list(self):
        self.notes_listbox.delete(0, tk.END)
        self.notes_data = []
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, content FROM notes ORDER BY id DESC")
            notes = cursor.fetchall()
            for note in notes:
                self.notes_data.append(note)
                self.notes_listbox.insert(tk.END, note[1])
            conn.close()
        except Exception as e:
            print("Error loading notes:", e)
            
    def load_selected_note(self, event):
        selection = self.notes_listbox.curselection()
        if not selection:
            return
            
        index = selection[0]
        note = self.notes_data[index]
        self.current_note_id = note[0]
        
        self.title_entry.delete(0, tk.END)
        self.title_entry.insert(0, note[1])
        
        self.text_area.delete("1.0", tk.END)
        self.text_area.insert(tk.END, note[2])
        
    def save_note(self):
        title = self.title_entry.get().strip()
        content = self.text_area.get("1.0", tk.END).strip()
        
        if not title:
            messagebox.showwarning("Warning", "Title is required.")
            return
            
        try:
            conn = get_connection()
            cursor = conn.cursor()
            if self.current_note_id is None:
                cursor.execute("INSERT INTO notes (title, content) VALUES (?, ?)", (title, content))
            else:
                cursor.execute("UPDATE notes SET title=?, content=? WHERE id=?", (title, content, self.current_note_id))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Note saved successfully.")
            self.load_notes_list()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
    def delete_note(self):
        if self.current_note_id is None:
            return
            
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM notes WHERE id=?", (self.current_note_id,))
            conn.commit()
            conn.close()
            
            self.clear_text()
            self.load_notes_list()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            
    def on_show(self):
        self.load_notes_list()
