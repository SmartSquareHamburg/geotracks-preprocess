INSERT INTO trx_persec_lines
SELECT 
	camname,
	timestamp,
	objid,
	objtype,
	CASE 
		WHEN objtype = 1 THEN 'person' 
		WHEN objtype = 2 THEN 'bicycle' 
		WHEN objtype = 3 THEN 'car' 
		WHEN objtype = 4 THEN 'motorcycle'
		WHEN objtype = 6 THEN 'bus'
		WHEN objtype = 8 THEN 'truck' 
		ELSE 'other' 
	END AS objtype_long,
	startFrame,
	ST_NUMPOINTS(ST_MAKELINE(centroid)) AS num,
	ST_MAKELINE(centroid) AS geom,
	videopart
FROM
	tracks_centroids
GROUP BY 
	camname,
	timestamp,
	videopart,
	objid,
	objtype,
	objtype_long,
	startFrame
ORDER BY
	camname,
	timestamp,
	objid