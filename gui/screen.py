from tkinter import *
from tkinter import ttk
import gui.setup, gui.event
import db.query, db.model

NEW_COMBO_LABEL = "<Nuovo>"
RETURN_HOME = "Ritorna alla home"
SCHOOL_SELECT_LABEL = "Seleziona scuola"
SCHOOLYEAR_SELECT_LABEL = "Seleziona anno scolastico"
ADD_SCHOOL_LABEL = "Aggiungi scuola"
ADD_SCHOOLYEAR_LABEL = "Aggiungi anno scolastico"
ADD_YEAR_LABEL = "Aggiungi anno"
ADD_SECTION_LABEL = "Aggiungi sezione"
CREATE_CLASS_LABEL = "Crea classi da anni e sezioni"
DELETE_SCHOOL_LABEL = "Elimina scuola"
DELETE_SCHOOLYEAR_LABEL = "Elimina anno scolastico"
DELETE_YEAR_LABEL = "Elimina anno"
DELETE_SECTION_LABEL = "Elimina sezione"
DELETE_CLASS_LABEL = "Elimina classe"
MATCH_CLASS_TIMETABLE_LABEL = "Abbina classi al piano orario"
DUPLICATE_SCHOOL_LABEL = "Duplica scuola"
DUPLICATE_SCHOOLYEAR_LABEL = "Duplica anno scolastico"
RESET_SCHOOLYEAR_LABEL = "Ripristina anno scolastico"
MANAGE_CLASSES_LABEL = "Gestisci classi"
MANAGE_LOGISTIC_LABEL = "Gestisci spazi"
MANAGE_SUBJECTS_LABEL = "Gestisci materie"
MANAGE_PERSONS_LABEL = "Gestisci docenti"
MANAGE_TIMETABLE_LABEL = "Gestisci piani orari"
MANAGE_ASSIGNMENT_LABEL = "Gestisci assegnazioni"
MANAGE_RESTRICTIONS_LABEL = "Gestisci restrizioni"
PROCESS_LABEL = "Elabora calendari"

geometries = {}

YEAR_SELECT_LABEL = "Anni"
SECTION_SELECT_LABEL = "Sezioni"
CLASS_SELECT_LABEL = "Classi"

ROOM_SELECT_LABEL = "Spazi"
ADD_ROOM_LABEL = "Aggiungi spazio"
DELETE_ROOM_LABEL = "Elimina spazio"

SUBJECT_SELECT_LABEL = "Materie"
EDIT_SUBJECT_LABEL = "Modifica materia"
ADD_SUBJECT_LABEL = "Aggiungi materia"
DELETE_SUBJECT_LABEL = "Elimina materia"

PERSON_SELECT_LABEL = "Persone"
ADD_PERSON_LABEL = "Aggiungi persona"
DELETE_PERSON_LABEL = "Elimina persona"

TIMETABLE_SELECT_LABEL = "Piano orario"
START_END = "IN/FI"
PLAN_USED_IN = "Piano usato in"

ASSIGNMENT_SELECT_LABEL = "Assegnazioni"
EDIT_ASSIGNMENT_LABEL = "Modifica assegnazione"
ADD_ASSIGNMENT_LABEL = "Aggiungi assegnazione"
DELETE_ASSIGNMENT_LABEL = "Elimina assegnazione"
DUPLICATE_ASSIGNMENT_LABEL = "Duplica assegnazione"

RESTRICTION_SELECT_LABEL = "Restrizioni"
EDIT_RESTRICTION_LABEL = "Modifica restrizione"
ADD_RESTRICTION_LABEL = "Aggiungi restrizione"
DELETE_RESTRICTION_LABEL = "Elimina restrizione"
DUPLICATE_RESTRICTION_LABEL = "Duplica restrizione"

PROCESS_SELECT_LABEL = "Elaborazioni"
PROCESS_DETAIL_LABEL = "Dettagio elaborazione"
PROCESS_START_LABEL = "Avvia nuova elaborazione"

