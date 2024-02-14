import tkinter.messagebox
from datetime import datetime
from tkinter import *
from tkinter import ttk, simpledialog
import db, db.model
from gui.autocomplete import AutocompleteEntry


class AddClassInPlanDialog(simpledialog.Dialog):
    def __init__(self, parent, plans, classes: str):
        self.result = None
        self.selected_option = None
        self.options_combo = None
        self.parent = parent
        self.plans = plans
        self.classes = classes
        super().__init__(parent, title="Aggiungi classi al piano orario")

    def body(self, master):
        self.selected_option = StringVar(master)
        self.options_combo = ttk.Combobox(master, textvariable=self.selected_option)
        self.options_combo.grid(column=0, row=0, sticky=(N, W, E, S))
        self.options_combo['values'] = [a for a in self.plans.keys()]
        self.options_combo.current(0)

        l = ttk.Label(master=master, text=f"Abbina alle classi {self.classes}")
        l.grid(column=0, row=1, sticky=(N, W, E, S))
        return self.options_combo

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        self.result = self.selected_option.get()


class CreateRoomDialog(simpledialog.Dialog):
    def __init__(self, parent, options):
        self.entry = None
        self.result = None
        self.selected_option = None
        self.entry_text = ""
        self.options_combo = None
        self.parent = parent
        self.options = options
        super().__init__(parent, title="Crea uno spazio")

    def body(self, master):
        l = ttk.Label(master=master, text=f"Scegli tipo e nome dello spazio")
        l.grid(column=0, row=0, sticky=(N, W, E, S))

        self.selected_option = StringVar(master)
        self.options_combo = ttk.Combobox(master=master, textvariable=self.selected_option)
        self.options_combo.grid(column=0, row=1, sticky=(N, W, E, S))
        self.options_combo['values'] = list(self.options.values())
        self.options_combo.current(0)

        self.entry_text = StringVar(master)
        self.entry = ttk.Entry(master=master, textvariable=self.entry_text)
        self.entry.grid(column=0, row=2, sticky=(N, W, E, S))

        return self.options_combo

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        self.result = list(self.options.keys())[
            list(self.options.values()).index(self.selected_option.get())], self.entry_text.get()


class CreateSubjectDialog(simpledialog.Dialog):
    NO_PREFERENCE = '<NESSUNA PREFERENZA>'

    def __init__(self, parent, subject: db.model.Subject or None):
        self.con_hour_combo = None
        self.selected_con_hour = None
        self.def_hour_combo = None
        self.selected_def_hour = None
        self.entry = None
        self.result = None
        self.entry_text = ""
        self.parent = parent
        if subject is not None:
            self.subject = subject
        else:
            self.subject = db.model.Subject()
            self.subject.identifier = ''
            self.subject.default_hours = 1
            self.subject.preferred_consecutive_hours = 1
        super().__init__(parent, title="Materia")

    def body(self, master):
        l = ttk.Label(master=master,
                      text="Scegli nome, ore settimanali di default e \npreferenza su ore consecutive giornaliere per la materia")
        l.grid(column=0, row=0, pady=5)

        self.entry_text = StringVar(master)
        self.entry_text.set(self.subject.identifier)
        self.entry = ttk.Entry(master=master, textvariable=self.entry_text)
        self.entry.grid(column=0, row=2, pady=5, sticky=(N, W, E, S))

        self.selected_def_hour = StringVar(master)
        self.def_hour_combo = ttk.Combobox(master=master, textvariable=self.selected_def_hour)
        self.def_hour_combo.grid(column=0, pady=5, row=10, sticky=(N, S))
        self.def_hour_combo['values'] = [CreateSubjectDialog.NO_PREFERENCE, '1', '2', '3', '4', '5', '6', '7', '8']
        if self.subject.default_hours is not None:
            self.def_hour_combo.set(str(self.subject.default_hours))

        self.selected_con_hour = StringVar(master)
        self.con_hour_combo = ttk.Combobox(master=master, textvariable=self.selected_con_hour)
        self.con_hour_combo.grid(column=0, pady=5, row=20, sticky=(N, S))
        self.con_hour_combo['values'] = [CreateSubjectDialog.NO_PREFERENCE, '1', '2', '3']
        if self.subject.preferred_consecutive_hours is not None:
            self.con_hour_combo.set(str(self.subject.preferred_consecutive_hours))

        return self.entry

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        identifier = str(self.entry_text.get())
        if len(identifier) < 1:
            tkinter.messagebox.showwarning("Materia", "Dare un nome alla materia")
            self.result = None
            return
        else:
            self.subject.identifier = identifier
        def_hour = self.def_hour_combo.get()
        if def_hour == CreateSubjectDialog.NO_PREFERENCE or len(def_hour) < 1:
            self.subject.default_hours = None
        else:
            self.subject.default_hours = int(def_hour)
        con_hour = self.con_hour_combo.get()
        if con_hour == CreateSubjectDialog.NO_PREFERENCE or len(con_hour) < 1:
            self.subject.preferred_consecutive_hours = None
        else:
            self.subject.preferred_consecutive_hours = int(con_hour)
        self.result = self.subject


