from __future__ import print_function
import json, sys

class Writer:

  def __init__(self):
    return None

  def add_args(self, parser):
    return parser

  def configure(self, cfg, args):
    return cfg

  def do(self, cfg, docs):
    print(json.dumps(docs), file=sys.stdout)

