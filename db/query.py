import psycopg
import db.connection

def get_schools():
    try:
        cur = db.connection.active_connection.cursor()
        cur.execute("SELECT * FROM public.active_school")
        print("number of active schools: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg.DatabaseError) as error:
        print(error)
