# echolalia
Generate random data for your CouchDB

## Installation

Clone repo with `git clone https://github.com/eiri/echolalia.git`, activate virtual environmnet with `source venv/bin/activate`, install requirements with `pip install -r requirements.txt`.

Now edit _config.ini_ and you all set to run

## Usage

Create new database with random name and 10 documents using template _people_. Those are all defaults.

```bash
$ ./echolalia.py
$ cat echolalia.log
2015-07-27 02:03:02 [INFO] - Created database praesentium
2015-07-27 02:03:02 [INFO] - Populating database with template people
2015-07-27 02:03:02 [INFO] - Added 10 docs to database praesentium
2015-07-27 02:03:02 [INFO] - Done

$ curl http://localhost:5984/praesentium/_all_docs?include_docs=true -s | jq .rows[].doc.name
"Dr. Houston Veum"
"Esau Sporer"
"Lorrayne Dooley DVM"
"Dr. Nelson Parker"
"Tari Lakin"
"Sydnee Bernhard"
"Sergio DuBuque"
"Ms. Marlena Lind"
"Shonda Ortiz"
"Hudson Kohler"
```


Create new database with name `access` and populate it with 53 documents using emplate _access_logs_

```bash
$ ./echolalia.py -t access_logs -c 53 -n access
$ tail -9 echolalia.log 
2015-07-27 02:08:26 [INFO] - Created database access
2015-07-27 02:08:26 [INFO] - Populating database with template access_logs
2015-07-27 02:08:26 [INFO] - Added 10 docs to database access
2015-07-27 02:08:26 [INFO] - Added 10 docs to database access
2015-07-27 02:08:26 [INFO] - Added 10 docs to database access
2015-07-27 02:08:26 [INFO] - Added 10 docs to database access
2015-07-27 02:08:26 [INFO] - Added 10 docs to database access
2015-07-27 02:08:26 [INFO] - Added 3 docs to database access
2015-07-27 02:08:26 [INFO] - Done

$ curl http://localhost:5984/access/_all_docs?include_docs=true -s | jq .rows[].doc.ip | head -5
"215.120.72.2"
"206.112.242.72"
"240.91.11.184"
"251.88.133.83"
"179.217.22.167"
``` 

Delete all databases

```bash
$ ./echolalia.py --clear
$ tail -6 echolalia.log
2015-07-27 02:13:16 [INFO] - Deleted database access
2015-07-27 02:13:16 [INFO] - Deleted database distinctio
2015-07-27 02:13:16 [INFO] - Deleted database molestiae
2015-07-27 02:13:16 [INFO] - Deleted database praesentium
2015-07-27 02:13:16 [INFO] - Deleted database twelvebeans
2015-07-27 02:13:16 [INFO] - Done

$ curl http://localhost:5984/_all_dbs -s | jq .
[
  "_replicator",
  "_users"
]
```

## Licence

[MIT](https://github.com/eiri/echolalia/blob/master/LICENSE)
