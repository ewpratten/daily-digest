-- Dumps the publisher list to a CSV (for easy backups)
-- run with: sqlite3 daily_digest.sqlite3 < sql/dump_publishers.sql

.headers on
.mode csv
.output publishers.csv

SELECT * FROM publishers;

.quit
