import logging
from tkinter import END

import gui.setup, gui.screen, gui.dialog
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
subjects_dict = {}
timetable_dict = {}
persons_dict = {}

def populate_school_combo():
    ui = gui.setup.SchoolSchedulerGUI()
    for school in db.query.get_schools():
        school_dict[school.name] = school.id
    ui.widgets['schools_combo']['values'] = list(school_dict.keys())
    ui.widgets['schools_combo'].current(0)


def populate_school_configuration():
    ui = gui.setup.SchoolSchedulerGUI()

    years = db.query.get_years(school_id=school_selected_dict['id'])
    years_list = []

    # Clear the treeview list items
    for item in ui.widgets['years_listbox'].get_children():
        ui.widgets['years_listbox'].delete(item)

    for identifier, yid in [(y.identifier, y.id) for y in years]:
        years_list.append((identifier, yid))
    for (identifier, yid) in sorted(years_list, key=itemgetter(0)):
        years_dict[identifier] = yid
        years_dict[yid] = identifier
        ui.widgets['years_listbox'].insert(parent="", index="end", text=identifier, iid=yid)

        # Clear the treeview list items
    for item in ui.widgets['sections_listbox'].get_children():
        ui.widgets['sections_listbox'].delete(item)

    sections = db.query.get_sections(school_id=school_selected_dict['id'])
    sections_list = []
    for identifier, yid in [(y.identifier, y.id) for y in sections]:
        sections_list.append((identifier, yid))
    for (identifier, yid) in sorted(sections_list, key=itemgetter(0)):
        sections_dict[identifier] = yid
        sections_dict[yid] = identifier
        ui.widgets['sections_listbox'].insert(parent="", index="end", text=identifier, iid=yid)

        # Clear the treeview list items
    for item in ui.widgets['classes_listbox'].get_children():
        ui.widgets['classes_listbox'].delete(item)

    classes = db.query.get_classes(schoolyear_id=schoolyear_selected_dict['id'])
    classes_list = []
    for year, section, yid in [(c.year, c.section, c.id) for c in classes]:
        classes_list.append((year.identifier, section.identifier, yid))

    for (year, section, sid) in sorted(classes_list, key=itemgetter(1)):
        if not ui.widgets['classes_listbox'].exists('S' + str(section)):
            ui.widgets['classes_listbox'].insert(parent="", index="end", text=str(section), iid='S' + str(section))

    for (year, section, sid) in sorted(sorted(classes_list, key=itemgetter(1)), key=itemgetter(0)):
        identifier = str(year) + " " + str(section)
        classes_dict[identifier] = sid
        ui.widgets['classes_listbox'].insert(parent='S' + str(section), index="end", text=identifier, iid=sid)


def populate_room_configuration():
    ui = gui.setup.SchoolSchedulerGUI()

    rooms = db.query.get_rooms(school_id=school_selected_dict['id'])
    rooms_list = []

    # Clear the treeview list items
    for item in ui.widgets['rooms_listbox'].get_children():
        ui.widgets['rooms_listbox'].delete(item)

    for identifier, room_type, rid in [(r.identifier, r.room_type, r.id) for r in rooms]:
        rooms_list.append((identifier, room_type, rid))
    ui.widgets['rooms_listbox'].insert(parent="", index="end", text=db.model.RoomEnum.AULA.value, iid="A")
    ui.widgets['rooms_listbox'].insert(parent="", index="end", text=db.model.RoomEnum.LABORATORIO.value, iid="B")
    ui.widgets['rooms_listbox'].insert(parent="", index="end", text=db.model.RoomEnum.PALESTRA.value, iid="C")
    ui.widgets['rooms_listbox'].insert(parent="", index="end", text=db.model.RoomEnum.ALTRO.value, iid="D")

    for (identifier, room_type, rid) in sorted(rooms_list, key=itemgetter(0)):
        rooms_dict[identifier] = id
        if room_type == db.model.RoomEnum.AULA:
            ui.widgets['rooms_listbox'].insert(parent="A", index="end", text=identifier, iid=rid)
        elif room_type == db.model.RoomEnum.LABORATORIO:
            ui.widgets['rooms_listbox'].insert(parent="B", index="end", text=identifier, iid=rid)
        elif room_type == db.model.RoomEnum.PALESTRA:
            ui.widgets['rooms_listbox'].insert(parent="C", index="end", text=identifier, iid=rid)
        elif room_type == db.model.RoomEnum.ALTRO:
            ui.widgets['rooms_listbox'].insert(parent="D", index="end", text=identifier, iid=rid)

