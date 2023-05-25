import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from pdf_reader import PDFReader

class PDFReaderUI:

    def __init__(self, master):
        self.master = master
        master.title('PDF Reader')

        self.choose_file_button = tk.Button(master, text='Choose File', command=self.choose_file)
        self.choose_file_button.pack()

        self.extract_button = tk.Button(master, text='Extract Data', command=self.extract_data)
        self.extract_button.pack()

        self.table_header = tk.Frame(master)
        self.table_header.pack(side=tk.TOP)

        self.col1_lbl = tk.Label(self.table_header, width=20, text='Title')
        self.col1_lbl.pack(side=tk.LEFT)

        self.col2_lbl = tk.Label(self.table_header, width=20, text='Value')
        self.col2_lbl.pack(side=tk.LEFT)

        self.table_frame = tk.Frame(master)
        self.table_frame.pack()

        self.image_frame = tk.Frame(master)
        self.image_frame.pack()

        self.pdf_reader = PDFReader()

    def choose_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[('PDF Files', '*.pdf')])
        self.show_thumbnail()

    def show_thumbnail(self):
        image = self.pdf_reader.get_thumbnail(self.file_path)
        image = ImageTk.PhotoImage(image)
        image_lbl = tk.Label(self.image_frame, image=image)
        image_lbl.image = image
        image_lbl.pack()

    def extract_data(self):
        self.pdf_reader.extract_data(self.file_path)
        self.display_data()

    def display_data(self):
        self.clear_table()
        data = self.pdf_reader.get_data()
        for title, value in data.items():
            row = tk.Frame(self.table_frame)
            col1 = tk.Label(row, width=20, text=title, anchor='w')
            col2 = tk.Label(row, width=20, text=value, anchor='w')
            row.pack(side=tk.TOP, padx=5, pady=5)
            col1.pack(side=tk.LEFT)
            col2.pack(side=tk.LEFT)

    def clear_table(self):
        for child in self.table_frame.winfo_children():
            child.destroy()

    def close(self):
        self.master.quit()

root = tk.Tk()
pdf_reader_ui = PDFReaderUI(root)
root.protocol('WM_DELETE_WINDOW', pdf_reader_ui.close)
root.mainloop()
