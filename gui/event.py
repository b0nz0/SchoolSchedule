import gui.screen

def school_selected(event):
    print(event)
    print(gui.screen.schools_combo.get())
    print(gui.screen.school_dict[gui.screen.schools_combo.get()])
