import sys


class Writer:

    def __init__(self) -> None:
        pass

    def add_args(self, parser):
        return parser

    def write(self, args, docs) -> None:
        print(docs, file=sys.stdout)
