CREATE TABLE source (
    id SERIAL PRIMARY KEY,
    url VARCHAR NOT NULL,
    resource VARCHAR,
    table_name VARCHAR NOT NULL,
    extension VARCHAR NOT NULL
)