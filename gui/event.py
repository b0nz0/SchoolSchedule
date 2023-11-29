import gui.setup, gui.screen
import db.query, db.model
from operator import itemgetter
import tkinter.simpledialog, tkinter.messagebox
import datetime

school_dict = {}
schoolyears_dict = {}
school_selected_dict = {}
schoolyear_selected_dict = {}
years_dict = {}
sections_dict = {}
classes_dict = {}
rooms_dict = {}
timetable_dict = {}

def populate_school_combo():
    ui = gui.setup.SchoolSchedulerGUI()
    for school in db.query.get_schools():
        school_dict[school.name] = school.id
    ui.widgets['schools_combo']['values'] = list(school_dict.keys()) 

def populate_school_configuration():
    ui = gui.setup.SchoolSchedulerGUI()

    years = db.query.get_years(school_id=school_selected_dict['id'])
    years_list = []

    #Clear the treeview list items
    for item in ui.widgets['years_listbox'].get_children():
        ui.widgets['years_listbox'].delete(item)
    
    for identifier, id in [(y.identifier, y.id) for y in years]:
        years_list.append((identifier, id))
    for (identifier, id) in sorted(years_list, key=itemgetter(0)):
        years_dict[identifier] = id
        years_dict[id] = identifier
        ui.widgets['years_listbox'].insert(parent="", index="end", text=identifier, iid=id) 

    #Clear the treeview list items
    for item in ui.widgets['sections_listbox'].get_children():
        ui.widgets['sections_listbox'].delete(item)

    sections = db.query.get_sections(school_id=school_selected_dict['id'])
    sections_list = []
    for identifier, id in [(y.identifier, y.id) for y in sections]:
        sections_list.append((identifier, id))
    for (identifier, id) in sorted(sections_list, key=itemgetter(0)):
        sections_dict[identifier] = id
        sections_dict[id] = identifier
        ui.widgets['sections_listbox'].insert(parent="", index="end", text=identifier, iid=id) 

    #Clear the treeview list items
    for item in ui.widgets['classes_listbox'].get_children():
        ui.widgets['classes_listbox'].delete(item)

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

    rooms = db.query.get_rooms(school_id=school_selected_dict['id'])
    rooms_list = []
    
    #Clear the treeview list items
    for item in ui.widgets['rooms_listbox'].get_children():
        ui.widgets['rooms_listbox'].delete(item)

    
    for identifier, room_type, id in [(r.identifier, r.room_type, r.id) for r in rooms]:
        rooms_list.append((identifier, room_type, id))
    ui.widgets['rooms_listbox'].insert(parent="", index="end", text=db.model.RoomEnum.AULA.value, iid=1)
    ui.widgets['rooms_listbox'].insert(parent="", index="end", text=db.model.RoomEnum.LABORATORIO.value, iid=2)
    ui.widgets['rooms_listbox'].insert(parent="", index="end", text=db.model.RoomEnum.PALESTRA.value, iid=3)
    ui.widgets['rooms_listbox'].insert(parent="", index="end", text=db.model.RoomEnum.ALTRO.value, iid=4)

    for (identifier, room_type, id) in sorted(rooms_list, key=itemgetter(0)):
        rooms_dict[identifier] = id
        if room_type == db.model.RoomEnum.AULA:
            ui.widgets['rooms_listbox'].insert(parent=1, index="end", text=identifier, iid=id)
        elif room_type == db.model.RoomEnum.LABORATORIO:
            ui.widgets['rooms_listbox'].insert(parent=2, index="end", text=identifier, iid=id)
        elif room_type == db.model.RoomEnum.PALESTRA:
            ui.widgets['rooms_listbox'].insert(parent=3, index="end", text=identifier, iid=id)
        elif room_type == db.model.RoomEnum.ALTRO:
            ui.widgets['rooms_listbox'].insert(parent=4, index="end", text=identifier, iid=id)

def populate_timetable_combo():
    ui = gui.setup.SchoolSchedulerGUI()
    for plan in db.query.get_plans(school_id=school_selected_dict['id']):
        timetable_dict[plan.identifier] = plan.id
    ui.widgets['timetables_combo']['values'] = list(timetable_dict.keys()) 


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
    ui = gui.setup.SchoolSchedulerGUI()
    school_name = tkinter.simpledialog.askstring("Aggiungi scuola", "Nome scuola")
    if school_name != None and school_name != '':
        s = db.model.School()
        s.name = school_name
        if (db.query.get_school(s) != None):
            tkinter.messagebox.showwarning("Aggiunta scuola", "Scuola " + school_name + " già presente")
        else:
            db.query.save(s)
            ui.frames['school_select_frame'].destroy()
            gui.screen.school_select_screen()
            tkinter.messagebox.showinfo("Aggiunta scuola", "Scuola " + school_name + " inserita")

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
    ui.widgets['time_mgmt_button'].state(['!disabled'])
    
def schoolyear_delete():
    pass

