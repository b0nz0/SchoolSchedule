from tkinter import *
from tkinter import ttk

root = None

#s = ttk.Style()
#s.configure('Main.TFrame', background='black', borderwidth=5, relief='raised')

def startup():
    global root
    root = Tk()

def show():
    global root
    root.mainloop()

    