def school_select_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['school_select_frame'] = '1200x400'
    root.geometry('1200x400')

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0)
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

    schoolyear_add_button = ttk.Button(frame, text=ADD_SCHOOLYEAR_LABEL, command=gui.event.schoolyear_create)
    schoolyear_add_button.grid(column=11, row=1, sticky=(N, E, W, S))
    schoolyear_add_button.state(['!disabled'])

    schoolyear_delete_button = ttk.Button(frame, text=DELETE_SCHOOLYEAR_LABEL, command=gui.event.schoolyear_delete)
    schoolyear_delete_button.grid(column=12, row=1, sticky=(N, E, W, S))
    schoolyear_delete_button.state(['disabled'])

    schoolyear_duplicate_button = ttk.Button(frame, text=DUPLICATE_SCHOOLYEAR_LABEL,
                                             command=gui.event.schoolyear_delete)
    schoolyear_duplicate_button.grid(column=13, row=1, sticky=(N, E, W, S))
    schoolyear_duplicate_button.state(['disabled'])

    schoolyear_reset_button = ttk.Button(frame, text=RESET_SCHOOLYEAR_LABEL, command=gui.event.schoolyear_delete)
    schoolyear_reset_button.grid(column=14, row=1, sticky=(N, E, W, S))
    schoolyear_reset_button.state(['disabled'])

    classes_mgmt_button = ttk.Button(frame, text=MANAGE_CLASSES_LABEL, command=lambda: gui.event.switch_frame(
        "school_select_frame", "schoolyear_configure_frame"))
    classes_mgmt_button.grid(column=0, row=10, columnspan=2, sticky=(N, E, W, S))
    classes_mgmt_button.state(['disabled'])

    lgst_mgmt_button = ttk.Button(frame, text=MANAGE_LOGISTIC_LABEL, command=lambda: gui.event.switch_frame(
        "school_select_frame", "room_configure_frame"))
    lgst_mgmt_button.grid(column=11, row=10, columnspan=2, sticky=(N, E, W, S))
    lgst_mgmt_button.state(['disabled'])

    sbj_mgmt_button = ttk.Button(frame, text=MANAGE_SUBJECTS_LABEL, command=lambda: gui.event.switch_frame(
        "school_select_frame", "subject_configure_frame"))
    sbj_mgmt_button.grid(column=13, row=10, columnspan=2, sticky=(N, E, W, S))
    sbj_mgmt_button.state(['disabled'])

    pers_mgmt_button = ttk.Button(frame, text=MANAGE_PERSONS_LABEL, command=lambda: gui.event.switch_frame(
        "school_select_frame", "person_configure_frame"))
    pers_mgmt_button.grid(column=0, row=11, columnspan=2, sticky=(N, E, W, S))
    pers_mgmt_button.state(['disabled'])

    time_mgmt_button = ttk.Button(frame, text=MANAGE_TIMETABLE_LABEL, command=lambda: gui.event.switch_frame(
        "school_select_frame", "timetable_configure_frame"))
    time_mgmt_button.grid(column=11, row=11, columnspan=2, sticky=(N, E, W, S))
    time_mgmt_button.state(['disabled'])

    rest_mgmt_button = ttk.Button(frame, text=MANAGE_RESTRICTIONS_LABEL, command=lambda: gui.event.switch_frame(
        "school_select_frame", "restriction_configure_frame"))
    rest_mgmt_button.grid(column=13, row=11, columnspan=2, sticky=(N, E, W, S))
    rest_mgmt_button.state(['disabled'])

    ass_mgmt_button = ttk.Button(frame, text=MANAGE_ASSIGNMENT_LABEL, command=lambda: gui.event.switch_frame(
        "school_select_frame", "assignment_configure_frame"))
    ass_mgmt_button.grid(column=0, row=13, columnspan=2, sticky=(N, E, W, S))
    ass_mgmt_button.state(['disabled'])

    proc_mgmt_button = ttk.Button(frame, text=PROCESS_LABEL, command=lambda: gui.event.switch_frame(
        "school_select_frame", "process_configure_frame"))
    proc_mgmt_button.grid(column=11, row=13, columnspan=2, sticky=(N, E, W, S))
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
    ui.widgets['classes_mgmt_button'] = classes_mgmt_button
    ui.widgets['rooms_mgmt_button'] = lgst_mgmt_button
    ui.widgets['subjects_mgmt_button'] = sbj_mgmt_button
    ui.widgets['time_mgmt_button'] = time_mgmt_button
    ui.widgets['person_mgmt_button'] = pers_mgmt_button
    ui.widgets['assignment_mgmt_button'] = ass_mgmt_button
    ui.widgets['restriction_mgmt_button'] = rest_mgmt_button
    ui.widgets['process_mgmt_button'] = proc_mgmt_button

    gui.event.populate_school_combo()


