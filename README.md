setup:
1) create a postgres database that your user can write to (createdb databasename)
2) run "psql -d databasename -a -f schema.sql"
3) edit cnxinfo.txt to use your databasename

usage:
python3 fetchjobs.py num_pages

todo:
define sql functions for the queries
extend schema for the other many-to-many relationships (tags, categories, levels)
refactor locations code into a function that works for any many-to-many relationship
provide stats per page fetch: new jobs added, time taken to fetch page, etc)

Query to find number of jobs in 'New York City Metro Area':
select count(*) from jobs_locations WHERE location_id IN (select location_id from locations WHERE location='New York City Metro Area');


