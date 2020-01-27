UPDATE cam_pixelpoints SET camname = STDIN1 WHERE camname IS NULL;
UPDATE cam_pixelpoints SET timestamp = STDIN2 WHERE timestamp IS NULL;
UPDATE cam_pixelpoints SET geom = ST_SETSRID(ST_MAKEPOINT(x, y), 25832) WHERE geom IS NULL;
CREATE INDEX cam_pixelpts_idx ON cam_pixelpoints USING GIST(geom);