def configure_schoolyear_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['schoolyear_configure_frame'] = '800x600'
    root.geometry('800x600')

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # year selection
    year_label = ttk.Label(frame, text=YEAR_SELECT_LABEL)
    year_label.grid(column=0, row=0, sticky=(E, W))

    years_listbox = ttk.Treeview(frame, show="tree", selectmode=EXTENDED, height=5)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=years_listbox.yview)
    years_listbox.configure(yscroll=scrollbar.set)
    years_listbox.grid(column=1, row=0, rowspan=2, sticky=(N, W, E, S))
    scrollbar.configure(command=years_listbox.yview)
    scrollbar.grid(column=2, row=0, rowspan=2, sticky=(N, S))
    years_listbox.bind('<<TreeviewSelect>>', gui.event.year_selected)

    year_add_button = ttk.Button(frame, text=ADD_YEAR_LABEL, command=gui.event.year_add)
    year_add_button.grid(column=11, row=0, sticky=(E, W))
    year_add_button.state(['!disabled'])

    year_delete_button = ttk.Button(frame, text=DELETE_YEAR_LABEL, command=gui.event.year_delete)
    year_delete_button.grid(column=11, row=1, sticky=(E, W))
    year_delete_button.state(['disabled'])

    # section selection
    section_label = ttk.Label(frame, text=SECTION_SELECT_LABEL)
    section_label.grid(column=0, row=2, sticky=(E, W))

    sections_listbox = ttk.Treeview(frame, show="tree", selectmode=EXTENDED, height=5)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=sections_listbox.yview)
    sections_listbox.configure(yscroll=scrollbar.set)
    sections_listbox.grid(column=1, row=2, rowspan=2, sticky=(N, W, E, S))
    scrollbar.configure(command=sections_listbox.yview)
    scrollbar.grid(column=2, row=2, rowspan=2, sticky=(N, S))
    sections_listbox.bind('<<TreeviewSelect>>', gui.event.section_selected)

    section_add_button = ttk.Button(frame, text=ADD_SECTION_LABEL, command=gui.event.section_add)
    section_add_button.grid(column=11, row=2, sticky=(E, W))
    section_add_button.state(['!disabled'])

    section_delete_button = ttk.Button(frame, text=DELETE_SECTION_LABEL, command=gui.event.section_delete)
    section_delete_button.grid(column=11, row=3, sticky=(E, W))
    section_delete_button.state(['disabled'])

    # classes selection
    class_label = ttk.Label(frame, text=CLASS_SELECT_LABEL)
    class_label.grid(column=0, row=4, sticky=(E, W))

    classes_listbox = ttk.Treeview(frame, show="tree", selectmode=EXTENDED, height=15)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=sections_listbox.yview)
    classes_listbox.configure(yscroll=scrollbar.set)
    classes_listbox.grid(column=1, row=4, rowspan=3, sticky=(N, W, E, S))
    scrollbar.configure(command=classes_listbox.yview)
    scrollbar.grid(column=2, row=4, rowspan=4, sticky=(N, S))
    classes_listbox.bind('<<TreeviewSelect>>', gui.event.class_selected)

    class_create_button = ttk.Button(frame, text=CREATE_CLASS_LABEL, command=gui.event.class_create)
    class_create_button.grid(column=11, row=4, sticky=(E, W))
    class_create_button.state(['!disabled'])

    class_create_button = ttk.Button(frame, text=MATCH_CLASS_TIMETABLE_LABEL, command=gui.event.add_class_in_plan)
    class_create_button.grid(column=11, row=5, sticky=(E, W))
    class_create_button.state(['!disabled'])

    class_delete_button = ttk.Button(frame, text=DELETE_CLASS_LABEL, command=gui.event.class_delete)
    class_delete_button.grid(column=11, row=6, sticky=(E, W))
    class_delete_button.state(['disabled'])

    return_button = ttk.Button(frame, text=RETURN_HOME, command=lambda: gui.event.switch_frame(
        "schoolyear_configure_frame", "school_select_frame"))
    return_button.grid(column=0, row=10, columnspan=20, sticky=(N, S))
    return_button.state(['!disabled'])

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
    ui.widgets['year_add_button'] = year_add_button
    ui.widgets['year_delete_button'] = year_delete_button
    ui.widgets['sections_listbox'] = sections_listbox
    ui.widgets['section_add_button'] = section_add_button
    ui.widgets['section_delete_button'] = section_delete_button
    ui.widgets['classes_listbox'] = classes_listbox
    ui.widgets['class_create_button'] = class_create_button
    ui.widgets['class_delete_button'] = class_delete_button

    gui.event.populate_school_configuration()


