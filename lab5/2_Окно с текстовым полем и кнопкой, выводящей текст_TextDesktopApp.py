import tkinter as tk
from tkinter import ttk

class TextDisplayApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Текстовое поле")
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.text_entry = tk.Text(main_frame, height=5, width=40)
        self.text_entry.grid(row=0, column=0, columnspan=2, pady=5, sticky=(tk.W, tk.E))
        
        display_button = ttk.Button(main_frame, text="Вывести текст", command=self.display_text)
        display_button.grid(row=1, column=0, pady=10, sticky=tk.W)
        
        self.result_label = ttk.Label(main_frame, text="")
        self.result_label.grid(row=2, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
    def display_text(self):
        text_content = self.text_entry.get("1.0", tk.END).strip()
        if text_content:
            self.result_label.config(text=text_content)
        else:
            self.result_label.config(text="Текст не введен")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = TextDisplayApp()
    app.run()
