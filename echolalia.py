#!/usr/bin/env python
# coding: utf-8

"""
Generate random data for your application
"""

import argparse, logging, importlib
from echolalia.generator import Generator

def add_args():
  parser = argparse.ArgumentParser(
    description='Generate random data for your application')
  parser.add_argument('-w', '--writer', type=str, default='stdout')
  parser.add_argument('-f', '--format', type=str, default='json')
  parser.add_argument('-c', '--count', type=int, default=1)
  parser.add_argument('-v', '--verbose', action='store_true')
  group = parser.add_mutually_exclusive_group(required=True)
  group.add_argument('-t', '--template', type=str)
  group.add_argument('-i', '--items', type=str, action='append', metavar='KEY=VALUE')
  return parser

def init_logging(verbose=False):
  if verbose:
    level = logging.DEBUG
  else:
    level = logging.ERROR
  logging.basicConfig(
    format='%(levelname)-9s %(funcName)s:%(lineno)d - %(message)s',
    datefmt='%H:%M:%S',
    level=level)
  return logging.getLogger()

def main():
  parser = add_args()
  (args, _) = parser.parse_known_args()

  writer = args.writer
  formatter = args.format

  mod = importlib.import_module('echolalia.writer.{}'.format(writer))
  writer = mod.Writer()
  parser = writer.add_args(parser)

  mod = importlib.import_module('echolalia.formatter.{}er'.format(formatter))
  formatter = mod.Formatter()
  parser = formatter.add_args(parser)
  args = parser.parse_args()

  log = init_logging(verbose=args.verbose)
  log.debug('Start')

  template = args.template
  count = args.count
  if template is None:
    log.debug('Generating {} docs with {} item(s)'.format(count, len(args.items)))
    items = {}
    for item in args.items:
      kv = item.split("=", 1)
      if len(kv) == 2:
        items[kv[0]] = kv[1]
      else:
        items[item] = item
    generator = Generator(items=items)
  else:
    log.debug('Generating {} docs with template {}'.format(count, template))
    generator = Generator(template=template)
  data = generator.generate(count)

  log.debug('Marshalling with formatter "{}"'.format(args.format))
  docs = formatter.marshall(args, data)

  log.debug('Writing with writer "{}"'.format(args.writer))
  writer.write(args, docs)

  log.debug('Done')
  parser.exit(status=0)

if __name__ == '__main__':
  main()
