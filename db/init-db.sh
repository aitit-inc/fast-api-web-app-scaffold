#!/bin/sh
set -e

DB_NAME="fawapp_db"
DB_USER="fawapp_dev"
DB_PASSWORD="fawapp_dev"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
	CREATE DATABASE $DB_NAME;
	CREATE USER $DB_USER WITH ENCRYPTED PASSWORD '$DB_PASSWORD';
	GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
EOSQL

# Grant all privileges on the public schema within the fawapp_db database
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$DB_NAME" <<-EOSQL
	GRANT ALL PRIVILEGES ON SCHEMA public TO $DB_USER;
EOSQL
