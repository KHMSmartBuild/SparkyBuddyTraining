# Script name : ui_classes.py
#Location = gui\utils\prep\ui_classes.py
# Author: KHM Smartbuild
# Purpose: 
"""
This script is used to create the UI classes for the Sparky GUI

"""
# Created: 10/01/2022
# Updated: 10/01/2022
# Copyright: (c) 2022 KHM Smartbuild

import tkinter as tk

class QuestionLabel(tk.Label):
    def __init__(self, master, question, entry_box):
        super().__init__(master, text=question, font=("Arial", 10), fg="blue", cursor="hand2")
        self.question = question
        self.entry_box = entry_box
        self.bind("<Button-1>", self.insert_question)

    def insert_question(self, event):
        self.entry_box.delete(0, tk.END)
        self.entry_box.insert(0, self.question)

class ReferenceLabel(tk.Label):
    def __init__(self, master, reference, entry_box):
        super().__init__(master, text=reference, font=("Arial", 10), fg="blue", cursor="hand2")
        self.reference = reference
        self.entry_box = entry_box
        self.bind("<Button-1>", self.insert_reference)

    def insert_reference(self, event):
        self.entry_box.delete(0, tk.END)
        self.entry_box.insert(0, self.reference)