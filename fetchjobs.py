import sys
import requests
import psycopg2 as pg

pages = int(sys.argv[1].strip())

base_url = 'https://api-v2.themuse.com/jobs'

api_key = '7c46058625672f4656f6edb7bdeddf8de8d8c8c705f9fcba3c66964daa17eec4'

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
    except pg.IntegrityError:
        print("job_id {} already stored".format(job_id))
        conn.rollback()
    else:
        print("job_id {} added".format(job_id))
        conn.commit()
                        
    locations = [location['name'] for location in result['locations']]
    for location in locations:
        try:
            # insert new location in locations table
            cur.execute("INSERT INTO locations (location) VALUES (%s) RETURNING "
                        "location_id;", (location,))
        except pg.IntegrityError:
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
        except pg.IntegrityError:
            conn.rollback()
        else:
            conn.commit()
            
    cur.close()

def run(conn):
    for page in range(pages):
        params = {'page': page, 'api_key': api_key}
        url = make_url(base_url, params)
        response = requests.get(url)
        if response.status_code == 200:
            rjson = response.json()
            for result in rjson['results']:
                save_result(conn, result)
        else:
            break


f = open('cnxinfo.txt', 'r')
cnxstring = f.readline()
f.close()

try:
    conn = pg.connect(cnxstring)
except pg.Error as e:
    print(e.pgerror)
else:
    run(conn)
    conn.close()
