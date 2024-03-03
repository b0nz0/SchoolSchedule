import logging
import tkinter.messagebox
import tkinter.simpledialog
from datetime import datetime
from operator import itemgetter
from tkinter import END

import db.model
import db.query
import engine.struct
from engine import simple_engine, simple_engine_rand, local_optimal, process_coordinator
import gui.constraint_dialog
import gui.dialog
import gui.screen
import gui.setup

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
assignment_dict = {}
assignment_list = []
restriction_list = []
process_list = []

def treeview_sort_column(tv, col, text, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, text=text, command=lambda _col=col: \
        treeview_sort_column(tv, _col, text, not reverse))


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
        def_h = ''
        if subject.default_hours:
            def_h = str(subject.default_hours)
        con_h = ''
        if subject.preferred_consecutive_hours:
            con_h = str(subject.preferred_consecutive_hours)
        ui.widgets['subjects_listbox'].insert(parent="", index="end", iid=subject.id,
                                              values=(subject.identifier, def_h, con_h))
        subjects_list.append((subject.identifier, def_h, con_h))


def populate_person_configuration():
    ui = gui.setup.SchoolSchedulerGUI()

    persons = db.query.get_persons(school_id=school_selected_dict['id'])
    persons_list = []

    # Clear the treeview list items
    for item in ui.widgets['persons_listbox'].get_children():
        ui.widgets['persons_listbox'].delete(item)

    for person in persons:
        imp = ''
        if person.is_impersonal:
            imp = '(I)'
        ui.widgets['persons_listbox'].insert(parent="", index="end", iid=person.id,
                                             values=(person.fullname, person.person_type.value, imp))
        persons_list.append((person.fullname, person.person_type, person.id))


def populate_assignment_configuration():
    ui = gui.setup.SchoolSchedulerGUI()

    subj_in_classes = db.query.get_subjects_in_class_per_school_year(school_year_id=schoolyear_selected_dict['id'])
    global assignment_list
    assignment_list = []

    tot_hours_in_class = dict()
    for subj_in_class_id in subj_in_classes:
        subj_in_class = db.query.get(db.model.SubjectInClass, subj_in_class_id)
        class_id = subj_in_class.class_id
        if class_id not in tot_hours_in_class.keys():
            tot_hours_in_class[class_id] = 0
        tot_hours_in_class[class_id] += subj_in_class.hours_total
        
    # Clear the treeview list items
    for item in ui.widgets['assignment_listbox'].get_children():
        ui.widgets['assignment_listbox'].delete(item)

    for subj_in_class_id in subj_in_classes:
        subj_in_class = db.query.get(db.model.SubjectInClass, subj_in_class_id)
        persons = ','.join(list([x.fullname for x in subj_in_class.persons]))
        subject = subj_in_class.subject.identifier
        classe = f'{subj_in_class.class_.year.identifier} {subj_in_class.class_.section.identifier} ({tot_hours_in_class[subj_in_class.class_id]})'
        hours = subj_in_class.hours_total
        if subj_in_class.room is not None:
            room = subj_in_class.room.identifier
        else:
            room = ''
        assignment_list.append((subj_in_class_id, persons, subject, classe, hours, room))

    for ass in assignment_list:
        ui.widgets['assignment_listbox'].insert(parent="", index="end", iid=ass[0],
                                                values=ass[1:])


def populate_restriction_configuration():
    ui = gui.setup.SchoolSchedulerGUI()

    restrictions = db.query.get_constraints(school_year_id=schoolyear_selected_dict['id'])
    global restriction_list
    restriction_list = []

    # Clear the treeview list items
    for item in ui.widgets['restriction_listbox'].get_children():
        ui.widgets['restriction_listbox'].delete(item)

    for restriction in restrictions:
        identifier = restriction.identifier
        type_name = type(restriction).__name__
        type_ = None
        for ckind in engine.struct.Constraint.REGISTERED_CONSTRAINTS:
            if type_name == ckind['classname']:
                type_ = ckind['longname']
                break
        assert type_ is not None, 'impossibile trovare il tipo della restrizione'
        score = restriction.score
        restriction_list.append((restriction.id, identifier, type_, score))

    for res in restriction_list:
        ui.widgets['restriction_listbox'].insert(parent="", index="end", iid=res[0],
                                                 values=res[1:])


