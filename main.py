from model.entity import School
import db.connection, db.query

if __name__ == '__main__':
    db.connection.connect()
    school = School()
    print (db.connection.active_connection)
    db.query.get_schools()
    db.connection.unconnect()