def populate_subject_configuration():
    ui = gui.setup.SchoolSchedulerGUI()

    subjects = db.query.get_subjects(school_id=school_selected_dict['id'])
    subjects_list = []

    # Clear the treeview list items
    for item in ui.widgets['subjects_listbox'].get_children():
        ui.widgets['subjects_listbox'].delete(item)

    for subject in subjects:
        subjects_dict[subject.identifier] = subject.id
        ui.widgets['subjects_listbox'].insert(parent="", index="end", text=subject.identifier, iid=subject.id)


def populate_person_configuration():
    ui = gui.setup.SchoolSchedulerGUI()

    persons = db.query.get_persons(school_id=school_selected_dict['id'])
    persons_list = []
    
    # Clear the treeview list items
    for item in ui.widgets['persons_listbox'].get_children():
        ui.widgets['persons_listbox'].delete(item)

    for person in persons:
        if person.is_impersonal:
            fullname = person.fullname + " (I)"
        else:
            fullname = person.fullname
        persons_list.append((fullname, person.person_type, person.id))
        
    ui.widgets['persons_listbox'].insert(parent="", index="end", text=db.model.PersonEnum.DOCENTE.value, iid="A")
    ui.widgets['persons_listbox'].insert(parent="", index="end", text=db.model.PersonEnum.COLLABORATORE.value, iid="B")
    ui.widgets['persons_listbox'].insert(parent="", index="end", text=db.model.PersonEnum.LETTORE.value, iid="C")
    ui.widgets['persons_listbox'].insert(parent="", index="end", text=db.model.PersonEnum.ALTRO.value, iid="D")

    for (fullname, person_type, pid) in sorted(persons_list, key=itemgetter(0)):
        persons_dict[fullname] = id
        if person_type == db.model.PersonEnum.DOCENTE:
            ui.widgets['persons_listbox'].insert(parent="A", index="end", text=fullname, iid=pid)
        elif person_type == db.model.PersonEnum.COLLABORATORE:
            ui.widgets['persons_listbox'].insert(parent="B", index="end", text=fullname, iid=pid)
        elif person_type == db.model.PersonEnum.LETTORE:
            ui.widgets['persons_listbox'].insert(parent="C", index="end", text=fullname, iid=pid)
        elif person_type == db.model.PersonEnum.ALTRO:
            ui.widgets['persons_listbox'].insert(parent="D", index="end", text=fullname, iid=pid)


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
    ui.widgets['schoolyears_combo'].current(0)
    for identifier, sid in [(s.identifier, s.id) for s in schoolyears]:
        schoolyears_dict[identifier] = sid
    ui.widgets['school_delete_button'].state(['disabled'])
    schoolyear_selected(None)


def school_delete():
    pass


def school_add():
    ui = gui.setup.SchoolSchedulerGUI()
    school_name = tkinter.simpledialog.askstring("Aggiungi scuola", "Nome scuola")
    if school_name is not None and school_name != '':
        s = db.model.School()
        s.name = school_name
        if db.query.get_school(s) is not None:
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
    ui.widgets['schoolyear_delete_button'].state(['disabled'])
    ui.widgets['schoolyear_duplicate_button'].state(['disabled'])
    ui.widgets['schoolyear_reset_button'].state(['disabled'])
    ui.widgets['classes_mgmt_button'].state(['!disabled'])
    ui.widgets['subjects_mgmt_button'].state(['!disabled'])
    ui.widgets['rooms_mgmt_button'].state(['!disabled'])
    ui.widgets['time_mgmt_button'].state(['!disabled'])
    ui.widgets['person_mgmt_button'].state(['!disabled'])


