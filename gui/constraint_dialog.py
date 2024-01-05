import engine.constraint
import logging
import db.query, db.model
import gui.event
from tkinter import *
import tkinter.messagebox
from tkinter import ttk, simpledialog

class BoostDialog(simpledialog.Dialog):
    def __init__(self, parent, constraint: engine.constraint.Boost or None):
        self.parent = parent
        if constraint is None:
            constraint = engine.constraint.Boost()
            
        self.constraint = constraint
        self.entry_nome_text = None
        self.entry_nome = None
        self.combo_type_text = None
        self.combo_type = None
        self.entry_score_text = None
        self.entry_score = None
        self.combo_perssubj_text = None
        self.combo_perssubj = None
        self.button_person_text = None
        self.button_person = None
        self.button_subject_text = None
        self.button_subject = None
        self.button_class_text = None
        self.button_class = None
        self.combo_day_text = None
        self.combo_day = None
        self.combo_hour_text = None
        self.combo_hour = None

        super().__init__(parent, title="Restrizione Aumenta/Diminuisci probabilità")

    def body(self, master):
        l = ttk.Label(master=master, text="nome")
        l.grid(column=0, row=1, padx=30, pady=5, sticky=(E))
        self.entry_nome_text = StringVar(master)
        if self.constraint.identifier is not None and len(self.constraint.identifier) > 0:
            self.entry_nome_text.set(self.constraint.identifier)
        self.entry_nome = ttk.Entry(master=master, textvariable=self.entry_nome_text, width=50)
        self.entry_nome.grid(column=1, row=1, pady=5, sticky=(N, W, E, S))

        l = ttk.Label(master=master, text="aumenta/diminuisci probabilità")
        l.grid(column=0, row=2, padx=30, pady=5, sticky=(E))
        self.combo_type_text = StringVar(master)
        self.combo_type = ttk.Combobox(master=master, textvariable=self.combo_type_text, width=15)
        self.combo_type.grid(column=1, row=2, pady=5, sticky=(N, S))
        self.combo_type['values'] = ['aumenta', 'diminuisci']
        if self.constraint.score > 0: self.combo_type.set('aumenta')
        elif self.constraint.score < 0: self.combo_type.set('diminuisci')
        else: 
            logging.error(f'constraint {self.constraint.identifier} ha score 0')
            tkinter.messagebox.showwarning("Restrizione Aumenta/Diminuisci probabilità", 
                                           f'La restrizione {self.constraint.identifier} ha score 0. Impossibile continuare')
            return None

        l = ttk.Label(master=master, text="punteggio (minimo 1, massimo 2000)")
        l.grid(column=0, row=3, padx=30, pady=5, sticky=(E))
        self.entry_score_text = StringVar(master)
        if self.constraint.score > 0: self.entry_score_text.set(str(self.constraint.score))
        else: self.entry_score_text.set(str(-self.constraint.score))
        self.entry_score = ttk.Entry(master=master, textvariable=self.entry_score_text, width=8)
        self.entry_score.grid(column=1, row=3, pady=5, sticky=(N, S))

        l = ttk.Label(master=master, text="docente/materia")
        l.grid(column=0, row=4, padx=30, pady=5, sticky=(E))
        self.combo_perssubj_text = StringVar(master)
        self.combo_perssubj= ttk.Combobox(master=master, textvariable=self.combo_perssubj_text, width=15)
        self.combo_perssubj.grid(column=1, row=4, pady=5, sticky=(N, S))
        self.combo_perssubj['values'] = ['docente', 'materia']
        if self.constraint.person_id is not None: self.combo_perssubj.set('docente')
        else: self.combo_perssubj.set('materia')
        self.combo_perssubj.bind('<<ComboboxSelected>>', self.combo_perssubj_selected)

        l = ttk.Label(master=master, text="docente")
        l.grid(column=0, row=5, padx=30, pady=5, sticky=(E))
        self.button_person_text = StringVar(master)
        self.button_person = ttk.Button(master=master, width=25)
        self.button_person.grid(column=1, row=5, pady=5, sticky=(N, S))
        if self.combo_perssubj.get() == 'docente':
            self.button_person_text = '-'
            if self.constraint.person_id is not None:
                self.button_person_text = db.query.get(db.model.Person, self.constraint.person_id).fullname
            self.button_person.configure(text=self.button_person_text)
            self.button_person.state(['!disabled'])
        else:
            self.button_person_text = '-'
            self.button_person.configure(text=self.button_person_text)
            self.button_person.state(['disabled'])

        l = ttk.Label(master=master, text="materia")
        l.grid(column=0, row=6, padx=30, pady=5, sticky=(E))
        self.button_subject_text = StringVar(master)
        self.button_subject = ttk.Button(master=master, width=25)
        self.button_subject.grid(column=1, row=6, pady=5, sticky=(N, S))
        if self.combo_perssubj.get() == 'materia':
            self.button_subject_text = '-'
            if self.constraint.subject_id is not None:
                self.button_subject_text = db.query.get(db.model.Subject, self.constraint.subject_id).identifier
            self.button_subject.configure(text=self.button_subject_text)
            self.button_subject.state(['!disabled'])
        else:
            self.button_subject_text = '-'
            self.button_subject.configure(text=self.button_subject_text)
            self.button_subject.state(['disabled'])

        l = ttk.Label(master=master, text="classe")
        l.grid(column=0, row=7, padx=30, pady=5, sticky=(E))
        self.button_class_text = StringVar(master)
        self.button_class = ttk.Button(master=master, width=25)
        self.button_class.grid(column=1, row=7, pady=5, sticky=(N, S))
        if self.constraint.class_id is not None:
            class_ = db.query.get(db.model.Class, self.constraint.class_id)
            class_text = f'{class_.year.identifier} {class_.section.identifier}'
            self.button_class_text = class_text
            self.button_class.configure(text=self.button_class_text)
        else:
            self.button_class.configure(text='OGNI CLASSE')
        self.button_class.state(['!disabled'])

        l = ttk.Label(master=master, text="giorno")
        l.grid(column=0, row=8, padx=30, pady=5, sticky=(E))
        self.combo_day_text = StringVar(master)
        self.combo_day = ttk.Combobox(master=master, textvariable=self.combo_day_text, width=15)
        self.combo_day.grid(column=1, row=8, pady=5, sticky=(N, S))
        daylist = ['OGNI GIORNO']
        for day in db.model.WeekDayEnum:
            daylist.append(day.value)
        self.combo_day['values'] = daylist
        if self.constraint.day is not None:
            self.combo_day.set(self.constraint.day.value)
        else:
            self.combo_day.set('OGNI GIORNO')
        
        l = ttk.Label(master=master, text="ora")
        l.grid(column=0, row=9, padx=30, pady=5, sticky=(E))
        self.combo_hour_text = StringVar(master)
        self.combo_hour = ttk.Combobox(master=master, textvariable=self.combo_hour_text, width=15)
        self.combo_hour.grid(column=1, row=9, pady=5, sticky=(N, S))
        self.combo_hour['values'] = ['OGNI ORA', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        if self.constraint.hour != 0 and self.constraint.hour is not None:
            self.combo_hour.set(str(self.constraint.hour))
        else:
            self.combo_hour.set('OGNI ORA')
        
        return self.entry_nome

    def combo_perssubj_selected(self, event):
        if self.combo_perssubj.get() == 'docente':
            self.button_person_text = '-'
            if self.constraint.person_id is not None:
                self.button_person_text = db.query.get(db.model.Person, self.constraint.person_id).fullname
            self.button_person.configure(text=self.button_person_text)
            self.button_person.state(['!disabled'])
        else:
            self.button_person_text = '-'
            self.button_person.configure(text=self.button_person_text)
            self.button_person.state(['disabled'])

        if self.combo_perssubj.get() == 'materia':
            self.button_subject_text = '-'
            if self.constraint.subject_id is not None:
                self.button_subject_text = db.query.get(db.model.Subject, self.constraint.subject_id).identifier
            self.button_subject.configure(text=self.button_subject_text)
            self.button_subject.state(['!disabled'])
        else:
            self.button_subject_text = '-'
            self.button_subject.configure(text=self.button_subject_text)
            self.button_subject.state(['disabled'])
        

    def buttonbox(self):
        box = ttk.Frame(self)
        ok_button = ttk.Button(box, text="OK", width=10, command=self.ok)
        ok_button.grid(column=0, row=2, pady=5, sticky=(N, W, E, S))

        cancel_button = Button(box, text="Cancel", width=10, command=self.cancel)
        cancel_button.grid(column=0, row=3, pady=5, sticky=(N, W, E, S))

        box.pack()

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

    def apply(self):
        self.result = self.constraint

