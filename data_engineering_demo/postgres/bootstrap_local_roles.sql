-- Local PostgreSQL bootstrap (run once as a superuser), e.g.:
--   psql -U postgres -h 127.0.0.1 -f postgres/bootstrap_local_roles.sql
--
-- Matches docker-compose.yml warehouse credentials (dedemo / dedemo_wh).

DO
$$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'dedemo') THEN
        CREATE ROLE dedemo LOGIN PASSWORD 'dedemo';
    END IF;
END
$$;

CREATE DATABASE dedemo_wh OWNER dedemo;
-- If this errors with "already exists", you are done.