class CreatePersonDialog(simpledialog.Dialog):
    def __init__(self, parent, options):
        self.entry = None
        self.result = None
        self.selected_option = None
        self.entry_text = ""
        self.check_impersonal = None
        self.options_combo = None
        self.parent = parent
        self.options = options
        super().__init__(parent, title="Crea una persona")

    def body(self, master):
        l = ttk.Label(master=master, text="Scegli tipo, nome e flag impersonale della persona")
        l.grid(column=0, row=0, sticky=(N, W, E, S))

        self.selected_option = StringVar(master)
        self.options_combo = ttk.Combobox(master=master, textvariable=self.selected_option)
        self.options_combo.grid(column=0, row=1, sticky=(N, S))
        self.options_combo['values'] = list(self.options.values())
        self.options_combo.current(0)

        self.entry_text = StringVar(master)
        self.entry = ttk.Entry(master=master, textvariable=self.entry_text)
        self.entry.grid(column=0, row=2, sticky=(N, W, E, S))

        self.check_impersonal = ttk.Checkbutton(master=master, text='Impersonale')
        self.check_impersonal.state(['!alternate'])
        self.check_impersonal.state(['!disabled', '!selected'])
        self.check_impersonal.grid(column=0, row=3, sticky=(N, S))

        return self.options_combo

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        self.result = list(self.options.keys())[list(self.options.values()).index(self.selected_option.get())], \
            self.entry_text.get(), self.check_impersonal.instate(['selected'])


