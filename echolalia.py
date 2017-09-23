#!/usr/bin/env python
# coding: utf-8

"""
Generate random data for your application
"""

import os, sys, argparse, logging, importlib
from echolalia.generator import Generator

def add_args(add_help=True):
  parser = argparse.ArgumentParser(
    description='Generate random data for your application',
    add_help=add_help)
  parser.add_argument('-w', '--writer', type=str, default='stdout')
  parser.add_argument('-t', '--template', type=str, required=True)
  parser.add_argument('-c', '--count', type=int, default=1)
  parser.add_argument('-v', '--verbose', action='store_true')
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
  pre_parser = add_args(add_help=False)
  (pre_args, _) = pre_parser.parse_known_args()


  mod = importlib.import_module('echolalia.writer.{}'.format(pre_args.writer))
  writer = mod.Writer()
  parser = add_args()
  parser = writer.add_args(parser)
  args = parser.parse_args()

  log = init_logging(verbose=args.verbose)
  log.debug('Start')

  template = args.template
  count = args.count
  log.debug('Generating {} docs with template {}'.format(count, template))
  generator = Generator(template)
  docs = generator.generate(count)

  # FIXME - *facepalm*
  if args.writer == 'couchdb' and args.name is None:
    args.name = generator.word()

  log.debug('Writing with writer "{}"'.format(args.writer))
  writer.write(args, docs)

  log.debug('Done')
  sys.exit(0)

if __name__ == '__main__':
  main()
