#!/bin/bash
sudo su - postgres -c '/usr/bin//psql school_schedule < sql/backup_svi.sql'