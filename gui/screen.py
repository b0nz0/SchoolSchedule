from tkinter import *
from tkinter import ttk
import gui.setup, gui.event
import db.query

NEW_COMBO_LABEL = "<Nuovo>"
SCHOOL_SELECT_LABEL = "Seleziona scuola"
SCHOOLYEAR_SELECT_LABEL = "Seleziona anno scolastico"
ADD_SCHOOL_LABEL = "Aggiungi scuola"
ADD_SCHOOLYEAR_LABEL = "Aggiungi anno scolastico"
ADD_YEAR_LABEL = "Aggiungi anno"
ADD_SECTION_LABEL = "Aggiungi sezione"
DELETE_SCHOOL_LABEL = "Elimina scuola"
DELETE_SCHOOLYEAR_LABEL = "Elimina anno scolastico"
DELETE_YEAR_LABEL = "Elimina anno"
DELETE_SECTION_LABEL = "Elimina sezione"
DUPLICATE_SCHOOL_LABEL = "Duplica scuola"
DUPLICATE_SCHOOLYEAR_LABEL = "Duplica anno scolastico"
RESET_SCHOOLYEAR_LABEL = "Ripristina anno scolastico"
MANAGE_CLASSES_LABEL = "Gestisci classi"
MANAGE_LOGISTIC_LABEL = "Gestisci spazi"
MANAGE_SUBJECTS_LABEL = "Gestisci materie"
MANAGE_PERSONS_LABEL = "Gestisci docenti"
MANAGE_TIMETABLE_LABEL = "Gestisci date/ore"
MANAGE_RESTRICTIONS_LABEL = "Gestisci vincoli"
PROCESS_LABEL = "Elabora calendari"

YEAR_SELECT_LABEL = "Anni"
SECTION_SELECT_LABEL = "Sezioni"


