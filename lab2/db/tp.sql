create schema public;

alter schema public owner to postgres;

grant create, usage on schema public to public;
