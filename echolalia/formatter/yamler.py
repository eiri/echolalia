import yaml

class Formatter:

  def __init__(self):
    return None

  def add_args(self, parser):
    return parser

  def marshall(self, args, data):
    return yaml.safe_dump(data, default_flow_style=False)
