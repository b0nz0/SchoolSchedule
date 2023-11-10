from tkinter import *
from tkinter import ttk
import gui.setup, gui.event
import db.query


def school_select_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root

    school_select_frame = ttk.Frame(root, padding="3 3 12 12")
    school_select_frame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    label = ttk.Label(school_select_frame, text="Seleziona scuola")
    label.grid(column=0, row=0, sticky=(N, E, W, S))

    schoolsvar = StringVar()
    schools_combo = ttk.Combobox(school_select_frame, textvariable=schoolsvar)
    schools_combo.grid(column=1, row=0, sticky=(N, W, E, S))
    schools_combo.bind('<<ComboboxSelected>>', gui.event.school_selected)
    school_dict = {}
    for school in db.query.get_schools():
        school_dict[school.name] = school.id
    schools_combo['values'] = list(school_dict.keys())
    print(schools_combo['values'])
    
    for child in school_select_frame.winfo_children():
        child.grid_configure(padx=5, pady=5)

    ui.frames['school_select_frame'] = school_select_frame
    ui.widgets['schools_combo'] = schools_combo
    ui.variables['school_dict'] = school_dict

