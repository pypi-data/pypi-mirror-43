UPDATE pg_database SET datistemplate='false' WHERE datname='template1';
DROP DATABASE template1;
CREATE DATABASE "template1" ENCODING 'utf8' LC_COLLATE 'C' TEMPLATE "template0";
UPDATE pg_database SET datistemplate='true' WHERE datname='template1';