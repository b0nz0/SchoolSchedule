import psycopg
from psycopg.rows import dict_row
from configparser import ConfigParser

from sqlalchemy import create_engine

active_connection = None
connection_parameters = None
active_engine = None

def config(filename='database.ini', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return db

def connect():
    global active_connection
    global connection_parameters
    global active_engine
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        if connection_parameters == None:
            # read connection parameters
            connection_parameters = config()

        active_engine = create_engine("postgresql+psycopg://" + connection_parameters['user'] + \
                                ":" + connection_parameters['password'] + \
                                "@" + connection_parameters['host'] + \
                                ":" + connection_parameters['port'] + \
                                "/" + connection_parameters['dbname'], echo=True)

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg.connect(**connection_parameters, row_factory=dict_row)
	
        active_connection = conn
        print ('Database connected')
        print (active_connection)
        return conn

    except (Exception, psycopg.DatabaseError) as error:
        print(error)

def print_connection_status():
    global active_connection
    try:
        # create a cursor
        cur = active_connection.cursor()
        
	    # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
	    # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg.DatabaseError) as error:
        print(error)

def unconnect():
    global active_connection
    if active_connection is not None:
        active_connection.close()
        print('Database connection closed.')