class CreateAssignmentDialog(simpledialog.Dialog):
    def __init__(self, parent, options_persons, options_subject, options_class, options_room,
                 pre_person1=None, pre_person2=None, pre_person3=None, pre_subject=None,
                 pre_class=None, pre_room=None, pre_hours=None):
        self.result = None
        self.selected_person1 = None
        self.selected_person2 = None
        self.selected_person3 = None
        self.selected_subject = None
        self.selected_class = None
        self.selected_room = None
        self.selected_hours = None
        self.combo_person1 = None
        self.combo_person2 = None
        self.combo_person3 = None
        self.combo_subject = None
        self.combo_class = None
        self.combo_room = None
        self.combo_hours = None
        self.options_persons = options_persons
        self.options_subject = options_subject
        self.options_class = options_class
        self.options_room = options_room
        self.options_hours = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10'}
        self.pre_person1 = pre_person1
        self.pre_person2 = pre_person2
        self.pre_person3 = pre_person3
        self.pre_subject = pre_subject
        self.pre_class = pre_class
        self.pre_room = pre_room
        self.pre_hours = pre_hours
        self.parent = parent
        super().__init__(parent, title="Aggiungi assegnazione")

    def body(self, master):
        self.geometry("500x400")
        master.columnconfigure(1, minsize=300)
        l = ttk.Label(master=master, text="Scegli docenti (minimo 1, massimo 3), materia, classe, \n \
            aula e numero di ore settimanali", anchor=CENTER, justify=CENTER)
        l.grid(column=0, row=0, pady=10, columnspan=3, sticky=(N, W, E, S))

        self.selected_person1 = StringVar(master)
        self.selected_person2 = StringVar(master)
        self.selected_person3 = StringVar(master)
        self.selected_subject = StringVar(master)
        self.selected_class = StringVar(master)
        self.selected_hours = StringVar(master)
        self.selected_room = StringVar(master)

        l = ttk.Label(master=master, text="Docente 1")
        l.grid(column=0, row=1, padx=30, pady=5, sticky=(E))
        self.combo_person1 = ttk.Combobox(master=master, textvariable=self.selected_person1)
        self.combo_person1.grid(column=1, row=1, sticky=(N, S, E, W))
        self.combo_person1['values'] = list(self.options_persons.values())
        if self.pre_person1 is not None:
            self.combo_person1.set(self.pre_person1)
        else:
            self.combo_person1.current(0)

        l = ttk.Label(master=master, text="Docente 2")
        l.grid(column=0, row=2, padx=30, pady=5, sticky=(E))
        self.combo_person2 = ttk.Combobox(master=master, textvariable=self.selected_person2)
        self.combo_person2.grid(column=1, row=2, sticky=(N, S, E, W))
        self.combo_person2['values'] = list(self.options_persons.values())
        if self.pre_person2 is not None:
            self.combo_person2.set(self.pre_person2)

        l = ttk.Label(master=master, text="Docente 3")
        l.grid(column=0, row=3, padx=30, pady=5, sticky=(E))
        self.combo_person3 = ttk.Combobox(master=master, textvariable=self.selected_person3)
        self.combo_person3.grid(column=1, row=3, sticky=(N, S, E, W))
        self.combo_person3['values'] = list(self.options_persons.values())
        if self.pre_person3 is not None:
            self.combo_person3.set(self.pre_person3)

        l = ttk.Label(master=master, text="Materia")
        l.grid(column=0, row=4, padx=30, pady=5, sticky=(E))
        self.combo_subject = ttk.Combobox(master=master, textvariable=self.selected_subject)
        self.combo_subject.grid(column=1, row=4, sticky=(N, S, E, W))
        self.combo_subject['values'] = [ident for ident, hours in self.options_subject.values()]
        self.combo_subject.bind('<<ComboboxSelected>>', self.set_preferred_hours)
        if self.pre_subject is not None:
            self.combo_subject.set(self.pre_subject)
        else:
            self.combo_subject.current(0)

        l = ttk.Label(master=master, text="Classe")
        l.grid(column=0, row=5, padx=30, pady=5, sticky=(E))
        self.combo_class = ttk.Combobox(master=master, textvariable=self.selected_class)
        self.combo_class.grid(column=1, row=5, sticky=(N, S))
        self.combo_class['values'] = list(self.options_class.values())
        if self.pre_class is not None:
            self.combo_class.set(self.pre_class)
        else:
            self.combo_class.current(0)

        l = ttk.Label(master=master, text="Aula")
        l.grid(column=0, row=6, padx=30, pady=5, sticky=(E))
        self.combo_room = ttk.Combobox(master=master, textvariable=self.selected_room)
        self.combo_room.grid(column=1, row=6, sticky=(N, S))
        self.combo_room['values'] = list(self.options_room.values())
        if self.pre_room is not None:
            self.combo_room.set(self.pre_room)
        else:
            self.combo_room.current(0)

        l = ttk.Label(master=master, text="Ore sett.")
        l.grid(column=0, row=7, padx=30, pady=5, sticky=(E))
        self.combo_hours = ttk.Combobox(master=master, textvariable=self.selected_hours)
        self.combo_hours.grid(column=1, row=7, sticky=(N, S))
        self.combo_hours['values'] = list(self.options_hours.values())
        if self.pre_hours is not None:
            self.combo_hours.set(self.pre_hours)
        else:
            self.combo_hours.current(0)

        return self.combo_hours

    def set_preferred_hours(self, event):
        for sid in self.options_subject:
            ident, hours = self.options_subject[sid]
            if ident == self.selected_subject.get():
                if hours is not None:
                    self.combo_hours.set(str(hours))
                else:
                    self.combo_hours.set('1')
                return

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        person1 = list(self.options_persons.keys())[
            list(self.options_persons.values()).index(self.selected_person1.get())]
        if self.selected_person2.get() != '':
            person2 = list(self.options_persons.keys())[
                list(self.options_persons.values()).index(self.selected_person2.get())]
        else:
            person2 = None
        if self.selected_person3.get() != '':
            person3 = list(self.options_persons.keys())[
                list(self.options_persons.values()).index(self.selected_person3.get())]
        else:
            person3 = None
        #        subject = list(self.options_subject.keys())[
        #            list(self.options_subject.values()).index(self.selected_subject.get())]
        for sid in self.options_subject:
            ident, hours = self.options_subject[sid]
            if ident == self.selected_subject.get():
                subject = sid
                break
        class_ = list(self.options_class.keys())[list(self.options_class.values()).index(self.selected_class.get())]
        if len(self.selected_room.get()) > 0:
            room = list(self.options_room.keys())[list(self.options_room.values()).index(self.selected_room.get())]
        else:
            room = None
        hours = int(self.selected_hours.get())

        self.result = person1, person2, person3, subject, class_, room, hours


