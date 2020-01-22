INSERT INTO tracks_centroids -- CREATE TABLE tracks_centroids AS
SELECT 
	camname, 
	timestamp,
	videopart,
	objid,
	CAST(ROUND(objtype) AS smallint) AS objtype,
	min AS startFrame,
	key,
	cluster, 
	ST_CENTROID(ST_COLLECT(geom)) AS centroid
FROM
	(
		SELECT 
			*,
			ROUND((frame-min)/25) AS cluster
		FROM 
			tracks_raw 
		LEFT JOIN 
			(
				SELECT 
					camname || '_' || timestamp || '_' || videopart || '_' || objid AS key, 
					MIN(frame) AS min 
				FROM 
					tracks_raw 
				GROUP BY 
					camname, 
					timestamp,
					videopart,
					objid
			) AS createMinValueAndJoinKey 
		ON 
			camname || '_' || timestamp || '_' || videopart || '_' || objid = key
		WHERE
			camname = STDIN1 AND
			timestamp = STDIN2 AND
			videopart = STDIN3
		ORDER BY 
			camname, 
			timestamp, 
			objid, 
			frame
	) AS createClusterValue
GROUP BY
	camname,
	timestamp,
	videopart, 
	objid, 
	objtype,
	startFrame,
	key,
	cluster
