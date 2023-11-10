-- Start of SQL script

-- Drop tables if they already exist (to start fresh)
DROP TABLE IF EXISTS urls;
DROP TABLE IF EXISTS users;

-- Create the 'users' table
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    tier INTEGER NOT NULL
);

-- Create the 'urls' table
CREATE TABLE urls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    long_url TEXT NOT NULL,
    short_url TEXT UNIQUE NOT NULL,
    user_id TEXT NOT NULL,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

BEGIN TRANSACTION;

-- Insert dummy users with different tiers.
INSERT INTO users (user_id, tier) VALUES ('user1', 1);
INSERT INTO users (user_id, tier) VALUES ('user2', 2);

-- Insert dummy URLs for user1.
-- Assuming user1 is tier 1 and can have up to 1000 URLs.
INSERT INTO urls (long_url, short_url, user_id) VALUES 
('http://example.com/verylongurl1', 'short1', 'user1'),
('http://example.com/verylongurl2', 'short2', 'user1'),
('http://example.com/verylongurl1000', 'short1000', 'user1');

-- Insert dummy URLs for user2.
-- Assuming user2 is tier 2 and can have up to 500 URLs.
INSERT INTO urls (long_url, short_url, user_id) VALUES 
('http://example.com/differentlongurl1', 'diffshort1', 'user2'),
('http://example.com/differentlongurl2', 'diffshort2', 'user2'),
('http://example.com/differentlongurl500', 'diffshort500', 'user2');

COMMIT;

-- End of SQL script