class EditAssignmentDialog(simpledialog.Dialog):
    NO_ROOM = ''

    def __init__(self, parent, assignment: db.model.SubjectInClass or None,
                 options_persons, options_subject, options_class, options_room, lock=True):
        self.result = None
        if assignment is None:
            assignment = db.model.SubjectInClass()
        self.assignment = assignment

        self.selected_person1 = None
        self.selected_person2 = None
        self.selected_person3 = None
        self.selected_subject = None
        self.selected_class = None
        self.selected_room = None
        self.selected_hours = None
        self.combo_person1 = None
        self.combo_person2 = None
        self.combo_person3 = None
        self.combo_subject = None
        self.combo_class = None
        self.combo_room = None
        self.combo_hours = None
        self.options_persons = options_persons
        self.options_subject = options_subject
        self.options_class = options_class
        self.options_room = options_room
        self.options_hours = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '10'}
        self.parent = parent
        self.lock = lock
        super().__init__(parent, title="Modifica assegnazione")

    def body(self, master):
        self.geometry("500x400")
        master.columnconfigure(1, minsize=300)
        l = ttk.Label(master=master, text="Scegli docenti (minimo 1, massimo 3), materia, classe, \n \
            aula e numero di ore settimanali", anchor=CENTER, justify=CENTER)
        l.grid(column=0, row=0, pady=10, columnspan=3, sticky=(N, W, E, S))

        self.selected_person1 = StringVar(master)
        self.selected_person2 = StringVar(master)
        self.selected_person3 = StringVar(master)
        self.selected_subject = StringVar(master)
        self.selected_class = StringVar(master)
        self.selected_hours = StringVar(master)
        self.selected_room = StringVar(master)

        l = ttk.Label(master=master, text="Docente 1")
        l.grid(column=0, row=1, padx=30, pady=5, sticky=(E))
        self.combo_person1 = ttk.Combobox(master=master, textvariable=self.selected_person1)
        self.combo_person1.grid(column=1, row=1, sticky=(N, S, E, W))
        self.combo_person1['values'] = list(self.options_persons.values())
        if len(self.assignment.persons) > 0:
            self.combo_person1.set(self.assignment.persons[0].fullname)
        else:
            self.combo_person1.current(0)

        l = ttk.Label(master=master, text="Docente 2")
        l.grid(column=0, row=2, padx=30, pady=5, sticky=(E))
        self.combo_person2 = ttk.Combobox(master=master, textvariable=self.selected_person2)
        self.combo_person2.grid(column=1, row=2, sticky=(N, S, E, W))
        self.combo_person2['values'] = list(self.options_persons.values())
        if len(self.assignment.persons) > 1:
            self.combo_person2.set(self.assignment.persons[1].fullname)

        l = ttk.Label(master=master, text="Docente 3")
        l.grid(column=0, row=3, padx=30, pady=5, sticky=(E))
        self.combo_person3 = ttk.Combobox(master=master, textvariable=self.selected_person3)
        self.combo_person3.grid(column=1, row=3, sticky=(N, S, E, W))
        self.combo_person3['values'] = list(self.options_persons.values())
        if len(self.assignment.persons) > 2:
            self.combo_person2.set(self.assignment.persons[2].fullname)

        l = ttk.Label(master=master, text="Materia")
        l.grid(column=0, row=4, padx=30, pady=5, sticky=(E))
        self.combo_subject = ttk.Combobox(master=master, textvariable=self.selected_subject)
        self.combo_subject.grid(column=1, row=4, sticky=(N, S, E, W))
        self.combo_subject['values'] = [ident for ident, hours in self.options_subject.values()]
        self.combo_subject.bind('<<ComboboxSelected>>', self.set_preferred_hours)
        if self.assignment.subject is not None:
            self.combo_subject.set(self.assignment.subject.identifier)
        else:
            self.combo_subject.current(0)
        if self.lock:
            self.combo_subject.state(['disabled'])

        l = ttk.Label(master=master, text="Classe")
        l.grid(column=0, row=5, padx=30, pady=5, sticky=(E))
        self.combo_class = ttk.Combobox(master=master, textvariable=self.selected_class)
        self.combo_class.grid(column=1, row=5, sticky=(N, S))
        self.combo_class['values'] = list(self.options_class.values())
        if self.assignment.class_ is not None:
            self.combo_class.set(str(self.assignment.class_))
        else:
            self.combo_class.current(0)
        if self.lock:
            self.combo_class.state(['disabled'])

        l = ttk.Label(master=master, text="Aula")
        l.grid(column=0, row=6, padx=30, pady=5, sticky=(E))
        self.combo_room = ttk.Combobox(master=master, textvariable=self.selected_room)
        self.combo_room.grid(column=1, row=6, sticky=(N, S))
        room_list = [EditAssignmentDialog.NO_ROOM]
        room_list.extend(list(self.options_room.values()))
        self.combo_room['values'] = room_list
        if self.assignment.room is not None:
            self.combo_room.set(self.assignment.room.identifier)
        else:
            self.combo_room.current(0)

        l = ttk.Label(master=master, text="Ore sett.")
        l.grid(column=0, row=7, padx=30, pady=5, sticky=(E))
        self.combo_hours = ttk.Combobox(master=master, textvariable=self.selected_hours)
        self.combo_hours.grid(column=1, row=7, sticky=(N, S))
        self.combo_hours['values'] = list(self.options_hours.values())
        if self.assignment.hours_total is not None:
            self.combo_hours.set(str(self.assignment.hours_total))
        else:
            self.combo_hours.current(0)

        return self.combo_hours

    def set_preferred_hours(self, event):
        for sid in self.options_subject:
            ident, hours = self.options_subject[sid]
            if ident == self.selected_subject.get():
                if hours is not None:
                    self.combo_hours.set(str(hours))
                else:
                    self.combo_hours.set('1')
                return

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        for person in self.assignment.persons:
            if person.fullname != self.selected_person1.get() and \
                    person.fullname != self.selected_person2.get() and \
                    person.fullname != self.selected_person3.get():
                self.assignment.persons.remove(person)
        person_id = list(self.options_persons.keys())[
            list(self.options_persons.values()).index(self.selected_person1.get())]
        if person_id not in [p.id for p in self.assignment.persons]:
            self.assignment.persons.append(db.query.get(db.model.Person, person_id))
        if self.selected_person2.get() != '':
            person_id = list(self.options_persons.keys())[
                list(self.options_persons.values()).index(self.selected_person2.get())]
            if person_id not in [p.id for p in self.assignment.persons]:
                self.assignment.persons.append(db.query.get(db.model.Person, person_id))
        if self.selected_person3.get() != '':
            person_id = list(self.options_persons.keys())[
                list(self.options_persons.values()).index(self.selected_person3.get())]
            if person_id not in [p.id for p in self.assignment.persons]:
                self.assignment.persons.append(db.query.get(db.model.Person, person_id))

        #        subject = list(self.options_subject.keys())[
        #            list(self.options_subject.values()).index(self.selected_subject.get())]
        for sid in self.options_subject:
            ident, hours = self.options_subject[sid]
            if ident == self.selected_subject.get():
                subject_id = sid
                break
        if self.assignment.subject is None or subject_id != self.assignment.subject.id:
            self.assignment.subject = db.query.get(db.model.Subject, subject_id)
        class_id = list(self.options_class.keys())[list(self.options_class.values()).index(self.selected_class.get())]
        if self.assignment.class_ is None or class_id != self.assignment.class_.id:
            self.assignment.class_ = db.query.get(db.model.Class, class_id)
        if self.selected_room.get() != EditAssignmentDialog.NO_ROOM:
            room_id = list(self.options_room.keys())[list(self.options_room.values()).index(self.selected_room.get())]
            if self.assignment.room is None or room_id != self.assignment.room.id:
                self.assignment.room = db.query.get(db.model.Room, room_id)
        else:
            self.assignment.room = None

        self.assignment.hours_total = int(self.selected_hours.get())

        self.result = self.assignment


