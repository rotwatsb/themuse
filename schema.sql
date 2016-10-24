BEGIN;

CREATE TABLE jobs (
	job_id int NOT NULL PRIMARY KEY,
	full_name varchar(256) NOT NULL,
	publication_date timestamp with time zone NOT NULL,
	listing_type varchar(32) NOT NULL,
	company varchar(128) NOT NULL,
	contents text NOT NULL);

CREATE TABLE locations (
	location_id serial NOT NULL PRIMARY KEY,
	location varchar(256) NOT NULL UNIQUE);

CREATE TABLE jobs_locations (
	job_id int REFERENCES jobs (job_id) ON DELETE RESTRICT,
	location_id int REFERENCES locations (location_id) ON DELETE RESTRICT,
	CONSTRAINT job_location_id PRIMARY KEY (job_id, location_id));

    COMMIT;
