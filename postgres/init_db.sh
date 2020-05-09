#!/usr/bin/env bash
set -e

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER grader WITH PASSWORD 'grader';
    CREATE DATABASE grader;
    GRANT ALL PRIVILEGES ON DATABASE grader TO grader;

    CREATE USER content WITH PASSWORD 'content';
    CREATE DATABASE content;
    GRANT ALL PRIVILEGES ON DATABASE content TO content;
EOSQL