class SelectPersonDialog(simpledialog.Dialog):
    def __init__(self, parent, options):
        self.autocomplete_frame = None
        self.result = None
        self.parent = parent
        self.options = options
        self.selected_option = None
        self.options_combo = None

        super().__init__(parent, title="Seleziona docente")

    def body(self, master):
        l = ttk.Label(master=master, text="Scegli il tipo e cerca per nome")
        l.grid(column=0, row=0, columnspan=2, pady=5)

        l = ttk.Label(master=master, text="tipo")
        l.grid(column=0, row=1, padx=30, pady=5, sticky=(E))
        self.selected_option = StringVar(master)
        self.options_combo = ttk.Combobox(master=master, textvariable=self.selected_option)
        self.options_combo.grid(column=1, row=1, pady=5, sticky=(N, S))
        self.options_combo['values'] = list(self.options.keys())
        self.options_combo.current(0)
        self.options_combo.bind('<<ComboboxSelected>>', self._build_autocomplete_frame)

        l = ttk.Label(master=master, text="nome")
        l.grid(column=0, row=2, padx=30, pady=5, sticky=(E))
        self.autocomplete_frame = AutocompleteEntry(master=master)
        self.autocomplete_frame.grid(column=1, row=2, pady=5, sticky=(N, W, E, S))
        self._build_autocomplete_frame()

    def _build_autocomplete_frame(self, event=None):
        type_value = self.options_combo.get()
        self.autocomplete_frame.build(entries=self.options[type_value])

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        self.result = self.autocomplete_frame.value, self.autocomplete_frame.id