def populate_timetable_combo():
    ui = gui.setup.SchoolSchedulerGUI()
    for plan in db.query.get_plans(school_id=school_selected_dict['id']):
        timetable_dict[plan.identifier] = plan.id
    ui.widgets['timetables_combo']['values'] = list(timetable_dict.keys())

def populate_process_configuration():
    ui = gui.setup.SchoolSchedulerGUI()

    processes = db.query.get_processes(school_year_id=schoolyear_selected_dict['id'])
    global process_list
    process_list = []

    # Clear the treeview list items
    for item in ui.widgets['process_listbox'].get_children():
        ui.widgets['process_listbox'].delete(item)

    for process in processes:
        status = process.status
        type_ = process.kind
        date_start = '<>' if process.date_start is None else \
            process.date_start.strftime('%d/%m/%Y %H:%M:%S')
        date_end = '<>' if process.date_end is None else \
            process.date_end.strftime('%d/%m/%Y %H:%M:%S')
        dates = f'{date_start} - {date_end}'
        process_list.append((process.id, dates, type_, status))

    for res in process_list:
        ui.widgets['process_listbox'].insert(parent="", index="end", iid=res[0],
                                                 values=res[1:])

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
    ui.widgets['assignment_mgmt_button'].state(['!disabled'])
    ui.widgets['restriction_mgmt_button'].state(['!disabled'])
    ui.widgets['process_mgmt_button'].state(['!disabled'])


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
            # ui.frames['school_select_frame'].destroy()
            # gui.screen.school_select_screen()
            tkinter.messagebox.showinfo("Aggiunta sezione", "Sezione " + section_name + " inserita")

    populate_school_configuration()


def class_selected(event):
    ui = gui.setup.SchoolSchedulerGUI()
    selected = ui.widgets['classes_listbox'].selection()


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


def subject_edit(event=None):
    ui = gui.setup.SchoolSchedulerGUI()
    subjects_ids = ui.widgets['subjects_listbox'].selection()
    if len(subjects_ids) == 0:
        tkinter.messagebox.showwarning("Modifica materia", "Selezionare una materia")
        return None

    for subject_id in subjects_ids:
        subject = db.query.get(db.model.Subject, subject_id)
        dialog = gui.dialog.CreateSubjectDialog(ui.root, subject=subject)
        ret = dialog.result
        if ret is not None:
            db.query.save(ret)
            tkinter.messagebox.showinfo("Modifica materia", "Materia modificata correttamente")

        populate_subject_configuration()


def subject_create():
    ui = gui.setup.SchoolSchedulerGUI()
    dialog = gui.dialog.CreateSubjectDialog(ui.root, subject=None)
    subject = dialog.result
    if subject:
        subject.school_id = school_selected_dict['id']
        if db.query.get_subject(subject) is not None:
            tkinter.messagebox.showwarning("Aggiunta materia",
                                           "Materia " + subject.identifier + " già presente")
        else:
            db.query.save(subject)
            tkinter.messagebox.showinfo("Aggiunta materia", "Materia " + subject.identifier + " inserita")

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
        classes_str = classes_str + classe.class_.long_repr() + '\n'
    l.insert("1.0", classes_str)


def assignment_selected(event):
    pass


