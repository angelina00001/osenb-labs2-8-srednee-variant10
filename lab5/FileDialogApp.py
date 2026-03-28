import tkinter as tk
from tkinter import ttk, filedialog

class FileDialogApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Выбор файла")
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.file_label = ttk.Label(main_frame, text="Файл не выбран")
        self.file_label.grid(row=0, column=0, columnspan=2, pady=5, sticky=tk.W)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        open_button = ttk.Button(button_frame, text="Выбрать файл", command=self.open_file_dialog)
        open_button.grid(row=0, column=0, padx=5)
        
        save_button = ttk.Button(button_frame, text="Сохранить файл", command=self.save_file_dialog)
        save_button.grid(row=0, column=1, padx=5)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_label.config(text=f"Открыть: {file_path}")
            
    def save_file_dialog(self):
        file_path = filedialog.asksaveasfilename()
        if file_path:
            self.file_label.config(text=f"Сохранить: {file_path}")
            
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = FileDialogApp()
    app.run()
