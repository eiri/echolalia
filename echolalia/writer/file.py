from __future__ import print_function
import sys

class Writer:

  def __init__(self):
    return None

  def add_args(self, parser):
    parser.add_argument('-o', '--output', type=str, required=True)
    return parser

  def write(self, args, docs):
    with open(args.output, 'w') as f:
        print(docs, file=f)