def schoolyear_add():
    ui = gui.setup.SchoolSchedulerGUI()
    schoolyear_name = tkinter.simpledialog.askstring("Aggiungi anno scolastico", "Anno Scolastico")
    if schoolyear_name != None and schoolyear_name != '':
        s = db.model.SchoolYear()
        s.identifier = schoolyear_name
        if (db.query.get_schoolyear(s) != None):
            tkinter.messagebox.showwarning("Aggiunta anno scolastico", "Anno scolastico " + schoolyear_name + " già presente")
        else:
            s.school_id = school_selected_dict['id']
            db.query.save(s)
            ui.frames['school_select_frame'].destroy()
            gui.screen.school_select_screen()
            tkinter.messagebox.showinfo("Aggiunta anno scolastico", "Anno scolastico " + schoolyear_name + " inserito")

def year_selected(event):
    pass
    
def year_delete():
    pass

def year_add():
    ui = gui.setup.SchoolSchedulerGUI()
    year_name = tkinter.simpledialog.askstring("Aggiungi anno", "Anno")
    if year_name != None and year_name != '':
        s = db.model.Year()
        s.identifier = year_name
        if (db.query.get_year(s)):
            tkinter.messagebox.showwarning("Aggiunta anno ", "Anno " + year_name + " già presente")
        else:
            s.school_id = school_selected_dict['id']
            db.query.save(s)
            ui.frames['school_select_frame'].destroy()
            gui.screen.school_select_screen()
            tkinter.messagebox.showinfo("Aggiunta anno", "Anno " + year_name + " inserito")

def section_selected(event):
    pass
    
def section_delete():
    pass

def section_add():
    ui = gui.setup.SchoolSchedulerGUI()
    section_name = tkinter.simpledialog.askstring("Aggiungi sezione", "Sezione")
    if section_name != None and section_name != '':
        s = db.model.Year()
        s.identifier = section_name
        if (db.query.get_section(s) != None):
            tkinter.messagebox.showwarning("Aggiunta sezione", "Sezione " + section_name + " già presente")
        else:
            s.school_id = school_selected_dict['id']
            db.query.save(s)
            ui.frames['school_select_frame'].destroy()
            gui.screen.school_select_screen()
            tkinter.messagebox.showinfo("Aggiunta sezione", "Sezione " + section_name + " inserita")

def class_selected(event):
    ui = gui.setup.SchoolSchedulerGUI()
    selected = ui.widgets['classes_listbox'].selection()
    for item in selected:
        pass
    
def class_delete():
    pass

def class_create():
    ui = gui.setup.SchoolSchedulerGUI()
    schoolyear_id = schoolyear_selected_dict['id']

    year_ids = ui.widgets['years_listbox'].selection()
    year_string = str()
    for year_id in year_ids:
        year_string = year_string + years_dict[int(year_id)] +", "
    year_string = year_string[:-2]

    section_ids = ui.widgets['sections_listbox'].selection()
    section_string = str()
    for section_id in section_ids:
        section_string = section_string + sections_dict[int(section_id)] +", "
    section_string = section_string[:-2]

    confirm = tkinter.messagebox.askokcancel("Creazione classi", \
            "Confermi di creare le classi per l'Anno Scolastico " + ui.widgets['schoolyears_combo'].get() + ":\n" + \
            "Anni: " + year_string + ", Sezioni: " + section_string +"?")
    
    if confirm:        
        created = 0
        for year_id in year_ids:
            for section_id in section_ids:
                c = db.model.Class()
                c.school_year_id = int(schoolyear_id)
                c.year_id = int(year_id)
                c.section_id = int(section_id)
                if db.query.get_class(c) == None:
                    db.query.save(c)
                    created = created + 1
        
        tkinter.messagebox.showinfo("Creazione classi", "Create " + str(created) + " classi")
        populate_school_configuration()    
    
    

def room_selected(event):
    pass

def room_delete():
    pass

def room_create():
    pass

def timetable_selected(event):
    ui = gui.setup.SchoolSchedulerGUI()
    choice = ui.widgets['timetables_combo'].get()
    plan = db.query.get_plan(timetable_dict[choice])

    d = 1
    for day in [db.model.WeekDayEnum.MONDAY,
                db.model.WeekDayEnum.TUESDAY,
                db.model.WeekDayEnum.WEDNESDAY,
                db.model.WeekDayEnum.THURSDAY,
                db.model.WeekDayEnum.FRIDAY,
                db.model.WeekDayEnum.SATURDAY,
                db.model.WeekDayEnum.SUNDAY,
                ]:
        i = 1
        for hour in plan[day]:
            var_start = ui.variables[f'timetable_hour_{d}_{i}_start']
            var_start.set(hour.start.strftime('%H:%M'))
            var_end = ui.variables[f'timetable_hour_{d}_{i}_end']
            dt = datetime.datetime(1970, 1, 1, hour=hour.start.hour, minute=hour.start.minute)
            tt = dt + datetime.timedelta(minutes=hour.minutes)
            var_end.set(tt.strftime('%H:%M'))
            i = i + 1
        d = d + 1
        
    

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
        elif to_name == "timetable_configure_frame":
            gui.screen.configure_timetable_screen()
    ui.root.geometry(gui.screen.geometries[to_name])

    
