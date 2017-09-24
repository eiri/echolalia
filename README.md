# Echolalia
Generate random data to test your application

## Installation

Clone repo with `git clone https://github.com/eiri/echolalia-prototype.git`, create and active virtual environment with `virtualenv venv` and  `source venv/bin/activate`, then install requirements with `pip install -r requirements.txt`.


## Usage

```bash
$ ./echolalia.py -c 2 -t templates/people.json -w stdout
[{"name": {"lastName": "Shannon", "firstName": "Rhonda"}, "tags": ["nihil", "fngheqnl", "impedit", "consequatur"], "age": 30, "state": "Hawaii, AR", "sex": "F", "phone": "03744269231", "single": true, "street": "4081 Sharon Ranch Apt. 197", "postcode": "ZIP: 02709-0053", "times": {"createdAt": "2017-02-13 13:14:08", "updatedAt": "2017-09-23 15:37:29"}, "email": "tiffany87@hotmail.com"}, {"name": {"lastName": "Hanson", "firstName": "Robert"}, "tags": ["quasi", "zbaqnl", "deserunt", "laborum"], "age": 104, "state": "Nevada, FL", "sex": "F", "phone": "(698)292-8761x6944", "single": false, "street": "3898 Alexandria Parkways", "postcode": "ZIP: 24439", "times": {"createdAt": "2017-05-03 03:16:21", "updatedAt": "2017-09-23 15:37:02"}, "email": "zfowler@hotmail.com"}]
```

## Teplates
_TBD_

## Formatters
_TBD_

## Writers
### StdOut
This is a basic plugin that just outputs generated data on standard output.

### CouchDB

This plugin creates new database with given name, than using passed in data to propogate it.

```bash
$ ./echolalia.py -c 2 -t templates/people.json -w couchdb --name tori -v
DEBUG     main:44 - Start
DEBUG     main:48 - Generating 2 docs with template templates/people.json
DEBUG     set_template:85 - Reading template templates/people.json
DEBUG     doc:121 - Generated doc {u'name': {u'lastName': 'Williams', u'firstName': 'Deanna'}, u'tags': ['facilis', 'sevqnl', 'sit', 'inventore'], u'age': 74, u'state': u'North Dakota, ND', u'sex': 'M', u'phone': '08582618909', u'single': True, u'street': '007 Sarah Walks', u'postcode': u'ZIP: 44204', u'times': {u'createdAt': '2016-12-28 23:54:19', u'updatedAt': '2017-09-23 15:39:20'}, u'email': 'timothylynch@hotmail.com'}
DEBUG     doc:121 - Generated doc {u'name': {u'lastName': 'Martinez', u'firstName': 'Jermaine'}, u'tags': ['laborum', 'jrqarfqnl', 'iure', 'tenetur'], u'age': 77, u'state': u'Alaska, SD', u'sex': 'M', u'phone': '06400668895', u'single': True, u'street': '24396 Joshua Vista Suite 529', u'postcode': u'ZIP: 15229-1795', u'times': {u'createdAt': '2017-06-13 08:42:26', u'updatedAt': '2017-09-23 15:39:42'}, u'email': 'aguilartracey@gmail.com'}
DEBUG     main:52 - Writing with writer "couchdb"
DEBUG     _new_conn:208 - Starting new HTTP connection (1): localhost
DEBUG     _make_request:396 - http://localhost:5984 "PUT /tori HTTP/1.1" 201 12
DEBUG      __create_db__:58 - Created database tori
DEBUG      __create_docs__:64 - Populating database tori
DEBUG     _new_conn:208 - Starting new HTTP connection (1): localhost
DEBUG     _make_request:396 - http://localhost:5984 "POST /tori/_bulk_docs HTTP/1.1" 201 192
DEBUG     __bulk_insert__:95 - Added 2 docs to database tori
DEBUG     main:55 - Done

$ curl http://localhost:5984/tori/_all_docs?include_docs=true -s | jq .rows[].doc.name
{
  "lastName": "Williams",
  "firstName": "Deanna"
}
{
  "lastName": "Martinez",
  "firstName": "Jermaine"
}
```

## Licence

[MIT](https://github.com/eiri/echolalia/blob/master/LICENSE)
