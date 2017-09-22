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
  parser.add_argument('-l', '--log', type=str)
  parser.add_argument('-v', '--verbose', action='store_true')
  return parser

def init_logging(log_file=None, verbose=False):
  if log_file is None:
    if verbose:
      level = logging.DEBUG
      fmt = '%(levelname)-9s %(funcName)s:%(lineno)d - %(message)s'
    else:
      level = logging.INFO
      fmt = '%(asctime)s - %(message)s'
    logging.basicConfig(
      format=fmt,
      datefmt='%H:%M:%S',
      level=level)
  else:
    logging.basicConfig(
      format='%(asctime)s [%(levelname)s] - %(message)s',
      filename=log_file,
      datefmt='%Y-%m-%d %H:%M:%S',
      level=logging.INFO)
  return logging.getLogger()

def main():
  pre_parser = add_args(add_help=False)
  (pre_args, _) = pre_parser.parse_known_args()
  # TODO change approach to pass-through default writer
  if pre_args.writer is None:
    pre_parser.print_help()
    pre_parser.exit(0)

  log = init_logging(log_file=pre_args.log, verbose=pre_args.verbose)

  mod = importlib.import_module('echolalia.writer.{}'.format(pre_args.writer))
  writer = mod.Writer()
  parser = add_args()
  parser = writer.add_args(parser)
  args = parser.parse_args()

  log.info('Start')

  tpl = args.template
  count = args.count
  generator = Generator(tpl)
  log.info('Generating {count} docs with template {template}'.format(
    count=count, template=tpl))
  docs = [generator.doc() for _ in xrange(count)]

  # FIXME - *facepalm*
  if args.writer == 'couchdb' and args.name is None:
    args.name = generator.word()

  writer.do(args, docs)

  log.info('Done')
  sys.exit(0)

if __name__ == '__main__':
  main()