def assignment_edit(event=None):
    ui = gui.setup.SchoolSchedulerGUI()
    assignment_ids = ui.widgets['assignment_listbox'].selection()
    if len(assignment_ids) == 0:
        tkinter.messagebox.showwarning("Modifica assegnazione", "Selezionare una assegnazione")
        return None

    for assignment_id in assignment_ids:
        assignment = db.query.get(db.model.SubjectInClass, assignment_id)
        options_person = {}
        options_subject = {}
        options_class = {}
        options_room = {}

        school_id = school_selected_dict['id']
        schoolyear_id = schoolyear_selected_dict['id']

        persons = db.query.get_persons(school_id)
        subjects = db.query.get_subjects(school_id)
        classes = db.query.get_classes(schoolyear_id)
        rooms = db.query.get_rooms(school_id)

        for person in persons:
            options_person[person.id] = person.fullname
        for subject in subjects:
            options_subject[subject.id] = (subject.identifier, subject.default_hours)
        for class_ in classes:
            ident = f'{class_.year.identifier} {class_.section.identifier}'
            options_class[class_.id] = ident
        for room in rooms:
            options_room[room.id] = room.identifier

        # sort by class identifiers
        options_class = dict(sorted(options_class.items(), key=lambda x: x[1]))

        dialog = gui.dialog.EditAssignmentDialog(ui.root, assignment=assignment,
                                                 options_persons=options_person, options_subject=options_subject,
                                                 options_class=options_class, options_room=options_room)
        ret = dialog.result
        if ret is not None:
            db.query.save(ret)
            # tkinter.messagebox.showinfo("Modifica assegnazione", "Assegnazione modificata correttamente")

            populate_assignment_configuration()


def assignment_delete():
    ui = gui.setup.SchoolSchedulerGUI()

    assignment_ids = ui.widgets['assignment_listbox'].selection()
    if len(assignment_ids) == 0:
        tkinter.messagebox.showwarning("Eliminazione assegnazione", "Selezionare una assegnazione")
        return None

    for assignment_id in assignment_ids:
        for assignment in assignment_list:
            if assignment[0] == int(assignment_id):
                confirm = tkinter.messagebox.askokcancel("Eliminazione assegnazione",
                                                         f'Confermi di eliminare l\'assegnazione di {assignment[1]} per \
                                                 {assignment[2]} in classe {assignment[3]}?')

                if confirm:
                    db.query.delete(db.model.SubjectInClass, assignment_id)
                    tkinter.messagebox.showinfo("Eliminazione assegnazione", "Assegnazione eliminata")

                break

    populate_assignment_configuration()


def assignment_create():
    return _assignment_create()


def _assignment_create(pperson1=None, pperson2=None, pperson3=None, psubject=None, pclass=None, proom=None,
                       phours=None):
    ui = gui.setup.SchoolSchedulerGUI()
    options_person = {}
    options_subject = {}
    options_class = {}
    options_room = {}

    school_id = school_selected_dict['id']
    schoolyear_id = schoolyear_selected_dict['id']

    persons = db.query.get_persons(school_id)
    subjects = db.query.get_subjects(school_id)
    classes = db.query.get_classes(schoolyear_id)
    rooms = db.query.get_rooms(school_id)

    for person in persons:
        options_person[person.id] = person.fullname
    for subject in subjects:
        options_subject[subject.id] = (subject.identifier, subject.default_hours)
    for class_ in classes:
        ident = f'{class_.year.identifier} {class_.section.identifier}'
        options_class[class_.id] = ident
    options_room[None] = ''
    for room in rooms:
        options_room[room.id] = room.identifier

    # sort by class identifiers
    options_class = dict(sorted(options_class.items(), key=itemgetter(1)))

    dialog = gui.dialog.CreateAssignmentDialog(ui.root, options_persons=options_person, options_subject=options_subject,
                                               options_class=options_class, options_room=options_room,
                                               pre_person1=pperson1, pre_person2=pperson2, pre_person3=pperson3,
                                               pre_subject=psubject, pre_class=pclass, pre_room=proom, pre_hours=phours)
    ret = dialog.result
    if ret:
        person1_id, person2_id, person3_id, subject_id, class_id, room_id, hours = ret
        if person1_id == '-':
            tkinter.messagebox.showwarning("Aggiunta assegnazione",
                                           "Almeno il primo docente va selezionato")
            return

        ass_persons = [db.query.get(db.model.Person, person1_id)]
        if person2_id is not None:
            ass_persons.append(db.query.get(db.model.Person, person2_id))
        if person3_id is not None:
            ass_persons.append(db.query.get(db.model.Person, person3_id))
        subject_in_class = db.model.SubjectInClass()
        subject_in_class.subject_id = subject_id
        subject_in_class.class_id = class_id
        subject_in_class.room_id = room_id
        subject_in_class.hours_total = hours
        subject = db.query.get(db.model.Subject, subject_id)
        subject_in_class.max_hours_per_day = subject.preferred_consecutive_hours
        subject_in_class.persons = ass_persons

        if db.query.get_subject_in_class(subject_in_class) is not None:
            tkinter.messagebox.showwarning("Aggiunta assegnazione",
                                           "Associazione classe-materia già presente. Inserimento ignorato")
        else:
            db.query.save(subject_in_class)
            # tkinter.messagebox.showinfo("Aggiunta Assegnazione", "Associazione aggiunta")

        populate_assignment_configuration()