def configure_room_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['room_configure_frame'] = '800x400'
    root.geometry('800x400')

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # year selection
    room_label = ttk.Label(frame, text=ROOM_SELECT_LABEL)
    room_label.grid(column=0, row=0, sticky=(E, W))

    rooms_listbox = ttk.Treeview(frame, show="tree", selectmode=EXTENDED, height=10)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=rooms_listbox.yview)
    rooms_listbox.configure(yscroll=scrollbar.set)
    rooms_listbox.grid(column=1, row=0, rowspan=2, sticky=(N, W, E, S))
    scrollbar.configure(command=rooms_listbox.yview)
    scrollbar.grid(column=2, row=0, rowspan=2, sticky=(N, S))
    rooms_listbox.bind('<<TreeviewSelect>>', gui.event.room_selected)

    room_add_button = ttk.Button(frame, text=ADD_ROOM_LABEL, command=gui.event.room_create)
    room_add_button.grid(column=11, row=0, sticky=(E, W))
    room_add_button.state(['!disabled'])

    room_delete_button = ttk.Button(frame, text=DELETE_ROOM_LABEL, command=gui.event.room_delete)
    room_delete_button.grid(column=11, row=1, sticky=(E, W))
    room_delete_button.state(['disabled'])

    return_button = ttk.Button(frame, text=RETURN_HOME, command=lambda: gui.event.switch_frame(
        "room_configure_frame", "school_select_frame"))
    return_button.grid(column=0, row=10, columnspan=20, sticky=(N, S))
    return_button.state(['!disabled'])

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

    ui.frames['room_configure_frame'] = frame
    ui.widgets['rooms_listbox'] = rooms_listbox
    ui.widgets['room_add_button'] = room_add_button
    ui.widgets['room_delete_button'] = room_delete_button

    gui.event.populate_room_configuration()


def configure_subject_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['subject_configure_frame'] = '1000x600'
    root.geometry('1000x600')

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # subject selection
    subject_label = ttk.Label(frame, text=SUBJECT_SELECT_LABEL)
    subject_label.grid(column=0, row=0, padx=5, rowspan=20)

    subjects_listbox = ttk.Treeview(frame, show="headings", column=("c1", "c2", "c3"),
                                   selectmode=EXTENDED, height=20)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=subjects_listbox.yview)
    subjects_listbox.configure(yscroll=scrollbar.set)
    subjects_listbox.grid(column=1, row=0, rowspan=3, sticky=(N, W, E, S))
    scrollbar.configure(command=subjects_listbox.yview)
    scrollbar.grid(column=2, row=0, rowspan=3, sticky=(N, S))
    subjects_listbox.bind('<<TreeviewSelect>>', gui.event.subject_selected)

    subjects_listbox.column("#1", anchor=W, stretch=NO, width=200)
    subjects_listbox.heading("#1", text="Materia", command=lambda _col="#1":
        gui.event.treeview_sort_column(subjects_listbox, _col, "Materia", False))
    subjects_listbox.column("#2", anchor=CENTER, stretch=NO, width=80)
    subjects_listbox.heading("#2", text="Ore default", command=lambda _col="#2":
        gui.event.treeview_sort_column(subjects_listbox, _col, "Ore default", False))
    subjects_listbox.column("#3", anchor=CENTER, stretch=NO, width=80)
    subjects_listbox.heading("#3", text="Ore consecutive max", command=lambda _col="#3":
        gui.event.treeview_sort_column(subjects_listbox, _col, "Ore consecutive max", False))
    # bind double-click to edit
    subjects_listbox.bind("<Double-1>", gui.event.subject_edit)

    subject_add_button = ttk.Button(frame, text=EDIT_SUBJECT_LABEL, command=gui.event.subject_edit)
    subject_add_button.grid(column=11, row=0, sticky=(E, W))
    subject_add_button.state(['!disabled'])

    subject_add_button = ttk.Button(frame, text=ADD_SUBJECT_LABEL, command=gui.event.subject_create)
    subject_add_button.grid(column=11, row=1, sticky=(E, W))
    subject_add_button.state(['!disabled'])

    subject_delete_button = ttk.Button(frame, text=DELETE_SUBJECT_LABEL, command=gui.event.subject_delete)
    subject_delete_button.grid(column=11, row=2, sticky=(E, W))
    subject_delete_button.state(['disabled'])

    return_button = ttk.Button(frame, text=RETURN_HOME, command=lambda: gui.event.switch_frame(
        "subject_configure_frame", "school_select_frame"))
    return_button.grid(column=0, row=10, columnspan=20, sticky=(N, S))
    return_button.state(['!disabled'])

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
    frame.columnconfigure(0, minsize=100)
    frame.columnconfigure(1, minsize=width)

    ui.frames['subject_configure_frame'] = frame
    ui.widgets['subjects_listbox'] = subjects_listbox
    ui.widgets['subject_add_button'] = subject_add_button
    ui.widgets['subject_delete_button'] = subject_delete_button

    gui.event.populate_subject_configuration()


