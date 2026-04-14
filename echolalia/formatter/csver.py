import csv
import io


class Formatter:

    def __init__(self) -> None:
        pass

    def add_args(self, parser):
        parser.add_argument("--with_header", action="store_true")
        return parser

    def marshall(self, args, data) -> str:
        output = io.StringIO()
        keys = data[0].keys()
        writer = csv.DictWriter(output, fieldnames=keys)
        if args.with_header:
            writer.writeheader()
        for doc in data:
            writer.writerow(doc)
        return output.getvalue()
