import traceback
import psycopg
import db.connection
from datetime import datetime
from model.entity import School

def get_base(obj, row):
    obj.object_id = row['object_id']
    obj.start_date = row['start_datetime']
    obj.end_date = row['end_datetime']
    obj.log_user = row['log_user']
    return obj

def write_base(obj, log_user: str):
    try:
        cur = db.connection.active_connection.cursor()       
        object_id = obj.object_id     
        if type(obj) == School:
            print(f"school id({object_id}) found")
            tablename = "public.school"
        if object_id == None or object_id == 0:
            print("new object found")
            qstring = "SELECT MAX(object_id)+1 AS new_id FROM " + tablename + ";"
            cur.execute(qstring)
            object_id = cur.fetchone()['new_id']
        else:
            print("old object found")
            qstring = "SELECT MAX(id) AS old_id FROM " + tablename + " \
                        WHERE object_id=" + str(object_id) + " AND end_datetime IS NULL;"
            cur.execute(qstring)
            old_id = cur.fetchone()['old_id']
            qstring = "UPDATE " + tablename + " \
	                    SET end_datetime=NOW(), log_user='" + log_user + "' WHERE id=" + str(old_id) + ";"
            cur.execute(qstring)
        qstring = "INSERT INTO " + tablename + " ( \
                    object_id, start_datetime, end_datetime, log_user EXTRA_COLUMNS) \
                    VALUES (" + str(object_id) + ", NOW(), NULL, '" + log_user + "' EXTRA_VALUES);"
        obj.object_id = object_id
        obj.start_date = datetime.now()
        obj.end_date = None
        obj.log_user = log_user

        return qstring
    except (Exception, psycopg.DatabaseError) as error:
        traceback.print_exc()


def get_schools():
    try:
        with db.connection.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM public.active_school")
            print("number of active schools: ", cur.rowcount)
            row = cur.fetchone()
            schools = []

            while row is not None:
                print(row)
                school = get_base(School(), row)
                school.name = row['name']
                schools.append(school)
                print(school)
                row = cur.fetchone()

            cur.close()
            return schools
    
    except (Exception, psycopg.DatabaseError) as error:
        traceback.print_exc()

def write_school(school:School, log_user: str):
    try:
        with db.connection.connect() as conn:
            cur = conn.cursor()
            qstring = write_base(school, log_user)
            qstring = qstring.replace("EXTRA_COLUMNS", ", name").replace("EXTRA_VALUES", ", '" + school.name + "'")
            cur.execute(qstring)
            print(cur.fetchone)
    except (Exception, psycopg.DatabaseError) as error:
        traceback.print_exc()
