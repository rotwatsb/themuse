<h3>Setup:</h3>
<p>1) create a postgres database that your user can write to (createdb databasename)</p>
<p>2) run "psql -d databasename -a -f schema.sql"</p>
<p>3) edit cnxinfo.txt to use your databasename</p>
<br>
<h3>usage:</h3>
<p>python3 fetchjobs.py num_pages</p>
<br>
<h3>todo:</h3>
<p>1) define pgpsql functions for the queries</p>
<p>2) extend schema for the other many-to-many relationships (tags, categories, levels)</p>
<p>3) refactor locations code into a function that works for any many-to-many relationship</p>
<p>4) provide stats per page fetch: new jobs added, time taken to fetch page, etc)</p>
<br>
<p><strong>Query to find number of jobs in 'New York City Metro Area':</strong></p>
<p>select count(*) from jobs_locations WHERE location_id IN (select location_id from locations WHERE location='New York City Metro Area');</p>


