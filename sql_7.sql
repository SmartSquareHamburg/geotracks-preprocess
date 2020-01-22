UPDATE tracks_raw SET camname = STDIN1 WHERE camname IS NULL;
UPDATE tracks_raw SET timestamp = STDIN2 WHERE timestamp IS NULL;
UPDATE tracks_raw SET videopart = STDIN3 WHERE videopart IS NULL;