# Echolalia

![project: prototype](https://img.shields.io/badge/project-prototype-orange.svg "Project: Prototype")
![test](https://github.com/eiri/echolalia/workflows/test/badge.svg)

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

## Licence

[MIT](https://github.com/eiri/echolalia/blob/master/LICENSE)
