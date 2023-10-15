CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    url TEXT NOT NULL,
    category TEXT NOT NULL,
    publisher_id INTEGER NOT NULL,
    sent BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (publisher_id) REFERENCES publishers (id)
);

CREATE TABLE IF NOT EXISTS publishers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rss_url TEXT NOT NULL,
    category TEXT
);