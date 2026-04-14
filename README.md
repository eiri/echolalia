# Echolalia

![project: prototype](https://img.shields.io/badge/project-prototype-orange.svg "Project: Prototype")
[![Build Status](https://github.com/eiri/echolalia/workflows/CI/badge.svg)](https://github.com/eiri/echolalia/actions)

Generate random data to test your application.

## Requirements

- Python 3.12 or 3.13
- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
git clone https://github.com/eiri/echolalia.git
cd echolalia
uv sync
```

`uv sync` creates the virtual environment and installs all dependencies.

## Usage

```bash
$ uv run echolalia -c 2 -t templates/people.json
[{"name": {"lastName": "Shannon", "firstName": "Rhonda"}, "tags": ["nihil", "fngheqnl", "impedit", "consequatur"], "age": 30, "state": "Hawaii, AR", "sex": "F", "phone": "03744269231", "single": true, "street": "4081 Sharon Ranch Apt. 197", "postcode": "ZIP: 02709-0053", "times": {"createdAt": "2017-02-13 13:14:08", "updatedAt": "2017-09-23 15:37:29"}, "email": "tiffany87@hotmail.com"}, {"name": {"lastName": "Hanson", "firstName": "Robert"}, "tags": ["quasi", "##tuesday###", "deserunt", "laborum"], "age": 104, "state": "Nevada, FL", "sex": "F", "phone": "(698)292-8761x6944", "single": false, "street": "3898 Alexandria Parkways", "postcode": "ZIP: 24439", "times": {"createdAt": "2017-05-03 03:16:21", "updatedAt": "2017-09-23 15:37:02"}, "email": "zfowler@hotmail.com"}]
```

```bash
$ uv run echolalia -c 2 -i name -i email=free_email -f csv
Bruce Day,lori09@yahoo.com
Janice Turner,matthew72@sanders.com
```

To skip the `uv run` prefix, activate the virtualenv first:

```bash
source .venv/bin/activate
echolalia -c 2 -i name -i email=free_email -f csv
```

## Development

```bash
uv sync --dev
uv run pytest
```

## Templates

Templates are JSON objects. Keys become keys in the generated document; values are [faker](https://github.com/joke2k/faker) method names.

To pass arguments to a method, use an object with `"attr"` and `"args"`:

```json
{ "birthday": { "attr": "date_of_birth", "args": [null, 18, 65] } }
```

A key's value can also be a list of methods, which produces an array. For composite strings, use mustache syntax: `"{state}, {state_abbr}"`. To transform the result after generation, add a `"postprocess"` key with a `str` method name.

See `templates/people.json` for a full example.

## Formatters

**raw** — returns the data as a Python object, no serialization.

**json** — JSON output.

**csv** — CSV output. Pass `--with_header` to add a header row. Nested objects are flattened to strings.

**yaml** — YAML output, always in block style.

## Writers

**stdout** — prints to standard output (default).

**file** — writes to a file; requires `-o`/`--output`.

## Licence

[MIT](https://github.com/eiri/echolalia/blob/master/LICENSE)
