#!/bin/bash
#sudo su - postgres -c '/usr/bin//psql < /home/b0nz0/workspace/SchoolSchedule/sql/create_db.sql'
#sudo su - postgres -c '/usr/bin/psql < /home/b0nz0/workspace/SchoolSchedule/sql/backup_svi.sql'
sudo su - postgres -c '/usr/bin/psql < backup_svi.sql'