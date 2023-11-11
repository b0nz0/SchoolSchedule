import gui.setup, gui.screen
import db.query, db.model

school_dict = {}

def populate_school_combo():
    ui = gui.setup.SchoolSchedulerGUI()
    for school in db.query.get_schools():
        school_dict[school.name] = school.id
    ui.widgets['schools_combo']['values'] = list(school_dict.keys()) 

def school_selected(event):
    ui = gui.setup.SchoolSchedulerGUI()
    choice = ui.widgets['schools_combo'].get()
    # check if choose to add a school
    if choice == gui.screen.NEW_COMBO_LABEL:
        ui.widgets['school_delete_button'].state(['disabled'])
    else:
        school = db.query.get(db.model.School, school_dict[choice])
        schoolyears = db.query.get_schoolyears(school_id=school.id)
        ui.widgets['schoolyears_combo'].grid()
        ui.widgets['schoolyears_label'].grid()
        ui.widgets['schoolyear_add_button'].grid()
        ui.widgets['schoolyear_delete_button'].grid()
        ui.widgets['schoolyear_duplicate_button'].grid()
        ui.widgets['schoolyear_reset_button'].grid()
        ui.widgets['schoolyears_combo']['values'] = list([s.identifier for s in schoolyears]) 
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