def configure_person_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['person_configure_frame'] = '700x500'
    root.geometry('700x500')

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # person selection
    person_label = ttk.Label(frame, text=PERSON_SELECT_LABEL)
    person_label.grid(column=0, row=0, rowspan=2, padx=30, sticky=(N, W, E, S))

    persons_listbox = ttk.Treeview(frame, show="headings", column=("c1", "c2", "c3"),
                                   selectmode=EXTENDED, height=20)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=persons_listbox.yview)
    persons_listbox.configure(yscroll=scrollbar.set)
    persons_listbox.grid(column=1, row=0, rowspan=2, sticky=(N, W, E, S))
    scrollbar.configure(command=persons_listbox.yview)
    scrollbar.grid(column=2, row=0, rowspan=2, sticky=(N, S))
    persons_listbox.bind('<<TreeviewSelect>>', gui.event.person_selected)
    persons_listbox.column("#1", anchor=W, stretch=NO, width=200)
    persons_listbox.heading("#1", text="Nome", command=lambda _col="#1":
        gui.event.treeview_sort_column(persons_listbox, _col, "Nome", False))
    persons_listbox.column("#2", anchor=CENTER, stretch=NO, width=80)
    persons_listbox.heading("#2", text="Tipo", command=lambda _col="#2":
        gui.event.treeview_sort_column(persons_listbox, _col, "Tipo", False))
    persons_listbox.column("#3", anchor=CENTER, stretch=NO, width=80)
    persons_listbox.heading("#3", text="Impersonale", command=lambda _col="#3":
        gui.event.treeview_sort_column(persons_listbox, _col, "Impersonale", False))

    person_add_button = ttk.Button(frame, text=ADD_PERSON_LABEL, command=gui.event.person_create)
    person_add_button.grid(column=11, row=0, sticky=(E, W))
    person_add_button.state(['!disabled'])

    person_delete_button = ttk.Button(frame, text=DELETE_PERSON_LABEL, command=gui.event.person_delete)
    person_delete_button.grid(column=11, row=1, sticky=(E, W))
    person_delete_button.state(['disabled'])

    return_button = ttk.Button(frame, text=RETURN_HOME, command=lambda: gui.event.switch_frame(
        "person_configure_frame", "school_select_frame"))
    return_button.grid(column=0, row=10, columnspan=20, sticky=(N, S))
    return_button.state(['!disabled'])

    ui.frames['person_configure_frame'] = frame
    ui.widgets['persons_listbox'] = persons_listbox
    ui.widgets['person_add_button'] = person_add_button
    ui.widgets['person_delete_button'] = person_delete_button

    gui.event.populate_person_configuration()


