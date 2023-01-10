from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from covid_template import *


import os

#TODO add proper documentation

def browse_csv_click(browse_text_entry): 
    csv_filename = filedialog.askopenfile(title = "Select File",filetypes = (("CSV Files","*.csv"),))
    browse_text_entry.delete(0,"end")
    browse_text_entry.insert(0, csv_filename.name)

def browse_folder_click(browse_text_entry): 
    output_folder = filedialog.askdirectory(title="Select Folder")  # todo: add a default folder opening location
    browse_text_entry.delete(0,"end")
    browse_text_entry.insert(0, output_folder)


