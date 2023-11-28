#!/bin/bash
# full
/usr/bin/pg_dump --file "sql/backup_svi.sql" --host "localhost" --port "5432" --username "postgres" --format=p --inserts --create --clean --if-exists --verbose "school_schedule"
#schema only
/usr/bin/pg_dump --file "sql/create_db.sql" --host "localhost" --port "5432" --username "postgres" --format=p --schema-only --create --clean --if-exists --verbose "school_schedule"
