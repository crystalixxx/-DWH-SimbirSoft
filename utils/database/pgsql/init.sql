CREATE TABLE source (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL,
    resource VARCHAR,
    table_name VARCHAR NOT NULL,
    extension VARCHAR NOT NULL
)