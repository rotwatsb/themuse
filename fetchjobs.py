import sys
import requests
import psycopg2 as pg

pages = int(sys.argv[1].strip())

base_url = 'https://api-v2.themuse.com/jobs'

def make_url(base_url, params):
    if params:
        params_string = '&'.join(['='.join([str(k), str(v)])
                                 for k, v in params.items()])
        return ''.join([base_url, '?', params_string])
    else:
        return base_url

def save_result(conn, result):
    cur = conn.cursor()

    job_id = int(result['id'])
    full_name = result['name']
    publication_date = result['publication_date']
    listing_type = result['type']
    company = result['company']['name']
    contents = result['contents']

    try:
        cur.execute("INSERT INTO jobs (job_id, full_name, publication_date, "
                    "listing_type, company, contents) "
                    "VALUES (%s, %s, %s, %s, %s, %s);",
                    (job_id, full_name, publication_date, listing_type, company,
                     contents,))
    except pg.Error as e:
        conn.rollback()
    else:
        conn.commit()
                        
    locations = [location['name'] for location in result['locations']]
    for location in locations:
        try:
            # insert new location in locations table
            cur.execute("INSERT INTO locations (location) VALUES (%s) "
                        "RETURNING location_id;", (location,))
        except pg.Error as e:
            conn.rollback()
            try:
                cur.execute("SELECT location_id FROM locations WHERE location=%s;",
	                    (location,))
            except pg.Error as e:
                print(e.pgerror)
                conn.rollback()
                return
        else:
            conn.commit()
        
        location_id = cur.fetchone()[0]
        try:
            cur.execute("INSERT INTO jobs_locations (job_id, location_id) "
                        "VALUES (%s, %s);", (job_id, location_id))
        except pg.Error as e:
            conn.rollback()
        else:
            conn.commit()
    cur.close()

f = open('cnxinfo.txt', 'r')
cnxstring = f.readline()
conn = pg.connect(cnxstring)

for page in range(pages):
    params = {'page': page}
    url = make_url(base_url, params)
    response = requests.get(url)
    if response.status_code == 200:
        rjson = response.json()
        for result in rjson['results']:
            save_result(conn, result)
    else:
        break

conn.close()

