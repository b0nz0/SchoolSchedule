import gui.setup

def school_selected(event):
    ui = gui.setup.SchoolSchedulerGUI()
    print(event)
    print(ui.widgets['schools_combo'].get())
    print(ui.variables['school_dict'][ui.widgets['schools_combo'].get()])
    