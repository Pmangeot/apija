#!/bin/bash

set -e

# Check if the database volume exists
if [ -d "/var/lib/postgresql/data/pgdata" ]; then
    echo "Database volume exists. Skipping migration."
else
    echo "Database volume does not exist. Running migration."
    # Run the migration script
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" < /migration.sql
fi