from db.model import *
import db.connection, db.query
import gui.setup, gui.screen
from tkinter import *
import pickle

def populate_DB():
    s = School()
    s.name="Morgagni"
    db.query.save(s)
    print("school:" + s.name)
    print(s)

    y = SchoolYear()
    y.identifier = "2023/24"
    y.school = s
    db.query.save(y)

    r1 = Year()
    r1.identifier = "I"
    r1.school = s
    db.query.save(r1)

    r2 = Year()
    r2.identifier = "II"
    r2.school = s
    db.query.save(r2)

    r3 = Year()
    r3.identifier = "III"
    r3.school = s
    db.query.save(r3)

    r4 = Year()
    r4.identifier = "IV"
    r4.school = s
    db.query.save(r4)

    r5 = Year()
    r5.identifier = "V"
    r5.school = s
    db.query.save(r5)


    ca = Section()
    ca.identifier = "A"
    ca.school = s
    db.query.save(ca)

    cb = Section()
    cb.identifier = "B"
    cb.school = s
    db.query.save(cb)

    cc = Section()
    cc.identifier = "C"
    cc.school = s
    db.query.save(cc)

    l = Class()
    l.school_year = y
    l.section = ca
    l.year = r1
    db.query.save(l)
    print(l)
    l2 = Class()
    l2.school_year = y
    l2.section = cb
    l2.year = r1
    db.query.save(l2)
    print(l2)
    l3 = Class()
    l3.school_year = y
    l3.section = ca
    l3.year = r2
    db.query.save(l3)
    print(l3)
    
    room1 = Room()
    room1.identifier = "101"
    room1.room_type = RoomEnum.AULA
    room1.school = s
    db.query.save(room1)
    
    room2 = Room()
    room2.identifier = "102"
    room2.room_type = RoomEnum.AULA
    room2.school = s
    db.query.save(room2)
    
    room3 = Room()
    room3.identifier = "Palestra Grande"
    room3.room_type = RoomEnum.PALESTRA
    room3.school = s
    db.query.save(room3)
    
    room4 = Room()
    room4.identifier = "Laboratorio di Informatica"
    room4.room_type = RoomEnum.LABORATORIO
    room4.school = s
    db.query.save(room4)

    profs = {}
    
    for i in range(1, 15):
        pers = Person()
        pers.fullname = "Prof. " + str(i)
        pers.person_type = PersonEnum.DOCENTE
        pers.is_impersonal = False
        pers.school = s
        db.query.save(pers)
        profs[i] = pers
    
    lettore = Person()
    lettore.fullname = "Lettore Inglese"
    lettore.person_type = PersonEnum.LETTORE
    lettore.is_impersonal = False
    lettore.school = s
    db.query.save(lettore)
    
    subj_italiano = Subject()
    subj_italiano.identifier = "Italiano"
    subj_italiano.school = s
    db.query.save(subj_italiano)
    subj_matematica = Subject()
    subj_matematica.identifier = "Matematica"
    subj_matematica.school = s
    db.query.save(subj_matematica)
    subj_inglese = Subject()
    subj_inglese.identifier = "Inglese"
    subj_inglese.school = s
    db.query.save(subj_inglese)
    subj_fisica = Subject()
    subj_fisica.identifier = "Fisica"
    subj_fisica.school = s
    db.query.save(subj_fisica)
    subj_latino = Subject()
    subj_latino.identifier = "Latino"
    subj_latino.school = s
    db.query.save(subj_latino)
    subj_edfisica = Subject()
    subj_edfisica.identifier = "Ed. Fisica"
    subj_edfisica.school = s
    db.query.save(subj_edfisica)
    subj_religione = Subject()
    subj_religione.identifier = "Religione"
    subj_religione.school = s
    db.query.save(subj_religione)
    subj_storia = Subject()
    subj_storia.identifier = "Storia"
    subj_storia.school = s
    db.query.save(subj_storia)
    subj_filosofia = Subject()
    subj_filosofia.identifier = "Filosofia"
    subj_filosofia.school = s
    db.query.save(subj_filosofia)
    subj_arte = Subject()
    subj_arte.identifier = "St. dell'Arte"
    subj_arte.school = s
    db.query.save(subj_arte)
    
    sic = SubjectInClass()
    sic.class_ = l
    sic.subject = subj_matematica
    sic.hours_total = 5
    sic.max_hours_per_day = 2
    sic.persons = [profs[1]]
    sic.room = room1
    db.query.save(sic)
    sic = SubjectInClass()
    sic.class_ = l
    sic.subject = subj_italiano
    sic.hours_total = 5
    sic.max_hours_per_day = 2
    sic.persons = [profs[2]]
    sic.room = room1
    db.query.save(sic)
    sic = SubjectInClass()
    sic.class_ = l
    sic.subject = subj_inglese
    sic.hours_total = 4
    sic.max_hours_per_day = 2
    sic.persons = [profs[3], lettore]
    sic.room = room1
    db.query.save(sic)
    sic = SubjectInClass()
    sic.class_ = l
    sic.subject = subj_arte
    sic.hours_total = 2
    sic.max_hours_per_day = 1
    sic.persons = [profs[4]]
    sic.room = room1
    db.query.save(sic)
    sic = SubjectInClass()
    sic.class_ = l
    sic.subject = subj_edfisica
    sic.hours_total = 2
    sic.max_hours_per_day = 1
    sic.persons = [profs[5]]
    sic.room = room3
    db.query.save(sic)
    sic = SubjectInClass()
    sic.class_ = l
    sic.subject = subj_fisica
    sic.hours_total = 3
    sic.max_hours_per_day = 2
    sic.persons = [profs[1]]
    sic.room = room1
    db.query.save(sic)
    sic = SubjectInClass()
    sic.class_ = l
    sic.subject = subj_latino
    sic.hours_total = 3
    sic.max_hours_per_day = 1
    sic.persons = [profs[6]]
    sic.room = room1
    db.query.save(sic)
    sic = SubjectInClass()
    sic.class_ = l
    sic.subject = subj_religione
    sic.hours_total = 1
    sic.max_hours_per_day = 1
    sic.persons = [profs[7]]
    sic.room = room1
    db.query.save(sic)

    h1 = Hour()
    h1.start = time(8, 0)
    h1.minutes = 60
    h1.school = s
    db.query.save(h1)
    h2 = Hour()
    h2.start = time(9, 0)
    h2.minutes = 60
    h2.school = s
    db.query.save(h2)
    h3 = Hour()
    h3.start = time(10, 0)
    h3.minutes = 60
    h3.school = s
    db.query.save(h3)
    h4 = Hour()
    h4.start = time(11, 0)
    h4.minutes = 60
    h4.school = s
    db.query.save(h4)
    h5 = Hour()
    h5.start = time(12, 0)
    h5.minutes = 60
    h5.school = s
    db.query.save(h5)
    
    plan = Plan()
    plan.identifier = "Calendario 1"
    plan.school = s
    db.query.save(plan)
    
    d = DailyHour()
    d.week_day = WeekDayEnum.MONDAY
    d.plan = plan
    d.hour = h1
    d.ordinal = 1
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.MONDAY
    d.plan = plan
    d.hour = h2
    d.ordinal = 2
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.MONDAY
    d.plan = plan
    d.hour = h3
    d.ordinal = 3
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.MONDAY
    d.plan = plan
    d.hour = h4
    d.ordinal = 4
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.MONDAY
    d.plan = plan
    d.hour = h5
    d.ordinal = 5
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.TUESDAY
    d.plan = plan
    d.hour = h1
    d.ordinal = 1
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.TUESDAY
    d.plan = plan
    d.hour = h2
    d.ordinal = 2
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.TUESDAY
    d.plan = plan
    d.hour = h3
    d.ordinal = 3
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.TUESDAY
    d.plan = plan
    d.hour = h4
    d.ordinal = 4
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.TUESDAY
    d.plan = plan
    d.hour = h5
    d.ordinal = 5
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.WEDNESDAY
    d.plan = plan
    d.hour = h1
    d.ordinal = 1
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.WEDNESDAY
    d.plan = plan
    d.hour = h2
    d.ordinal = 2
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.WEDNESDAY
    d.plan = plan
    d.hour = h3
    d.ordinal = 3
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.WEDNESDAY
    d.plan = plan
    d.hour = h4
    d.ordinal = 4
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.WEDNESDAY
    d.plan = plan
    d.hour = h5
    d.ordinal = 5
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.THURSDAY
    d.plan = plan
    d.hour = h1
    d.ordinal = 1
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.THURSDAY
    d.plan = plan
    d.hour = h2
    d.ordinal = 2
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.THURSDAY
    d.plan = plan
    d.hour = h3
    d.ordinal = 3
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.THURSDAY
    d.plan = plan
    d.hour = h4
    d.ordinal = 4
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.THURSDAY
    d.plan = plan
    d.hour = h5
    d.ordinal = 5
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.FRIDAY
    d.plan = plan
    d.hour = h1
    d.ordinal = 1
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.FRIDAY
    d.plan = plan
    d.hour = h2
    d.ordinal = 2
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.FRIDAY
    d.plan = plan
    d.hour = h3
    d.ordinal = 3
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.FRIDAY
    d.plan = plan
    d.hour = h4
    d.ordinal = 4
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.FRIDAY
    d.plan = plan
    d.hour = h5
    d.ordinal = 5
    db.query.save(d)    

    cp = ClassPlan()
    cp.plan = plan
    cp.class_ = l
    db.query.save(cp)
    cp = ClassPlan()
    cp.plan = plan
    cp.class_ = l2
    db.query.save(cp)
    cp = ClassPlan()
    cp.plan = plan
    cp.class_ = l3
    db.query.save(cp)


if __name__ == '__main__':
    db.connection.connect()
#    print (db.connection.active_connection)
#    db.connection.print_connection_status()
#    db.connection.unconnect()
#    schools = db.query.get_schools()
#    for s in schools:
#        print(s.name)
#    populate_DB()
    s = db.query.get(School, 1)
    print(s)
    with open("test_ser_school.ser", "wb") as outfile:
        pickle.dump(s, outfile)
    ui = gui.setup.SchoolSchedulerGUI()
    ui.startup()
    gui.screen.school_select_screen()
    root = ui.root
    root.title("Scuola")
    root.resizable(width=TRUE, height=TRUE)
    ui.show()