def configure_timetable_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['timetable_configure_frame'] = '800x700'
    root.geometry('800x700')

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # plan selection
    time_label = ttk.Label(frame, text=TIMETABLE_SELECT_LABEL)
    time_label.grid(column=0, row=0, sticky=(E, W))

    timetables_var = StringVar()
    timetables_combo = ttk.Combobox(frame, textvariable=timetables_var)
    timetables_combo.grid(column=1, row=0, sticky=(N, W, E, S))
    timetables_combo.bind('<<ComboboxSelected>>', gui.event.timetable_selected)
    timetables_combo['values'] = ['']

    frame.rowconfigure(1, minsize=10)

    s = ttk.Style()
    # Create style for the inner frame
    s.configure('TTFrame.TFrame', background='white', bordercolor='black', border=1, borderwidth=1)
    s.configure('TTFrame.TLabel', background='white')

    timetable_grid_frame = ttk.Frame(frame, padding="12 12 12 12", style='TTFrame.TFrame')
    timetable_grid_frame.grid(column=0, row=2, columnspan=2, sticky=(N, W, E, S))

    for i in range(1, 11):
        l = ttk.Label(timetable_grid_frame, text=str(i), style='TTFrame.TLabel', padding="5 5 5 5")
        l.grid(column=i, row=0, sticky=(N, W, E, S))

    d = 1
    curr_row = 1
    for day in db.model.WeekDayEnum:
        l = ttk.Label(timetable_grid_frame, text=day.value, style='TTFrame.TLabel', padding="5 5 5 5")
        l.grid(column=0, row=curr_row, rowspan=2, sticky=(N, W, E, S))
        for i in range(1, 11):
            var = StringVar(timetable_grid_frame, value="-")
            l = ttk.Entry(timetable_grid_frame, textvariable=var, state=DISABLED, width=5)
            l.grid(column=i, row=curr_row, rowspan=1, sticky=(N, W, E, S))
            ui.variables[f'timetable_hour_{d}_{i}_start'] = var
            var = StringVar(timetable_grid_frame, value="-")
            l = ttk.Entry(timetable_grid_frame, textvariable=var, state=DISABLED, width=5)
            l.grid(column=i, row=curr_row + 1, rowspan=1, sticky=(N, W, E, S))
            ui.variables[f'timetable_hour_{d}_{i}_end'] = var
        curr_row = curr_row + 3
        d = d + 1
    timetable_grid_frame.rowconfigure(3, minsize=5)
    timetable_grid_frame.rowconfigure(6, minsize=5)
    timetable_grid_frame.rowconfigure(9, minsize=5)
    timetable_grid_frame.rowconfigure(12, minsize=5)
    timetable_grid_frame.rowconfigure(15, minsize=5)
    timetable_grid_frame.rowconfigure(18, minsize=5)

    frame.rowconfigure(9, minsize=10)

    l = ttk.Label(frame, text=PLAN_USED_IN, padding="5 5 5 5")
    l.grid(column=0, row=10, sticky=(N, W, E, S))
    # lwidth = l.winfo_reqwidth() * 2
    text_plan_classes = Text(frame, height=8, width=10)
    text_plan_classes.grid(column=1, row=10, columnspan=1, sticky=(W, E))
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=text_plan_classes.yview)
    text_plan_classes.configure(yscroll=scrollbar.set)
    scrollbar.grid(column=1, row=10, sticky=(N, S, E))

    frame.rowconfigure(20, minsize=10)

    return_button = ttk.Button(frame, text=RETURN_HOME, command=lambda: gui.event.switch_frame(
        "timetable_configure_frame", "school_select_frame"))
    return_button.grid(column=0, row=100, columnspan=2, pady=30, sticky=(N, S))
    return_button.state(['!disabled'])

    ui.frames['timetable_configure_frame'] = frame
    ui.frames['timetable_grid_frame'] = timetable_grid_frame
    ui.widgets['timetables_combo'] = timetables_combo
    ui.widgets['text_plan_classes'] = text_plan_classes

    gui.event.populate_timetable_combo()


def configure_assignment_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['assignment_configure_frame'] = '1000x600'
    root.geometry('1000x600')

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # person selection
    assignment_label = ttk.Label(frame, text=ASSIGNMENT_SELECT_LABEL)
    assignment_label.grid(column=0, row=0, rowspan=3, padx=30, sticky=(W, E))

    assignment_listbox = ttk.Treeview(frame, show="headings", column=("c1", "c2", "c3", "c4", "c5"),
                                      selectmode=BROWSE, height=20)
    assignment_listbox.grid(column=1, row=0, rowspan=4, sticky=(N, W, E, S))
    scrollbary = ttk.Scrollbar(frame, orient=VERTICAL, command=assignment_listbox.yview)
    assignment_listbox.configure(yscroll=scrollbary.set)
    scrollbary.configure(command=assignment_listbox.yview)
    scrollbary.grid(column=2, row=0, rowspan=4, sticky=(N, S))
    scrollbarx = ttk.Scrollbar(frame, orient=HORIZONTAL, command=assignment_listbox.xview)
    assignment_listbox.configure(xscroll=scrollbarx.set)
    scrollbarx.configure(command=assignment_listbox.xview)
    scrollbarx.grid(column=1, row=4, rowspan=1, sticky=(E, W))
    # bind double-click to edit
    assignment_listbox.bind("<Double-1>", gui.event.assignment_edit)

    assignment_listbox.bind('<<TreeviewSelect>>', gui.event.assignment_selected)
    assignment_listbox.column("#1", anchor=W, stretch=NO, width=200)
    assignment_listbox.heading("#1", text="Docenti", command=lambda _col="#1": \
        gui.event.treeview_sort_column(assignment_listbox, _col, "Docenti", False))
    assignment_listbox.column("#2", anchor=CENTER, stretch=NO, width=100)
    assignment_listbox.heading("#2", text="Materia", command=lambda _col="#2": \
        gui.event.treeview_sort_column(assignment_listbox, _col, "Materia", False))
    assignment_listbox.column("#3", anchor=CENTER, stretch=NO, width=80)
    assignment_listbox.heading("#3", text="Classe", command=lambda _col="#3": \
        gui.event.treeview_sort_column(assignment_listbox, _col, "Classe", False))
    assignment_listbox.column("#4", anchor=CENTER, stretch=NO, width=80)
    assignment_listbox.heading("#4", text="Ore sett.", command=lambda _col="#4": \
        gui.event.treeview_sort_column(assignment_listbox, _col, "Ore sett.", False))
    assignment_listbox.column("#5", anchor=CENTER, stretch=NO, width=100)
    assignment_listbox.heading("#5", text="Aula", command=lambda _col="#5": \
        gui.event.treeview_sort_column(assignment_listbox, _col, "Aula", False))

    assignment_edit_button = ttk.Button(frame, text=EDIT_ASSIGNMENT_LABEL, command=gui.event.assignment_edit)
    assignment_edit_button.grid(column=11, row=0, padx=30, sticky=(E, W))
    assignment_edit_button.state(['!disabled'])

    assignment_add_button = ttk.Button(frame, text=ADD_ASSIGNMENT_LABEL, command=gui.event.assignment_create)
    assignment_add_button.grid(column=11, row=1, padx=30, sticky=(E, W))
    assignment_add_button.state(['!disabled'])

    assignment_delete_button = ttk.Button(frame, text=DELETE_ASSIGNMENT_LABEL, command=gui.event.assignment_delete)
    assignment_delete_button.grid(column=11, row=2, padx=30, sticky=(E, W))
    assignment_delete_button.state(['!disabled'])

    assignment_duplicate_button = ttk.Button(frame, text=DUPLICATE_ASSIGNMENT_LABEL,
                                             command=gui.event.assignment_duplicate)
    assignment_duplicate_button.grid(column=11, row=3, padx=30, sticky=(E, W))
    assignment_duplicate_button.state(['!disabled'])

    return_button = ttk.Button(frame, text=RETURN_HOME, command=lambda: gui.event.switch_frame(
        "assignment_configure_frame", "school_select_frame"))
    return_button.grid(column=0, row=10, columnspan=20, pady=30, sticky=(N, S))
    return_button.state(['!disabled'])

    ui.frames['assignment_configure_frame'] = frame
    ui.widgets['assignment_listbox'] = assignment_listbox
    ui.widgets['assignment_edit_button'] = assignment_edit_button
    ui.widgets['assignment_add_button'] = assignment_add_button
    ui.widgets['assignment_delete_button'] = assignment_delete_button
    ui.widgets['assignment_duplicate_button'] = assignment_duplicate_button

    gui.event.populate_assignment_configuration()


