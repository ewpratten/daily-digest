-- Dumps the publisher list to a CSV (for easy backups)

.headers on
.mode csv
.output publishers.csv

SELECT * FROM publishers;

.quit
