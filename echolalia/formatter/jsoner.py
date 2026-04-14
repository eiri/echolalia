import json


class Formatter:

    def __init__(self) -> None:
        pass

    def add_args(self, parser):
        return parser

    def marshall(self, args, data) -> str:
        return json.dumps(data)