def school_select_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # school selection
    school_label = ttk.Label(frame, text=SCHOOL_SELECT_LABEL)
    school_label.grid(column=0, row=0, sticky=(N, E, W, S))

    schoolsvar = StringVar()
    schools_combo = ttk.Combobox(frame, textvariable=schoolsvar)
    schools_combo.grid(column=1, row=0, sticky=(N, W, E, S))
    schools_combo.bind('<<ComboboxSelected>>', gui.event.school_selected)

    school_add_button = ttk.Button(frame, text=ADD_SCHOOL_LABEL, command=gui.event.school_add)
    school_add_button.grid(column=11, row=0, sticky=(N, E, W, S))
    school_add_button.state(['!disabled'])

    school_delete_button = ttk.Button(frame, text=DELETE_SCHOOL_LABEL, command=gui.event.school_delete)
    school_delete_button.grid(column=12, row=0, sticky=(N, E, W, S))
    school_delete_button.state(['disabled'])

    school_duplicate_button = ttk.Button(frame, text=DUPLICATE_SCHOOL_LABEL, command=gui.event.school_delete)
    school_duplicate_button.grid(column=13, row=0, sticky=(N, E, W, S))
    school_duplicate_button.state(['disabled'])

    # school year selection
    schoolyears_label = ttk.Label(frame, text=SCHOOLYEAR_SELECT_LABEL)
    schoolyears_label.grid(column=0, row=1, sticky=(N, E, W, S))

    schoolyearssvar = StringVar()
    schoolyears_combo = ttk.Combobox(frame, textvariable=schoolyearssvar)
    schoolyears_combo.grid(column=1, row=1, sticky=(N, W, E, S))
    schoolyears_combo.bind('<<ComboboxSelected>>', gui.event.schoolyear_selected)
    schoolyears_combo['values'] = ['']

    schoolyear_add_button = ttk.Button(frame, text=ADD_SCHOOLYEAR_LABEL, command=gui.event.schoolyear_add)
    schoolyear_add_button.grid(column=11, row=1, sticky=(N, E, W, S))
    schoolyear_add_button.state(['!disabled'])

    schoolyear_delete_button = ttk.Button(frame, text=DELETE_SCHOOLYEAR_LABEL, command=gui.event.schoolyear_delete)
    schoolyear_delete_button.grid(column=12, row=1, sticky=(N, E, W, S))
    schoolyear_delete_button.state(['disabled'])

    schoolyear_duplicate_button = ttk.Button(frame, text=DUPLICATE_SCHOOLYEAR_LABEL, command=gui.event.schoolyear_delete)
    schoolyear_duplicate_button.grid(column=13, row=1, sticky=(N, E, W, S))
    schoolyear_duplicate_button.state(['disabled'])

    schoolyear_reset_button = ttk.Button(frame, text=RESET_SCHOOLYEAR_LABEL, command=gui.event.schoolyear_delete)
    schoolyear_reset_button.grid(column=14, row=1, sticky=(N, E, W, S))
    schoolyear_reset_button.state(['disabled'])

    classes_mgmt_button = ttk.Button(frame, text=MANAGE_CLASSES_LABEL)
    classes_mgmt_button.grid(column=0, row=10, columnspan=2, sticky=(N, E, W, S))
    classes_mgmt_button.state(['disabled'])
    
    lgst_mgmt_button = ttk.Button(frame, text=MANAGE_LOGISTIC_LABEL)
    lgst_mgmt_button.grid(column=11, row=10, columnspan=2, sticky=(N, E, W, S))
    lgst_mgmt_button.state(['disabled'])
    
    sbj_mgmt_button = ttk.Button(frame, text=MANAGE_SUBJECTS_LABEL)
    sbj_mgmt_button.grid(column=13, row=10, columnspan=2, sticky=(N, E, W, S))
    sbj_mgmt_button.state(['disabled'])
    
    pers_mgmt_button = ttk.Button(frame, text=MANAGE_PERSONS_LABEL)
    pers_mgmt_button.grid(column=0, row=11, columnspan=2, sticky=(N, E, W, S))
    pers_mgmt_button.state(['disabled'])
    
    time_mgmt_button = ttk.Button(frame, text=MANAGE_TIMETABLE_LABEL)
    time_mgmt_button.grid(column=11, row=11, columnspan=2, sticky=(N, E, W, S))
    time_mgmt_button.state(['disabled'])
    
    rest_mgmt_button = ttk.Button(frame, text=MANAGE_RESTRICTIONS_LABEL)
    rest_mgmt_button.grid(column=13, row=11, columnspan=2, sticky=(N, E, W, S))
    rest_mgmt_button.state(['disabled'])
    
    proc_mgmt_button = ttk.Button(frame, text=PROCESS_LABEL)
    proc_mgmt_button.grid(column=11, row=12, columnspan=2, sticky=(N, E, W, S))
    proc_mgmt_button.state(['disabled'])
    

    heights = []
    widths = []
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
        heights.append([child.winfo_reqheight()])
        widths.append([child.winfo_reqwidth()])

    height = 40
    width = max(widths)

    frame.rowconfigure(0, minsize=height)
    frame.rowconfigure(1, minsize=height)
    frame.columnconfigure(0, minsize=width)
    frame.columnconfigure(1, minsize=width)
    frame.columnconfigure(11, minsize=width)
    frame.columnconfigure(12, minsize=width)
    frame.columnconfigure(13, minsize=width)
    frame.columnconfigure(14, minsize=width)

    schoolyears_label.grid_remove()
    schoolyears_combo.grid_remove()
    schoolyear_add_button.grid_remove()
    schoolyear_delete_button.grid_remove()
    schoolyear_duplicate_button.grid_remove()
    schoolyear_reset_button.grid_remove()

    ui.frames['school_select_frame'] = frame
    ui.widgets['schools_combo'] = schools_combo
    ui.widgets['school_add_button'] = school_add_button
    ui.widgets['school_delete_button'] = school_delete_button
    ui.widgets['school_duplicate_button'] = school_duplicate_button
    ui.widgets['schoolyears_combo'] = schoolyears_combo
    ui.widgets['schoolyears_label'] = schoolyears_label
    ui.widgets['schoolyear_add_button'] = schoolyear_add_button
    ui.widgets['schoolyear_delete_button'] = schoolyear_delete_button
    ui.widgets['schoolyear_duplicate_button'] = schoolyear_duplicate_button
    ui.widgets['schoolyear_reset_button'] = schoolyear_reset_button

    gui.event.populate_school_combo()

def configure_schoolyear_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    #year selection
    year_label = ttk.Label(frame, text=YEAR_SELECT_LABEL)
    year_label.grid(column=0, row=2, sticky=(N, E, W, S))

    years_listbox = ttk.Treeview(frame, show="tree")
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=years_listbox.yview)
    years_listbox.configure(yscroll=scrollbar.set)
    years_listbox.grid(column=1, row=2, sticky=(N, W, E, S))
    scrollbar.configure(command=years_listbox.yview)
    scrollbar.grid(column=2, row=2, sticky='ns')
    years_listbox.bind('<<TreeviewSelect>>', gui.event.year_selected)

    year_add_button = ttk.Button(frame, text=ADD_YEAR_LABEL, command=gui.event.year_add)
    year_add_button.grid(column=11, row=2, sticky=(E, W))
    year_add_button.state(['!disabled'])

    year_delete_button = ttk.Button(frame, text=DELETE_YEAR_LABEL, command=gui.event.year_delete)
    year_delete_button.grid(column=12, row=2, sticky=(E, W))
    year_delete_button.state(['disabled'])


    heights = []
    widths = []
    for child in frame.winfo_children():
        child.grid_configure(padx=5, pady=5)
        heights.append([child.winfo_reqheight()])
        widths.append([child.winfo_reqwidth()])

    height = 40
    width = max(widths)

    frame.rowconfigure(0, minsize=height)
    frame.rowconfigure(1, minsize=height)
    frame.columnconfigure(0, minsize=width)
    frame.columnconfigure(1, minsize=width)

    ui.frames['schoolyear_configure_frame'] = frame
    ui.widgets['years_listbox'] = years_listbox

    gui.event.populate_schoolyear_cofiguration()

