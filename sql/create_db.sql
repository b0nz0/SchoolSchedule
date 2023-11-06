-- Database: school_schedule

DROP DATABASE IF EXISTS school_schedule;

CREATE DATABASE school_schedule
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'it_IT.UTF-8'
    LC_CTYPE = 'it_IT.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;