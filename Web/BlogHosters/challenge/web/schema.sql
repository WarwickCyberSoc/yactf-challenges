DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id integer primary key,
    username text NOT NULL,
    password text NOT NULL,
    is_admin integer NOT NULL,
    magic_code text,
    blog_content text,
    blog_styling text,
    being_reviewed integer,
    unapproved_blog_content text,
    unapproved_blog_styling text,
    last_review_time text,
    last_approval_time text
);

/* Note that passwords differ on remote */
INSERT INTO users (username, password, is_admin) VALUES ('admin', 'hjBf@7K4KX?F&Rc4', 1), ('support_katie', '5#9ySDxkQHGFnRkT', 1);