def schoolyear_delete():
    pass


def schoolyear_create():
    ui = gui.setup.SchoolSchedulerGUI()
    schoolyear_name = tkinter.simpledialog.askstring("Aggiungi anno scolastico", "Anno Scolastico")
    if schoolyear_name is not None and schoolyear_name != '':
        s = db.model.SchoolYear()
        s.identifier = schoolyear_name
        if db.query.get_schoolyear(s) is not None:
            tkinter.messagebox.showwarning("Aggiunta anno scolastico",
                                           "Anno scolastico " + schoolyear_name + " già presente")
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
    if year_name is not None and year_name != '':
        s = db.model.Year()
        s.identifier = year_name
        if db.query.get_year(s):
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
    if section_name is not None and section_name != '':
        s = db.model.Section()
        s.identifier = section_name
        if db.query.get_section(s) is not None:
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


def add_class_in_plan():
    ui = gui.setup.SchoolSchedulerGUI()

    class_ids = ui.widgets['classes_listbox'].selection()
    class_string = str()
    for class_id in [int(cid) for cid in class_ids if cid.isnumeric()]:
        for class_str in classes_dict.keys():
            if classes_dict[class_str] == class_id:
                class_string = class_string + class_str + ", "
    class_string = class_string[:-2]

    if len(class_string) == 0:
        tkinter.messagebox.showwarning("Abbinamento classi", "Nessuna classe selezionata")
        return None

    for plan in db.query.get_plans(school_id=school_selected_dict['id']):
        timetable_dict[plan.identifier] = plan.id

    dialog = gui.dialog.AddClassInPlanDialog(parent=ui.root, plans=timetable_dict, classes=class_string)

    plan = dialog.result
    if plan:
        plan_id = timetable_dict[plan]
        logging.info(f'assegno il piano ({plan}: {plan_id}) alle classi {class_string}')

        for class_id in [int(cid) for cid in class_ids if cid.isnumeric()]:
            db.query.delete_plan_for_class(class_id)
            cp = db.model.ClassPlan()
            cp.class_id = class_id
            cp.plan_id = plan_id
            db.query.save(cp)

        tkinter.messagebox.showinfo("Abbinamento classi", "Classi abbinate")



def class_delete():
    pass


def class_create():
    ui = gui.setup.SchoolSchedulerGUI()
    schoolyear_id = schoolyear_selected_dict['id']

    year_ids = ui.widgets['years_listbox'].selection()
    year_string = str()
    for year_id in year_ids:
        year_string = year_string + years_dict[int(year_id)] + ", "
    year_string = year_string[:-2]

    section_ids = ui.widgets['sections_listbox'].selection()
    section_string = str()
    for section_id in section_ids:
        section_string = section_string + sections_dict[int(section_id)] + ", "
    section_string = section_string[:-2]

    if len(year_string) == 0 or len(section_string) == 0:
        tkinter.messagebox.showwarning("Creazione classi", "Selezionare almeno un anno e una sezione")
        return None

    confirm = tkinter.messagebox.askokcancel("Creazione classi",
                                             "Confermi di creare le classi per l'Anno Scolastico " + ui.widgets[
                                                 'schoolyears_combo'].get() + ":\n" +
                                             "Anni: " + year_string + ", Sezioni: " + section_string + "?")

    if confirm:
        created = 0
        for year_id in year_ids:
            for section_id in section_ids:
                c = db.model.Class()
                c.school_year_id = int(schoolyear_id)
                c.year_id = int(year_id)
                c.section_id = int(section_id)
                if db.query.get_class(c) is None:
                    db.query.save(c)
                    created = created + 1

        tkinter.messagebox.showinfo("Creazione classi", "Create " + str(created) + " classi")
        populate_school_configuration()