class SelectSubjectDialog(simpledialog.Dialog):
    def __init__(self, parent, options):
        self.autocomplete_frame = None
        self.result = None
        self.parent = parent
        self.options = options
        self.selected_option = None
        self.options_combo = None

        super().__init__(parent, title="Seleziona materia")

    def body(self, master):
        l = ttk.Label(master=master, text="Cerca per nome")
        l.grid(column=0, row=0, columnspan=2, pady=5)

        l = ttk.Label(master=master, text="nome")
        l.grid(column=0, row=2, padx=30, pady=5, sticky=(E))
        self.autocomplete_frame = AutocompleteEntry(master=master)
        self.autocomplete_frame.grid(column=1, row=2, pady=5, sticky=(N, W, E, S))
        self.autocomplete_frame.build(entries=self.options)

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        self.result = self.autocomplete_frame.value, self.autocomplete_frame.id


class SelectClassDialog(simpledialog.Dialog):
    def __init__(self, parent, options):
        self.autocomplete_frame = None
        self.result = None
        self.parent = parent
        self.options = options
        self.every_class = None
        self.selected_option = None
        self.options_combo = None

        super().__init__(parent, title="Seleziona classe")

    def body(self, master):
        l = ttk.Label(master=master, text="Cerca per nome o seleziona OGNI CLASSE")
        l.grid(column=0, row=0, columnspan=2, pady=5)

        l = ttk.Label(master=master, text="nome")
        l.grid(column=0, row=2, padx=30, pady=5, sticky=(E))
        self.autocomplete_frame = AutocompleteEntry(master=master)
        self.autocomplete_frame.grid(column=1, row=2, pady=5, sticky=(N, W, E, S))
        self.autocomplete_frame.build(entries=self.options, case_sensitive=True)

        self.every_class = ttk.Checkbutton(master=master, text='OGNI CLASSE')
        self.every_class.state(['!alternate'])
        self.every_class.state(['!disabled', '!selected'])
        self.every_class.grid(column=0, row=3, columnspan=2, sticky=(N, S))

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        if self.every_class.instate(['selected']):
            self.result = 'OGNI CLASSE', None
        else:
            self.result = self.autocomplete_frame.value, self.autocomplete_frame.id


class NewRestrictionDialog(simpledialog.Dialog):
    def __init__(self, parent, options):
        self.result = None
        self.parent = parent
        self.options = options
        self.selected_option = None
        self.options_combo = None

        super().__init__(parent, title="Seleziona tipo restrizione")

    def body(self, master):
        l = ttk.Label(master=master, text="Scegli il tipo della nuova restrizione")
        l.grid(column=0, row=0, pady=5, sticky=(N, W, E, S))

        self.selected_option = StringVar(master)
        self.options_combo = ttk.Combobox(master=master, textvariable=self.selected_option)
        self.options_combo.grid(column=0, row=1, pady=5, sticky=(N, S))
        self.options_combo['values'] = list(self.options.keys())
        self.options_combo.current(0)

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        self.result = self.selected_option.get(), self.options[self.selected_option.get()]


