UPDATE tracks_raw
SET x = points.x, y = points.y 
FROM cam_pixelpoints AS points
WHERE 
	points.u = CASE 
	 	WHEN CAST(ROUND(tracks_raw.u) AS smallint) + ROUND(0.5*width) > 0
		THEN CAST(ROUND(tracks_raw.u) AS smallint) + ROUND(0.5*width)
		ELSE 1 END AND 
	points.v = CASE
		WHEN 1080 - (CAST(ROUND(tracks_raw.v) AS smallint) + ROUND(height)) <= 1080
		THEN 1080 - (CAST(ROUND(tracks_raw.v) AS smallint) + ROUND(height))
		ELSE 1080 END AND 
	points.camname = tracks_raw.camname AND
	points.timestamp = tracks_raw.timestamp AND
	tracks_raw.camname = STDIN1 AND
	tracks_raw.timestamp = STDIN2 AND
	tracks_raw.videopart = STDIN3;

UPDATE tracks_raw SET geom = ST_SETSRID(ST_MAKEPOINT(x, y), 25832) WHERE geom IS NULL AND camname = STDIN1 AND timestamp = STDIN2 AND videopart = STDIN3;