def room_selected(event):
    pass


def room_delete():
    pass


def room_create():
    ui = gui.setup.SchoolSchedulerGUI()
    options = {}
    for t in db.model.RoomEnum:
        options[t.name] = t.value
    dialog = gui.dialog.CreateRoomDialog(ui.root, options=options)
    ret = dialog.result
    if ret:
        rt, identifier = ret
        r = db.model.Room()
        r.identifier = identifier
        r.room_type = rt
        r.school_id = school_selected_dict['id']
        if db.query.get_room(r) is not None:
            tkinter.messagebox.showwarning("Aggiunta spazio",
                                           "Spazio " + identifier + " già presente")
        else:
            db.query.save(r)
            tkinter.messagebox.showinfo("Aggiunta spazio", "Spazio " + identifier + " aggiunto")
        populate_room_configuration()

def subject_selected(event):
    pass


def subject_delete():
    pass


def subject_create():
    subject_name = tkinter.simpledialog.askstring("Aggiungi materia", "Materia")
    if subject_name is not None and subject_name != '':
        subject = db.model.Subject()
        subject.identifier = subject_name
        subject.school_id = school_selected_dict['id']
        if db.query.get_subject(subject) is not None:
            tkinter.messagebox.showwarning("Aggiunta materia",
                                           "Materia " + subject_name + " già presente")
        else:
            db.query.save(subject)
            tkinter.messagebox.showinfo("Aggiunta materia", "Materia " + subject_name + " inserita")

        populate_subject_configuration()

def person_selected(event):
    pass


def person_delete():
    pass


def person_create():
    ui = gui.setup.SchoolSchedulerGUI()
    options = {}
    for t in db.model.PersonEnum:
        options[t.name] = t.value
    dialog = gui.dialog.CreatePersonDialog(ui.root, options=options)
    ret = dialog.result
    if ret:
        pt, fullname, impersonal = ret
        person = db.model.Person()
        person.fullname = fullname
        person.person_type = pt
        person.is_impersonal = impersonal
        person.school_id = school_selected_dict['id']
        if db.query.get_person(person) is not None:
            tkinter.messagebox.showwarning("Aggiunta persona",
                                           fullname + " già presente")
        else:
            db.query.save(person)
            tkinter.messagebox.showinfo("Aggiunta Persona", fullname + " aggiunto")
        populate_person_configuration()

def timetable_selected(event):
    ui = gui.setup.SchoolSchedulerGUI()
    choice = ui.widgets['timetables_combo'].get()
    plan = db.query.get_plan(timetable_dict[choice])

    d = 1
    for day in db.model.WeekDayEnum:
        i = 1
        for daily_hour in plan[day]:
            var_start = ui.variables[f'timetable_hour_{d}_{i}_start']
            var_start.set(daily_hour.hour.start.strftime('%H:%M'))
            var_end = ui.variables[f'timetable_hour_{d}_{i}_end']
            var_end.set(daily_hour.hour.get_end().strftime('%H:%M'))
            i = i + 1
        d = d + 1

    l = ui.widgets['text_plan_classes']
    l.delete('1.0', END)
    classes_str = str()
    for classe in db.query.get_classes_in_plan(timetable_dict[choice]):
        classes_str = classes_str + str(classe.class_) + '\n'
    l.insert("1.0", classes_str)


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
        elif to_name == "subject_configure_frame":
            gui.screen.configure_subject_screen()
        elif to_name == "timetable_configure_frame":
            gui.screen.configure_timetable_screen()
        elif to_name == "person_configure_frame":
            gui.screen.configure_person_screen()
    ui.root.geometry(gui.screen.geometries[to_name])