def assignment_duplicate():
    ui = gui.setup.SchoolSchedulerGUI()

    assignment_ids = ui.widgets['assignment_listbox'].selection()
    if len(assignment_ids) == 0:
        tkinter.messagebox.showwarning("Eliminazione assegnazione", "Selezionare una assegnazione")
        return None

    assignment_id = assignment_ids[0]
    for assignment in assignment_list:
        if assignment[0] == int(assignment_id):
            persons_list = assignment[1].split(',')
            persons_list.extend([None, None, None])

            _assignment_create(persons_list[0], persons_list[1], persons_list[2],
                               assignment[2], assignment[3], assignment[5], assignment[4])

            break


def restriction_selected(event):
    pass


def restriction_edit(event=None):
    ui = gui.setup.SchoolSchedulerGUI()

    restriction_ids = ui.widgets['restriction_listbox'].selection()
    if len(restriction_ids) != 1:
        tkinter.messagebox.showwarning("Modifica restrizione", "Selezionare una restrizione")
        return None

    constraint = None
    shortname = ''
    for restriction_id in restriction_ids:
        for restriction in restriction_list:
            if restriction[0] == int(restriction_id):
                type_name = restriction[2]
                type_ = None
                for ckind in engine.struct.Constraint.REGISTERED_CONSTRAINTS:
                    if type_name == ckind['longname']:
                        type_ = ckind['classname']
                        shortname = ckind['shortname']
                        break
                assert type_ is not None, 'impossibile trovare il tipo della restrizione'
                constraint = db.query.get_constraint(type_, int(restriction_id))
                break

    assert constraint is not None, 'impossibile trovare la restrizione'

    dialog_obj = getattr(gui.constraint_dialog, shortname + 'Dialog')
    assert dialog_obj is not None, 'impossibile trovare la finestra di dialogo per la restrizione di tipo ' + shortname

    dialog = dialog_obj(ui.root, constraint)

    ret = dialog.result
    if ret is not None:
        db.query.save(ret.to_model())
        tkinter.messagebox.showinfo("Modifica restrizione", "Restrizione modificata correttamente")

        populate_restriction_configuration()


def restriction_delete():
    ui = gui.setup.SchoolSchedulerGUI()

    restriction_ids = ui.widgets['restriction_listbox'].selection()
    if len(restriction_ids) == 0:
        tkinter.messagebox.showwarning("Eliminazione restrizione", "Selezionare una restrizione")
        return None

    for restriction_id in restriction_ids:
        for restriction in restriction_list:
            if restriction[0] == int(restriction_id):
                confirm = tkinter.messagebox.askokcancel("Eliminazione restrizione",
                                                         f'Confermi di eliminare la restrizione {restriction[1]} di tipo \
                                                 {restriction[2]}?')

                if confirm:
                    db.query.delete(db.model.Constraint, restriction_id)
                    tkinter.messagebox.showinfo("Eliminazione restrizione", "Restrizione eliminata")

                break

    populate_restriction_configuration()


