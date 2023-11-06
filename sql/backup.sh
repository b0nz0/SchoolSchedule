#|/bin/bash
/usr/bin/pg_dump --file "sql/backup_svi.sql" --host "localhost" --port "5432" --username "postgres" --format=p --inserts --create --clean --if-exists --verbose "school_schedule"