def configure_restriction_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['restriction_configure_frame'] = '1300x600'
    root.geometry('1300x600')

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # restriction selection
    restriction_label = ttk.Label(frame, text=RESTRICTION_SELECT_LABEL)
    restriction_label.grid(column=0, row=0, rowspan=3, padx=30, sticky=(W, E))

    restriction_listbox = ttk.Treeview(frame, show="headings", column=("c1", "c2"),
                                       selectmode=BROWSE, height=20)
    restriction_listbox.grid(column=1, row=0, rowspan=4, sticky=(N, W, E, S))
    # bind double-click to edit
    restriction_listbox.bind("<Double-1>", gui.event.restriction_edit)

    scrollbary = ttk.Scrollbar(frame, orient=VERTICAL, command=restriction_listbox.yview)
    restriction_listbox.configure(yscroll=scrollbary.set)
    scrollbary.configure(command=restriction_listbox.yview)
    scrollbary.grid(column=2, row=0, rowspan=4, sticky=(N, S))
    scrollbarx = ttk.Scrollbar(frame, orient=HORIZONTAL, command=restriction_listbox.xview)
    restriction_listbox.configure(xscroll=scrollbarx.set)
    scrollbarx.configure(command=restriction_listbox.xview)
    scrollbarx.grid(column=1, row=4, rowspan=1, sticky=(E, W))

    restriction_listbox.bind('<<TreeviewSelect>>', gui.event.restriction_selected)
    restriction_listbox.column("#1", anchor=W, stretch=NO, width=460)
    restriction_listbox.heading("#1", text="Nome", command=lambda _col="#1": \
        gui.event.treeview_sort_column(restriction_listbox, _col, "Nome", False))
    restriction_listbox.column("#2", anchor=CENTER, stretch=NO, width=300)
    restriction_listbox.heading("#2", text="Tipo", command=lambda _col="#2": \
        gui.event.treeview_sort_column(restriction_listbox, _col, "Tipo", False))

    restriction_edit_button = ttk.Button(frame, text=EDIT_RESTRICTION_LABEL, command=gui.event.restriction_edit)
    restriction_edit_button.grid(column=11, row=0, padx=30, sticky=(E, W))
    restriction_edit_button.state(['!disabled'])

    restriction_add_button = ttk.Button(frame, text=ADD_RESTRICTION_LABEL, command=gui.event.restriction_create)
    restriction_add_button.grid(column=11, row=1, padx=30, sticky=(E, W))
    restriction_add_button.state(['!disabled'])

    restriction_delete_button = ttk.Button(frame, text=DELETE_RESTRICTION_LABEL, command=gui.event.restriction_delete)
    restriction_delete_button.grid(column=11, row=2, padx=30, sticky=(E, W))
    restriction_delete_button.state(['!disabled'])

    restriction_duplicate_button = ttk.Button(frame, text=DUPLICATE_RESTRICTION_LABEL,
                                              command=gui.event.restriction_duplicate)
    restriction_duplicate_button.grid(column=11, row=3, padx=30, sticky=(E, W))
    restriction_duplicate_button.state(['!disabled'])

    return_button = ttk.Button(frame, text=RETURN_HOME, command=lambda: gui.event.switch_frame(
        "restriction_configure_frame", "school_select_frame"))
    return_button.grid(column=0, row=10, columnspan=20, pady=30, sticky=(N, S))
    return_button.state(['!disabled'])

    ui.frames['restriction_configure_frame'] = frame
    ui.widgets['restriction_listbox'] = restriction_listbox
    ui.widgets['restriction_edit_button'] = restriction_edit_button
    ui.widgets['restriction_add_button'] = restriction_add_button
    ui.widgets['restriction_delete_button'] = restriction_delete_button
    ui.widgets['restriction_duplicate_button'] = restriction_duplicate_button

    gui.event.populate_restriction_configuration()


