CREATE TABLE IF NOT EXISTS users (
    id integer primary key autoincrement,
    username text,
    password text
);

CREATE TABLE IF NOT EXISTS documents (
    id text primary key,
    file_name text,
    orig_name text,
    owner integer,
    metadata text,
    uploaded_at integer
);

CREATE TABLE IF NOT EXISTS shared_documents (
    id integer primary key autoincrement,
    document_id text,
    shared_with integer,
    shared_at integer,
    viewed boolean
);

INSERT INTO users (username, password) VALUES ('admin', 'WOW_THIS_PASSWORD!!!'); 

INSERT INTO documents (id, file_name, orig_name, owner, metadata, uploaded_at) VALUES ('81d4900ebaec9cef58453fa639ca6a73', '81d4900ebaec9cef58453fa639ca6a73_Passwords.csv', 'Passwords.csv', 1, '', 1644330535);