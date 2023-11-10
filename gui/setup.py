from tkinter import *
from tkinter import ttk

class SchoolSchedulerGUI(object):
    _root = None
    _frames = {}
    _widgets = {}
    _variables = {}

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SchoolSchedulerGUI, cls).__new__(cls)
        return cls.instance
  
    def startup(self):
        self._root = Tk()

    def show(self):
        self._root.mainloop()

    @property
    def root(self):
        return self._root
    
    @property
    def frames(self):
        return self._frames
    
    @property
    def widgets(self):
        return self._widgets
    
    @property
    def variables(self):
        return self._variables
    
