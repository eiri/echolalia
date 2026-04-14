class Writer:

    def __init__(self) -> None:
        pass

    def add_args(self, parser):
        parser.add_argument("-o", "--output", type=str, required=True)
        return parser

    def write(self, args, docs) -> None:
        with open(args.output, "w") as f:
            print(docs, file=f)
