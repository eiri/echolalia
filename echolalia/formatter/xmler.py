import lazyxml

class Formatter:

  def __init__(self):
    return None

  def add_args(self, parser):
    parser.add_argument('--root', type=str, default='document')
    return parser

  def marshall(self, args, data):
    return lazyxml.dumps(data, root=args.root, cdata=False, indent= ' ' * 4)
