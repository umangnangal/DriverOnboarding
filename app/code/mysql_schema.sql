CREATE DATABASE IF NOT EXISTS todo_db;

CREATE TABLE IF NOT EXISTS driver (
    email_id VARCHAR (255) PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    pwd TEXT,
    mobile TEXT,
    onb_status TEXT,
    onb_comment TEXT,
    is_available BOOLEAN,
    plate_number TEXT,
    vehicle TEXT
);

CREATE TABLE IF NOT EXISTS approval (
    email_id VARCHAR (255) PRIMARY KEY,
    status TEXT,
    comment TEXT,
    action_by TEXT
);