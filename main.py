from model.entity import School
from db.connection import active_connection, connect

if __name__ == '__main__':
    connect()
    school = School()

