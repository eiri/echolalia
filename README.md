# Echolalia

![project: prototype](https://img.shields.io/badge/project-prototype-orange.svg "Project: Prototype")

Generate random data to test your application

## Installation

Clone repo with `git clone https://github.com/eiri/echolalia-prototype.git`, create and active virtual environment with `virtualenv venv` and  `source venv/bin/activate`, then install requirements with `pip install -r requirements.txt`.


## Usage

```bash
$ ./echolalia.py -c 2 -t templates/people.json -w stdout
[{"name": {"lastName": "Shannon", "firstName": "Rhonda"}, "tags": ["nihil", "fngheqnl", "impedit", "consequatur"], "age": 30, "state": "Hawaii, AR", "sex": "F", "phone": "03744269231", "single": true, "street": "4081 Sharon Ranch Apt. 197", "postcode": "ZIP: 02709-0053", "times": {"createdAt": "2017-02-13 13:14:08", "updatedAt": "2017-09-23 15:37:29"}, "email": "tiffany87@hotmail.com"}, {"name": {"lastName": "Hanson", "firstName": "Robert"}, "tags": ["quasi", "zbaqnl", "deserunt", "laborum"], "age": 104, "state": "Nevada, FL", "sex": "F", "phone": "(698)292-8761x6944", "single": false, "street": "3898 Alexandria Parkways", "postcode": "ZIP: 24439", "times": {"createdAt": "2017-05-03 03:16:21", "updatedAt": "2017-09-23 15:37:02"}, "email": "zfowler@hotmail.com"}]
```

```bash
$ ./echolalia.py -c 2 -i name -i email=free_email -f csv
Bruce Day,lori09@yahoo.com
Janice Turner,matthew72@sanders.com

```

## Templates

JSON document of expected structure where keys will be used as keys for generated document and values should be methods of [faker](https://github.com/joke2k/faker) library. If method suppose to get arguments, the value block should be defined as json object with "attr" for name of method and "args" for list of provided arguments.

While template must be an object, the keys can take list of methods to generate arrays. For complex values mustash style of template can be used (e.g. `"{state}, {state_abbr}"`). Additional element "postprocess" can be used to run specified command over generated value.

Take a look at `templates/people.json` file for example.

## Formatters
### Raw
Pass through, returns generated data as python object.

### JSON
Marshalls data to JSON.

### CSV
Marshalls data to CSV format. If command line argument `--with_headers` provided adds as a first line a list of keys. Generated object more than 1 level of depth smashed into string

### YAML
Marshalls data in YAML. Collections always serialized in block style.

### XML
Marshalls data in XML. If command line argument `--root <ROOT>` provided, each document will be wraped in specified root element. Default root element `<document>`.

## Writers
### StdOut
This is a basic plugin that just outputs generated data on the standard output.

### File
Output to a specified with `-o` or `--output` file.

### CouchDB

This plugin creates new database with given name, than using passed in data to propogate it.

```bash
$ ./echolalia.py -c 2 -t templates/people.json -f raw -w couchdb --name tori -v
DEBUG     main:49 - Start
DEBUG     main:53 - Generating 2 docs with template templates/people.json
DEBUG     set_template:85 - Reading template templates/people.json
DEBUG     doc:121 - Generated doc {u'name': {u'lastName': 'Sanchez', u'firstName': 'Mary'}, u'tags': ['quas', 'ghrfqnl', 'iusto', 'molestiae'], u'age': 105, u'state': u'New Mexico, CT', u'sex': 'F', u'phone': '916-771-1436x8689', u'single': True, u'street': '5635 Holly Wells Suite 442', u'postcode': u'ZIP: 34574', u'times': {u'createdAt': '2017-07-17 21:37:27', u'updatedAt': '2017-09-25 08:49:10'}, u'email': 'dmorgan@gmail.com'}
DEBUG     doc:121 - Generated doc {u'name': {u'lastName': 'Miller', u'firstName': 'Jennifer'}, u'tags': ['sit', 'fngheqnl', 'suscipit', 'illum'], u'age': 16, u'state': u'Maine, PW', u'sex': 'F', u'phone': '1-099-592-1502', u'single': False, u'street': '643 Heather Trail', u'postcode': u'ZIP: 06884', u'times': {u'createdAt': '2017-09-23 10:01:20', u'updatedAt': '2017-09-25 08:50:00'}, u'email': 'gbraun@yahoo.com'}
DEBUG     main:57 - Marshalling with formatter "raw"
DEBUG     main:60 - Writing with writer "couchdb"
DEBUG     _new_conn:208 - Starting new HTTP connection (1): localhost
DEBUG     _make_request:396 - http://localhost:5984 "PUT /tori HTTP/1.1" 201 12
DEBUG     _create_db:48 - Created database tori
DEBUG     _create_docs:54 - Populating database tori
DEBUG     _new_conn:208 - Starting new HTTP connection (1): localhost
DEBUG     _make_request:396 - http://localhost:5984 "POST /tori/_bulk_docs HTTP/1.1" 201 192
DEBUG     _bulk_insert:67 - Added 2 docs to database tori
DEBUG     main:63 - Done

$ curl http://localhost:5984/tori/_all_docs?include_docs=true -s | jq .rows[].doc.name
{
  "lastName": "Sanchez",
  "firstName": "Mary"
}
{
  "lastName": "Miller",
  "firstName": "Jennifer"
}
```

## Licence

[MIT](https://github.com/eiri/echolalia/blob/master/LICENSE)
