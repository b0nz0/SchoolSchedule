from tkinter import *
from tkinter import ttk
import gui.setup, gui.event
import db.query

schools_combo = None
school_dict = {}

def main_screen():
    gui.setup.root.title("School Scheduler")

    mainframe = ttk.Frame(gui.setup.root, padding="3 3 12 12")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    gui.setup.root.columnconfigure(0, weight=1)
    gui.setup.root.rowconfigure(0, weight=1)

    schoolsvar = StringVar()
    global schools_combo
    global school_dict
    schools_combo = ttk.Combobox(mainframe, textvariable=schoolsvar)
    schools_combo.grid(column=1, row=1, sticky=(N, W, E, S))
    schools_combo.bind('<<ComboboxSelected>>', gui.event.school_selected)
    school_dict = {}
    for school in db.query.get_schools():
        school_dict[school.name] = school.id
    schools_combo['values'] = list(school_dict.keys())
    print(schools_combo['values'])

    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)

    

