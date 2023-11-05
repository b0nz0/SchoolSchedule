from model.entity import School
import db.connection, db.query

if __name__ == '__main__':
    db.connection.connect()
    print (db.connection.active_connection)
    db.connection.print_connection_status()
    db.connection.unconnect()
    schools = db.query.get_schools()
    print(schools)

    s = School()
    s.name="Morgagni"
    db.query.write_school(s, "Fede")
    s.name = "New Morgagni"
    db.query.write_school(s, "Fede")


