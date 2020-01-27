# Purpose

The two attached python scripts are helper tools to execute a set of SQL queries on your data. First it starts with reading data from csv- or txt-files then it creates database tables from it and starts the sql queries.

- smsqhelpers-01-newReference.py

    Takes the result of the georeference script (large csv) and loads the data into a (existing) database table as reference data
    
- smsqhelpers-02-newData.py

    Takes the result of a tracking algorithm (large txt-file with pixelcoordinates), creates a database table from it, and filters and cross-references the two tables to add geodata to the source data. The result will be a points- and a linestring database table with generalized break point for every second of the track.

# Usage

Use the scripts to process large sets of un-referenced tracking data to further analyze them with GIS power.

## run:
    python smsqhelpers-01-newReference.py [tps-result] [camera-name] [timestamp]
    
    and
    
    python smsqhelpers-02-newData.py [raw.txt] [camera-name] [timestamp] [videopart]

## e. g.:
    python smsqhelpers-01-newReference.py tps_result.csv 'designOffices' '20180314-0800-1000'
    
    and
    
    python smsqhelpers-02-newData.py "tracks_01.txt" 'designOffices' '20180314-0800-1000' '1'

# Before we start:
The attached sql files are gonna be executed as one after another:

- smsqhelpers-01-newReference.sql_1.sql

    loads csv data to table

- smsqhelpers-01-newReference.sql_2.sql

    adds semantic data (parameters) to table
    
- smsqhelpers-02-newData.sql_6.sql

    loads txt data to table
    
- smsqhelpers-02-newData.sql_7.sql

    adds semantic data (parameters) to table
    
- smsqhelpers-02-newData.sql_8.sql

    cross-references tables to add geodata
    
- smsqhelpers-02-newData.sql_9.sql

    filters one breakpoint a second (centroid of fps)
    
- smsqhelpers-02-newData.sql_10.sql

    creates linestrings
    
- smsqhelpers-02-newData.sql_11.sql

    keeps only valid linestrings (equal or more than two points)

# Dependencies
psycopg2 (Python module)
PostgreSQL/ PostGIS-database

Tested with:
Python 3.6
PostgreSQL 10

# UPDATE
# Order of linestring break points
For some reason detected points are not arranged as linestrings in the right order. If this happens use the following sql query to rectify that.

    UPDATE 
        trx_persec_vlines AS trx 
    SET 
        geom = sub.geom 
    FROM (
        SELECT 
            objid, ST_MAKELINE(centroid) AS geom 
        FROM 
            tracks_centroids 
        GROUP BY 
            objid, objtype, startFrame 
        ORDER BY 
            objid
    ) AS sub 
    WHERE 
        trx.objid = sub.objid;
   
`TODO` Is this because of spatial indexing with GIST()? Due to "A GiST index is lossy, meaning that the index might produce false matches" ([Source](https://www.postgresql.org/docs/10/textsearch-indexes.html))

## Create table
For initial SQL CREATE'ing used tables run attached `pg_create_tables.sql` and check used coordinate system in that file. Also check if you already created the table `tracks_centroids`, if not change first line of `sql_9.sql` for inital try.

## Autovacuum
At the end it turned out that best practice is to run every dataset one by one and dump every single part to your drive instead of appending rows to a super-large table. So run these scripts and dump your result, then truncate data to go on with the next one. The default `autovacuum` method of PostgreSQL will run queries on your tables in the background preventing you of edit these tables. Unfortunately this will cost you a lot of time.
