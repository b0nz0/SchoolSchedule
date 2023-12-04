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
MANAGE_RESTRICTIONS_LABEL = "Gestisci vincoli"
PROCESS_LABEL = "Elabora calendari"

geometries = {}

YEAR_SELECT_LABEL = "Anni"
SECTION_SELECT_LABEL = "Sezioni"
CLASS_SELECT_LABEL = "Classi"

ROOM_SELECT_LABEL = "Spazi"
ADD_ROOM_LABEL = "Aggiungi spazio"
DELETE_ROOM_LABEL = "Elimina spazio"

TIMETABLE_SELECT_LABEL = "Piani orari"
START_END = "IN/FI"
PLAN_USED_IN = "Piano usato in"

def school_select_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['school_select_frame'] = '1200x400'
    root.geometry('1200x400')

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

    classes_mgmt_button = ttk.Button(frame, text=MANAGE_CLASSES_LABEL, command=lambda: gui.event.switch_frame(\
        "school_select_frame", "schoolyear_configure_frame"))
    classes_mgmt_button.grid(column=0, row=10, columnspan=2, sticky=(N, E, W, S))
    classes_mgmt_button.state(['disabled'])
    
    lgst_mgmt_button = ttk.Button(frame, text=MANAGE_LOGISTIC_LABEL, command=lambda: gui.event.switch_frame(\
        "school_select_frame", "room_configure_frame"))
    lgst_mgmt_button.grid(column=11, row=10, columnspan=2, sticky=(N, E, W, S))
    lgst_mgmt_button.state(['disabled'])
    
    sbj_mgmt_button = ttk.Button(frame, text=MANAGE_SUBJECTS_LABEL)
    sbj_mgmt_button.grid(column=13, row=10, columnspan=2, sticky=(N, E, W, S))
    sbj_mgmt_button.state(['disabled'])
    
    pers_mgmt_button = ttk.Button(frame, text=MANAGE_PERSONS_LABEL)
    pers_mgmt_button.grid(column=0, row=11, columnspan=2, sticky=(N, E, W, S))
    pers_mgmt_button.state(['disabled'])
    
    time_mgmt_button = ttk.Button(frame, text=MANAGE_TIMETABLE_LABEL, command=lambda: gui.event.switch_frame(\
        "school_select_frame", "timetable_configure_frame"))
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
    ui.widgets['classes_mgmt_button'] = classes_mgmt_button
    ui.widgets['rooms_mgmt_button'] = lgst_mgmt_button
    ui.widgets['time_mgmt_button'] = time_mgmt_button

    gui.event.populate_school_combo()

def configure_schoolyear_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['schoolyear_configure_frame'] = '800x600'
    root.geometry('800x600')

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    #year selection
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

    #section selection
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

    #classes selection
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

    return_button = ttk.Button(frame, text=RETURN_HOME, command=lambda: gui.event.switch_frame(\
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
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    #year selection
    room_label = ttk.Label(frame, text=ROOM_SELECT_LABEL)
    room_label.grid(column=0, row=0, sticky=(E, W))

    rooms_listbox = ttk.Treeview(frame, show="tree", selectmode=EXTENDED, height=10)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=rooms_listbox.yview)
    rooms_listbox.configure(yscroll=scrollbar.set)
    rooms_listbox.grid(column=1, row=0, rowspan=2, sticky=(N, W, E, S))
    scrollbar.configure(command=rooms_listbox.yview)
    scrollbar.grid(column=2, row=0, rowspan=2, sticky=(N, S))
    rooms_listbox.bind('<<TreeviewSelect>>', gui.event.room_selected)

    room_add_button = ttk.Button(frame, text=ADD_YEAR_LABEL, command=gui.event.year_add)
    room_add_button.grid(column=11, row=0, sticky=(E, W))
    room_add_button.state(['!disabled'])

    room_delete_button = ttk.Button(frame, text=DELETE_YEAR_LABEL, command=gui.event.year_delete)
    room_delete_button.grid(column=11, row=1, sticky=(E, W))
    room_delete_button.state(['disabled'])

    return_button = ttk.Button(frame, text=RETURN_HOME, command=lambda: gui.event.switch_frame(\
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

def configure_timetable_screen():
    ui = gui.setup.SchoolSchedulerGUI()
    root = ui.root
    global geometries
    geometries['timetable_configure_frame'] = '800x700'
    root.geometry('800x700')

    frame = ttk.Frame(root, padding="3 3 12 12")
    frame.grid(column=0, row=0, sticky=(N, W, E, S))
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    
    #plan selection
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
            var = StringVar(timetable_grid_frame, value="00:00")
            l = ttk.Entry(timetable_grid_frame, textvariable=var, state=DISABLED, width=5)
            l.grid(column=i, row=curr_row, rowspan=1, sticky=(N, W, E, S))
            ui.variables[f'timetable_hour_{d}_{i}_start'] = var
            var = StringVar(timetable_grid_frame, value="00:00")
            l = ttk.Entry(timetable_grid_frame, textvariable=var, state=DISABLED, width=5)
            l.grid(column=i, row=curr_row+1, rowspan=1, sticky=(N, W, E, S))
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

    l = ttk.Label(frame, text=PLAN_USED_IN, padding= "5 5 5 5")
    l.grid(column=0, row=10, sticky=(N, W, E, S))
    lwidth = l.winfo_reqwidth() * 2
    text_plan_classes = Text(frame, height=8, width=10)
    text_plan_classes.grid(column=1, row=10, columnspan=1, sticky=(W, E))
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=text_plan_classes.yview)
    text_plan_classes.configure(yscroll=scrollbar.set)
    scrollbar.grid(column=1, row=10, sticky=(N, S, E))

    frame.rowconfigure(20, minsize=10)

    return_button = ttk.Button(frame, text=RETURN_HOME, command=lambda: gui.event.switch_frame(\
        "timetable_configure_frame", "school_select_frame"))    
    return_button.grid(column=0, row=100, columnspan=2, sticky=(N, S))
    return_button.state(['!disabled'])
        
    ui.frames['timetable_configure_frame'] = frame
    ui.frames['timetable_grid_frame'] = timetable_grid_frame
    ui.widgets['timetables_combo'] = timetables_combo
    ui.widgets['text_plan_classes'] = text_plan_classes
    
    gui.event.populate_timetable_combo()
