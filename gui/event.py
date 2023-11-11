import gui.setup, gui.screen
import db.query, db.model

school_dict = {}
schoolyears_dict = {}

def populate_school_combo():
    ui = gui.setup.SchoolSchedulerGUI()
    for school in db.query.get_schools():
        school_dict[school.name] = school.id
    ui.widgets['schools_combo']['values'] = list(school_dict.keys()) 

def populate_school_configuration():
    ui = gui.setup.SchoolSchedulerGUI()
    if 'schools_combo' in ui.widgets:
        choice = ui.widgets['schools_combo'].get()
        school = db.query.get(db.model.School, school_dict[choice])
        years = db.query.get_years(school_id=school.id)


def school_selected(event):
    ui = gui.setup.SchoolSchedulerGUI()
    choice = ui.widgets['schools_combo'].get()
    school = db.query.get(db.model.School, school_dict[choice])
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
    ui.widgets['schoolyear_delete_button'].state(['!disabled'])
    ui.widgets['schoolyear_duplicate_button'].state(['!disabled'])
    ui.widgets['schoolyear_reset_button'].state(['!disabled'])
    ui.widgets['classes_mgmt_button'].state(['!disabled'])
    
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
    
