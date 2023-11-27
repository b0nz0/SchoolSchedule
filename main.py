from db.model import *
import db.connection, db.query
import gui.setup, gui.screen
from tkinter import *
import pickle

def populate_DB():
    s = School()
    s.name="Morgagni"
    db.query.save(s, "Fede")
    print("school:" + s.name)
    print(s)

    y = SchoolYear()
    y.identifier = "2023/24"
    y.school = s
    db.query.save(y, "Fede")

    r1 = Year()
    r1.identifier = "I"
    r1.school = s
    db.query.save(r1, "Fede")

    r2 = Year()
    r2.identifier = "II"
    r2.school = s
    db.query.save(r2, "Fede")

    r3 = Year()
    r3.identifier = "III"
    r3.school = s
    db.query.save(r3, "Fede")

    r4 = Year()
    r4.identifier = "IV"
    r4.school = s
    db.query.save(r4, "Fede")

    r5 = Year()
    r5.identifier = "V"
    r5.school = s
    db.query.save(r5, "Fede")


    ca = Section()
    ca.identifier = "A"
    ca.school = s
    db.query.save(ca, "Fede")

    cb = Section()
    cb.identifier = "B"
    cb.school = s
    db.query.save(cb, "Fede")

    cc = Section()
    cc.identifier = "C"
    cc.school = s
    db.query.save(cc, "Fede")

    l = Class()
    l.school_year = y
    l.section = ca
    l.year = r1
    db.query.save(l, "Fede")
    print(l)
    l2 = Class()
    l2.school_year = y
    l2.section = cb
    l2.year = r1
    db.query.save(l2, "Fede")
    print(l2)
    l3 = Class()
    l3.school_year = y
    l3.section = ca
    l3.year = r2
    db.query.save(l3, "Fede")
    print(l3)
    
    room1 = Room()
    room1.identifier = "101"
    room1.room_type = RoomEnum.AULA
    room1.school = s
    db.query.save(room1, "Fede")
    
    room2 = Room()
    room2.identifier = "102"
    room2.room_type = RoomEnum.AULA
    room2.school = s
    db.query.save(room2, "Fede")
    
    room3 = Room()
    room3.identifier = "Palestra Grande"
    room3.room_type = RoomEnum.PALESTRA
    room3.school = s
    db.query.save(room3, "Fede")
    
    room4 = Room()
    room4.identifier = "Laboratorio di Informatica"
    room4.room_type = RoomEnum.LABORATORIO
    room4.school = s
    db.query.save(room4, "Fede")
    
    pers1 = Person()
    pers1.fullname = "Federico"
    pers1.person_type = PersonEnum.DOCENTE
    pers1.is_impersonal = False
    pers1.school = s
    db.query.save(pers1)
    
    pers2 = Person()
    pers2.fullname = "Eleonora"
    pers2.person_type = PersonEnum.DOCENTE
    pers2.is_impersonal = False
    pers2.school = s
    db.query.save(pers2)
    
    subj1 = Subject()
    subj1.identifier = "Italiano"
    subj1.school = s
    db.query.save(subj1)
    subj2 = Subject()
    subj2.identifier = "Matematica"
    subj2.school = s
    db.query.save(subj2)
    
    sic1 = SubjectInClass()
    sic1.class_ = l
    sic1.subject = subj1
    sic1.hours_total = 6
    sic1.max_hours_per_day = 2
    sic1.persons = [pers1, pers2]
    sic1.room = room1
    db.query.save(sic1)
    sic2 = SubjectInClass()
    sic2.class_ = l
    sic2.subject = subj2
    sic2.hours_total = 4
    sic2.max_hours_per_day = 2
    sic2 = db.query.save(sic2)

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
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.MONDAY
    d.plan = plan
    d.hour = h2
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.MONDAY
    d.plan = plan
    d.hour = h3
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.MONDAY
    d.plan = plan
    d.hour = h4
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.MONDAY
    d.plan = plan
    d.hour = h5
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.TUESDAY
    d.plan = plan
    d.hour = h1
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.TUESDAY
    d.plan = plan
    d.hour = h2
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.TUESDAY
    d.plan = plan
    d.hour = h3
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.TUESDAY
    d.plan = plan
    d.hour = h4
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.TUESDAY
    d.plan = plan
    d.hour = h5
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.WEDNESDAY
    d.plan = plan
    d.hour = h1
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.WEDNESDAY
    d.plan = plan
    d.hour = h2
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.WEDNESDAY
    d.plan = plan
    d.hour = h3
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.WEDNESDAY
    d.plan = plan
    d.hour = h4
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.WEDNESDAY
    d.plan = plan
    d.hour = h5
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.THURSDAY
    d.plan = plan
    d.hour = h1
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.THURSDAY
    d.plan = plan
    d.hour = h2
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.THURSDAY
    d.plan = plan
    d.hour = h3
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.THURSDAY
    d.plan = plan
    d.hour = h4
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.THURSDAY
    d.plan = plan
    d.hour = h5
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.FRIDAY
    d.plan = plan
    d.hour = h1
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.FRIDAY
    d.plan = plan
    d.hour = h2
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.FRIDAY
    d.plan = plan
    d.hour = h3
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.FRIDAY
    d.plan = plan
    d.hour = h4
    db.query.save(d)    
    d = DailyHour()
    d.week_day = WeekDayEnum.FRIDAY
    d.plan = plan
    d.hour = h5
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
