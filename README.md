<h3>Setup:</h3>
<p>1) create a postgres database that your user can write to (createdb databasename)</p>
<p>2) run "psql -d databasename -a -f schema.sql"</p>
<p>3) edit cnxinfo.txt to use your databasename</p>
<h3>usage:</h3>
<p>python3 fetchjobs.py num_pages</p>
<h3>todo:</h3>
<p>1) define pgpsql functions for the queries</p>
<p>2) extend schema for the other many-to-many relationships (tags, categories, levels)</p>
<p>3) refactor locations code into a function that works for similar many-to-many relationships</p>
<p>4) provide stats per page fetch: new jobs added, time taken to fetch page, etc)</p>
<p><strong>Query to find number of sept 2016 job postings for 'New York City Metro Area':</strong></p>

SELECT COUNT(*) FROM jobs JOIN jobs_locations ON jobs.job_id = jobs_locations.job_id JOIN locations ON jobs_locations.location_id=locations.location_id WHERE publication_date >= '2016-09-01 00:00:00' AND publication_date < '2016-10-01 00:00:00' AND location='New York City Metro Area';


