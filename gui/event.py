import gui.setup, gui.screen
import db.query, db.model
from operator import itemgetter

school_dict = {}
schoolyears_dict = {}
school_selected_dict = {}
schoolyear_selected_dict = {}
years_dict = {}
sections_dict = {}
classes_dict = {}

def populate_school_combo():
    ui = gui.setup.SchoolSchedulerGUI()
    for school in db.query.get_schools():
        school_dict[school.name] = school.id
    ui.widgets['schools_combo']['values'] = list(school_dict.keys()) 

def populate_school_configuration():
    ui = gui.setup.SchoolSchedulerGUI()

    years = db.query.get_years(school_id=school_selected_dict['id'])
    years_list = []
    for identifier, id in [(y.identifier, y.id) for y in years]:
        years_list.append((identifier, id))
    for (identifier, id) in sorted(years_list, key=itemgetter(0)):
        years_dict[identifier] = id
        ui.widgets['years_listbox'].insert(parent="", index="end", text=identifier, iid=id) 

    sections = db.query.get_sections(school_id=school_selected_dict['id'])
    sections_list = []
    for identifier, id in [(y.identifier, y.id) for y in sections]:
        sections_list.append((identifier, id))
    for (identifier, id) in sorted(sections_list, key=itemgetter(0)):
        sections_dict[identifier] = id
        ui.widgets['sections_listbox'].insert(parent="", index="end", text=identifier, iid=id) 

    classes = db.query.get_classes(schoolyear_id=schoolyear_selected_dict['id'])
    classes_list = []
    for year, section, id in [(c.year, c.section, c.id) for c in classes]:
        classes_list.append((year.identifier, section.identifier, id))

    for (year, section, id) in sorted(classes_list, key=itemgetter(1)):
        if not ui.widgets['classes_listbox'].exists(str(section)): 
            ui.widgets['classes_listbox'].insert(parent="", index="end", text=str(section), iid=str(section)) 

    for (year, section, id) in sorted(sorted(classes_list, key=itemgetter(1)), key=itemgetter(0)):
        identifier = str(year) + " " + str(section)
        classes_dict[identifier] = id
        ui.widgets['classes_listbox'].insert(parent=str(section), index="end", text=identifier, iid=id) 

def populate_room_configuration():
    ui = gui.setup.SchoolSchedulerGUI()


def school_selected(event):
    ui = gui.setup.SchoolSchedulerGUI()
    choice = ui.widgets['schools_combo'].get()
    school = db.query.get(db.model.School, school_dict[choice])
    school_selected_dict['name'] = choice
    school_selected_dict['id'] = school_dict[choice]
    schoolyears = db.query.get_schoolyears(school_id=school.id)
    ui.widgets['schoolyears_combo'].grid()
    ui.widgets['schoolyears_label'].grid()
    ui.widgets['schoolyear_add_button'].grid()
    ui.widgets['schoolyear_delete_button'].grid()
    ui.widgets['schoolyear_duplicate_button'].grid()
    ui.widgets['schoolyear_reset_button'].grid()
    ui.widgets['schoolyears_combo']['values'] = list([s.identifier for s in schoolyears]) 
    for identifier, id in [(s.identifier, s.id) for s in schoolyears]:
        schoolyears_dict[identifier] = id
    ui.widgets['school_delete_button'].state(['!disabled'])

def school_delete():
    pass

def school_add():
    pass

def schoolyear_selected(event):
    ui = gui.setup.SchoolSchedulerGUI()
    choice = ui.widgets['schoolyears_combo'].get()
    schoolyear = db.query.get(db.model.SchoolYear, schoolyears_dict[choice])
    schoolyear_selected_dict['name'] = choice
    schoolyear_selected_dict['id'] = schoolyears_dict[choice]
    ui.widgets['schoolyear_delete_button'].state(['!disabled'])
    ui.widgets['schoolyear_duplicate_button'].state(['!disabled'])
    ui.widgets['schoolyear_reset_button'].state(['!disabled'])
    ui.widgets['classes_mgmt_button'].state(['!disabled'])
    ui.widgets['rooms_mgmt_button'].state(['!disabled'])
    
def schoolyear_delete():
    pass

def schoolyear_add():
    pass

def year_selected(event):
    pass
    
def year_delete():
    pass

def year_add():
    pass

def section_selected(event):
    pass
    
def section_delete():
    pass

def section_add():
    pass

def class_selected(event):
    ui = gui.setup.SchoolSchedulerGUI()
    selected = ui.widgets['classes_listbox'].selection()
    for item in selected:
        pass
    
def class_delete():
    pass

def class_create():
    pass

def room_selected(event):
    pass

def room_delete():
    pass

def room_create():
    pass

def return_home():
    switch_frame(None, 'school_select_frame')

def switch_frame(from_name, to_name):
    ui = gui.setup.SchoolSchedulerGUI()
    if from_name in ui.frames:
        from_frame = ui.frames[from_name]
        from_frame.grid_remove()
    else:
        from_frame = None
    if to_name in ui.frames:
        to_frame = ui.frames[to_name]
        to_frame.grid()
    else:
        if to_name == "schoolyear_configure_frame":
            gui.screen.configure_schoolyear_screen()
        elif to_name == "room_configure_frame":
            gui.screen.configure_room_screen()
    ui.root.geometry(gui.screen.geometries[to_name])

    
