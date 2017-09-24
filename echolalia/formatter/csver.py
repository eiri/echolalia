import io, csv

class Formatter:

  def __init__(self):
    return None

  def add_args(self, parser):
    parser.add_argument('--with_header', action='store_true')
    return parser

  def marshall(self, args, data):
    output = io.BytesIO()
    keys = data[0].keys()
    writer = csv.DictWriter(output, fieldnames=keys)
    if args.with_header:
        writer.writeheader()
    for doc in data:
        writer.writerow(doc)
    return output.getvalue()
