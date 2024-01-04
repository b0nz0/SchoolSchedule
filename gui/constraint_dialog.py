import engine.constraint
import logging
import db.query, db.model
import gui.event
from tkinter import *
import tkinter.messagebox
from tkinter import ttk, simpledialog

class BoostDialog(simpledialog.Dialog):
    def __init__(self, parent, constraint:engine.constraint.Boost):
        self.parent = parent
        self.constraint = constraint
        self.entry_nome_text = None
        self.entry_nome = None
        self.combo_type_text = None
        self.combo_type = None
        self.entry_score_text = None
        self.entry_score = None
        self.combo_perssubj_text = None
        self.combo_perssubj = None
        self.combo_person_text = None
        self.combo_person = None
        self.combo_subject_text = None
        self.combo_subject = None
        gui.event.populate_person_configuration()
        gui.event.populate_subject_configuration()
        super().__init__(parent, title="Restrizione Aumenta/Diminuisci probabilità")

    def body(self, master):
        l = ttk.Label(master=master, text="nome")
        l.grid(column=0, row=1, padx=30, pady=5, sticky=(E))
        self.entry_nome_text = StringVar(master)
        if self.constraint.identifier is not None and len(self.constraint.identifier) > 0:
            self.entry_nome_text.set(self.constraint.identifier)
        self.entry_nome = ttk.Entry(master=master, textvariable=self.entry_nome_text)
        self.entry_nome.grid(column=1, row=1, sticky=(N, W, E, S))

        l = ttk.Label(master=master, text="aumenta/diminuisci probabilità")
        l.grid(column=0, row=2, padx=30, pady=5, sticky=(E))
        self.combo_type_text = StringVar(master)
        self.combo_type = ttk.Combobox(master=master, textvariable=self.combo_type_text)
        self.combo_type.grid(column=1, row=2, sticky=(N, S, E, W))
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
        if self.constraint.score > 0: self.entry_score_text = str(self.constraint.score)
        else: self.entry_score_text = str(-self.constraint.score)
        self.entry_score = ttk.Entry(master=master, textvariable=self.entry_score_text)
        self.entry_nome.grid(column=1, row=3, sticky=(N, W, E, S))

        l = ttk.Label(master=master, text="docente/materia")
        l.grid(column=0, row=4, padx=30, pady=5, sticky=(E))
        self.combo_perssubj_text = StringVar(master)
        self.combo_perssubj= ttk.Combobox(master=master, textvariable=self.combo_perssubj_text)
        self.combo_perssubj.grid(column=1, row=4, sticky=(N, S, E, W))
        self.combo_perssubj['values'] = ['docente', 'materia']
        if self.constraint.person_id is not None: self.combo_perssubj.set('docente')
        else: self.combo_perssubj.set('materia')

        l = ttk.Label(master=master, text="docente")
        l.grid(column=0, row=5, padx=30, pady=5, sticky=(E))
        self.combo_person_text = StringVar(master)
        self.combo_person = ttk.Entry(master=master, textvariable=self.combo_person_text)
        self.combo_person.grid(column=1, row=5, sticky=(N, W, E, S))
        if self.constraint.person_id is not None: 
            self.combo_person_text = db.query.get(db.model.Person, self.constraint.person_id).fullname
        else:
            self.combo_person_text = ''
            self.combo_person.config(state= "disabled")

        l = ttk.Label(master=master, text="materia")
        l.grid(column=0, row=6, padx=30, pady=5, sticky=(E))
        self.combo_subject_text = StringVar(master)
        self.combo_subject = ttk.Entry(master=master, textvariable=self.combo_subject_text)
        self.combo_subject.grid(column=1, row=6, sticky=(N, W, E, S))
        if self.constraint.subject_id is not None: 
            self.combo_subject_text = db.query.get(db.model.Subject, self.constraint.subject_id).identifier
        else:
            self.combo_subject_text = ''
            self.combo_subject.config(state= "disabled")


        return self.entry_nome

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