class NewProcessDialog(simpledialog.Dialog):
    CYCLES_MAX = 10000

    def __init__(self, parent, options):
        self.entry = None
        self.entry_text = None
        self.result = None
        self.parent = parent
        self.options = options
        self.selected_option = None
        self.options_combo = None
        self.process = None

        super().__init__(parent, title="Avvia una nuova elaborazione")

    def body(self, master):
        self.geometry("400x200")
        master.columnconfigure(1, minsize=300)
        l = ttk.Label(master=master,
                      text=f'Scegli il tipo di motore e il numero di cicli di esecuzione (max {NewProcessDialog.CYCLES_MAX})',
                      anchor=CENTER, justify=CENTER)
        l.grid(column=0, row=0, pady=10, sticky=(N, W, E, S))

        self.selected_option = StringVar(master)
        self.options_combo = ttk.Combobox(master=master, textvariable=self.selected_option)
        self.options_combo.grid(column=0, row=1, pady=5, sticky=(N, S))
        self.options_combo['values'] = list(self.options.keys())
        self.options_combo.current(2)

        self.entry_text = StringVar(master)
        self.entry_text.set("1")
        self.entry = ttk.Entry(master=master, textvariable=self.entry_text)
        self.entry.grid(column=0, row=2, sticky=(N, S))

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def ok(self, event=None):
        if len(self.entry.get()) < 1:
            tkinter.messagebox.showwarning("Nuova elaborazione", "Indicare il numero di cicli")
            return

        if not self.entry.get().isdigit() or \
                int(self.entry.get()) < 1 or \
                int(self.entry.get()) > NewProcessDialog.CYCLES_MAX:
            tkinter.messagebox.showwarning("Nuova elaborazione",
                                           f'Il numero di cicli deve essere un numero compreso tra 1 e {NewProcessDialog.CYCLES_MAX}')
            return

        self.process = db.model.Process()
        self.process.kind = self.selected_option.get()
        self.process.cycles = int(self.entry.get())
        self.process.status = "NUOVO"
        self.process.date_start = None
        self.process.date_end = None
        self.process.files = []

        super().ok(event=event)

    def apply(self):
        self.result = self.process


class ShowProcessDialog(simpledialog.Dialog):
    def __init__(self, parent, process):
        self.result = None
        self.parent = parent
        self.process = process

        super().__init__(parent, title="Dettagli elaborazione")

    def body(self, master):
        master.columnconfigure(1, minsize=300)
        l = ttk.Label(master=master, text="Tipo elaborazione")
        l.grid(column=0, row=1, padx=30, pady=5, sticky=(E))
        l = ttk.Label(master=master, text=self.process.kind)
        l.grid(column=1, row=1, padx=30, pady=5, sticky=(W))
        l = ttk.Label(master=master, text="Numero di cicli")
        l.grid(column=0, row=2, padx=30, pady=5, sticky=(E))
        l = ttk.Label(master=master, text=str(self.process.cycles))
        l.grid(column=1, row=2, padx=30, pady=5, sticky=(W))
        l = ttk.Label(master=master, text="Stato")
        l.grid(column=0, row=3, padx=30, pady=5, sticky=(E))
        l = ttk.Label(master=master, text=self.process.status)
        l.grid(column=1, row=3, padx=30, pady=5, sticky=(W))

        date_start = '-' if self.process.date_start is None else \
            self.process.date_start.strftime('%Y-%m-%d_%H-%M-%S')
        date_end = '-' if self.process.date_end is None else \
            self.process.date_end.strftime('%Y-%m-%d_%H-%M-%S')
        l = ttk.Label(master=master, text="Avviato")
        l.grid(column=0, row=10, padx=30, pady=5, sticky=(E))
        l = ttk.Label(master=master, text=date_start)
        l.grid(column=1, row=10, padx=30, pady=5, sticky=(W))
        l = ttk.Label(master=master, text="Completato")
        l.grid(column=0, row=11, padx=30, pady=5, sticky=(E))
        l = ttk.Label(master=master, text=date_end)
        l.grid(column=1, row=11, padx=30, pady=5, sticky=(W))

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
