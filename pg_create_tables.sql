-- You may create this tables first...

CREATE TABLE cam_pixelpoints (x numeric, y numeric, u smallint, v smallint, camname text, timestamp text, geom geometry(Point, 25832));
CREATE TABLE tracks_raw (frame smallint, objid smallint, u numeric, v numeric, width numeric, height numeric, confidence numeric, objtype numeric, unknown1 smallint, unknown2 smallint, unknown3 smallint, camname text, timestamp text, x numeric, y numeric, geom geometry(Point,25832), videopart smallint);
CREATE TABLE trx_persec_lines (camname text, timestamp text, objid smallint, objtype smallint, objtype_long text, startframe smallint, num integer, geom geometry, videopart smallint);
CREATE TABLE trx_persec_vlines (gid integer, camname varchar(16), timestamp varchar(18), objid double precision, objtype double precision, objtype_lo varchar(13), startframe double precision, num numeric, spatialclu numeric, dir boolean, videopart double precision, geom geometry(MultiLineString, 25832));