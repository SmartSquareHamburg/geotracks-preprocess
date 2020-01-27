DROP INDEX IF EXISTS cam_pixelpts_idx;
COPY cam_pixelpoints(x,y,u,v) FROM STDIN DELIMITER ',' CSV HEADER;
