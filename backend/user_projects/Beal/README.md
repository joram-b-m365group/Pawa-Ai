import tkinter as tk
from tkinter import filedialog

class DataReaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Reader App")
        self.file_path = None
        self.data = None

        self.file_label = tk.Label(root, text="No file selected")
        self.file_label.pack()

        self.select_file_button = tk.Button(root, text="Select File", command=self.select_file)
        self.select_file_button.pack()

        self.read_data_button = tk.Button(root, text="Read Data", command=self.read_data)
        self.read_data_button.pack()

        self.data_text = tk.Text(root)
        self.data_text.pack()

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        self.file_label.config(text=self.file_path)

    def read_data(self):
        if self.file_path:
            try:
                with open(self.file_path, 'r') as file:
                    self.data = file.read()
                    self.data_text.delete(1.0, tk.END)
                    self.data_text.insert(tk.END, self.data)
            except Exception as e:
                self.data_text.delete(1.0, tk.END)
                self.data_text.insert(tk.END, str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = DataReaderApp(root)
    root.mainloop()