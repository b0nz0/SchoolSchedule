from tkinter import *
from tkinter import ttk, simpledialog


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

        cancel_button = Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        self.result = self.selected_option.get()


class CreateRoomDialog(simpledialog.Dialog):
    def __init__(self, parent, options):
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

        cancel_button = Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        self.result = list(self.options.keys())[
            list(self.options.values()).index(self.selected_option.get())], self.entry_text.get()


class CreatePersonDialog(simpledialog.Dialog):
    def __init__(self, parent, options):
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

        cancel_button = Button(box, text="Cancel", width=10, command=self.cancel)
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
        self.options_hours = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6'}
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
        self.combo_subject['values'] = list(self.options_subject.values())
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

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, sticky=(N, W, E, S))

        cancel_button = Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        person1 = list(self.options_persons.keys())[list(self.options_persons.values()).index(self.selected_person1.get())]
        if self.selected_person2.get() != '':
            person2 = list(self.options_persons.keys())[list(self.options_persons.values()).index(self.selected_person2.get())]
        else: person2 = None
        if self.selected_person3.get() != '':
            person3 = list(self.options_persons.keys())[list(self.options_persons.values()).index(self.selected_person3.get())]
        else: person3 = None
        subject = list(self.options_subject.keys())[list(self.options_subject.values()).index(self.selected_subject.get())]
        class_ = list(self.options_class.keys())[list(self.options_class.values()).index(self.selected_class.get())]
        room = list(self.options_room.keys())[list(self.options_room.values()).index(self.selected_room.get())]
        hours = int(self.selected_hours.get())

        self.result = person1, person2, person3, subject, class_, room, hours
