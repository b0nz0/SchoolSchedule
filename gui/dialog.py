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
        self.result = list(self.options.keys())[list(self.options.values()).index(self.selected_option.get())], self.entry_text.get()