def restriction_create():
    ui = gui.setup.SchoolSchedulerGUI()

    options = dict()
    for ckind in engine.struct.Constraint.REGISTERED_CONSTRAINTS:
        try:
            dialog_obj = getattr(gui.constraint_dialog, ckind['shortname'] + 'Dialog')
            if dialog_obj is not None:
                options[ckind['longname']] = ckind['shortname']
        except AttributeError:
            pass

    dialog = gui.dialog.NewRestrictionDialog(parent=ui.root, options=options)

    ret = dialog.result
    if ret is not None:
        longname, shortname = ret
        dialog_obj = getattr(gui.constraint_dialog, shortname + 'Dialog')
        assert dialog_obj is not None, 'impossibile trovare la finestra di dialogo per la restrizione di tipo ' + shortname

        dialog = dialog_obj(ui.root, None)

        ret = dialog.result
        if ret is not None:
            db.query.save(ret.to_model())
            tkinter.messagebox.showinfo("Creazione restrizione", "Restrizione creata correttamente")
            populate_restriction_configuration()


def restriction_duplicate():
    ui = gui.setup.SchoolSchedulerGUI()

    restriction_ids = ui.widgets['restriction_listbox'].selection()
    if len(restriction_ids) != 1:
        tkinter.messagebox.showwarning("Duplica restrizione", "Selezionare una restrizione")
        return None

    constraint = None
    shortname = ''
    for restriction_id in restriction_ids:
        for restriction in restriction_list:
            if restriction[0] == int(restriction_id):
                type_name = restriction[2]
                type_ = None
                for ckind in engine.struct.Constraint.REGISTERED_CONSTRAINTS:
                    if type_name == ckind['longname']:
                        type_ = ckind['classname']
                        shortname = ckind['shortname']
                        break
                assert type_ is not None, 'impossibile trovare il tipo della restrizione'
                constraint = db.query.get_constraint(type_, int(restriction_id))
                break

    assert constraint is not None, 'impossibile trovare la restrizione'

    dialog_obj = getattr(gui.constraint_dialog, shortname + 'Dialog')
    assert dialog_obj is not None, 'impossibile trovare la finestra di dialogo per la restrizione di tipo ' + shortname

    constraint.id = None

    dialog = dialog_obj(ui.root, constraint)

    ret = dialog.result
    if ret is not None:
        db.query.save(ret.to_model())
        tkinter.messagebox.showinfo("Duplica restrizione", "Restrizione creata correttamente")

        populate_restriction_configuration()


def process_detail(event=None):
    ui = gui.setup.SchoolSchedulerGUI()

    process_ids = ui.widgets['process_listbox'].selection()
    if len(process_ids) != 1:
        tkinter.messagebox.showwarning("Dettagli elaborazione", "Selezionare una elaborazione")
        return None

    process = db.query.get(db.model.Process, int(process_ids[0]))

    dialog = gui.dialog.ShowProcessDialog(parent=ui.root, process=process)


def process_new():
    ui = gui.setup.SchoolSchedulerGUI()

    options = {"Simple Engine": simple_engine.SimpleEngine,
               "Randomized Engine": simple_engine_rand.SimpleEngineRand,
               "Local Optimal Engine": local_optimal.LocalOptimalEngine}

    dialog = gui.dialog.NewProcessDialog(parent=ui.root, options=options)

    process = dialog.result
    if process is not None:
        process.school_year_id = schoolyear_selected_dict['id']
        db.query.save(process)
        pc = process_coordinator.ProcessCoordinator()
        pc.start(process)
        populate_process_configuration()

def return_home():
    switch_frame(None, 'school_select_frame')


def switch_frame(from_name, to_name):
    ui = gui.setup.SchoolSchedulerGUI()
    if from_name in ui.frames:
        from_frame = ui.frames[from_name]
        from_frame.grid_remove()
    else:
        pass
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
        elif to_name == "assignment_configure_frame":
            gui.screen.configure_assignment_screen()
        elif to_name == "restriction_configure_frame":
            gui.screen.configure_restriction_screen()
        elif to_name == "process_configure_frame":
            gui.screen.process_screen()
    ui.root.geometry(gui.screen.geometries[to_name])




