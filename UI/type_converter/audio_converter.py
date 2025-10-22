# text_converter.py
import tkinter as tk

class AudioPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="white")
        tk.Label(self, text="audio Converter Page", font=("Segoe UI", 20)).pack(expand=True)
