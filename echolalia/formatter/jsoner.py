import json

class Formatter:

  def __init__(self):
    return None

  def add_args(self, parser):
    return parser

  def marshall(self, args, data):
    return json.dumps(data)