def process_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['process_configure_frame'] = '1300x600'
    root.geometry('1300x600')

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # past processes selection
    processes_label = ttk.Label(frame, text=PROCESS_SELECT_LABEL)
    processes_label.grid(column=0, row=0, rowspan=3, padx=30, sticky=(W, E))

    process_listbox = ttk.Treeview(frame, show="headings", column=("c1", "c2", "c3"),
                                   selectmode=BROWSE, height=20)
    process_listbox.grid(column=1, row=0, rowspan=4, sticky=(N, W, E, S))
    # bind double-click to details
    process_listbox.bind("<Double-1>", gui.event.process_detail)

    scrollbary = ttk.Scrollbar(frame, orient=VERTICAL, command=process_listbox.yview)
    process_listbox.configure(yscroll=scrollbary.set)
    scrollbary.configure(command=process_listbox.yview)
    scrollbary.grid(column=2, row=0, rowspan=4, sticky=(N, S))
    scrollbarx = ttk.Scrollbar(frame, orient=HORIZONTAL, command=process_listbox.xview)
    process_listbox.configure(xscroll=scrollbarx.set)
    scrollbarx.configure(command=process_listbox.xview)
    scrollbarx.grid(column=1, row=4, rowspan=1, sticky=(E, W))

    process_listbox.column("#1", anchor=W, stretch=NO, width=360)
    process_listbox.heading("#1", text="Inizio-Fine", command=lambda _col="#1": \
        gui.event.treeview_sort_column(process_listbox, _col, "Inizio-Fine", False))
    process_listbox.column("#2", anchor=CENTER, stretch=NO, width=300)
    process_listbox.heading("#2", text="Tipo", command=lambda _col="#2": \
        gui.event.treeview_sort_column(process_listbox, _col, "Tipo", False))
    process_listbox.column("#3", anchor=CENTER, stretch=NO, width=100)
    process_listbox.heading("#3", text="Stato", command=lambda _col="#3": \
        gui.event.treeview_sort_column(process_listbox, _col, "Stato", False))

    process_detail_button = ttk.Button(frame, text=PROCESS_DETAIL_LABEL, command=gui.event.process_detail)
    process_detail_button.grid(column=11, row=0, padx=30, sticky=(E, W))
    process_detail_button.state(['!disabled'])

    process_new_button = ttk.Button(frame, text=PROCESS_START_LABEL, command=gui.event.process_new)
    process_new_button.grid(column=11, row=1, padx=30, sticky=(E, W))
    process_new_button.state(['!disabled'])

    return_button = ttk.Button(frame, text=RETURN_HOME, command=lambda: gui.event.switch_frame(
        "process_configure_frame", "school_select_frame"))
    return_button.grid(column=0, row=10, columnspan=20, pady=30, sticky=(N, S))
    return_button.state(['!disabled'])

    ui.frames['process_configure_frame'] = frame
    ui.widgets['process_listbox'] = process_listbox
    ui.widgets['process_detail_button'] = process_detail_button
    ui.widgets['process_new_button'] = process_new_button

    gui.event.populate_process_configuration()
