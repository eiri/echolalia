#!/usr/bin/env python
# coding: utf-8

"""
Generate random data for your application
"""

import sys, argparse, logging, ConfigParser, importlib
from echolalia.generator import Generator

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', action='store_true')
  parser.add_argument('-l', '--log', type=str)
  parser.add_argument('--whitelist', type=str, action='append')
  parser.add_argument('-t', '--template', type=str, default='people')
  parser.add_argument('-c', '--count', type=int, default=10)
  parser.add_argument('-n', '--name', type=str)
  parser.add_argument('-w', '--writer', type=str, required=True)
  parser.add_argument('--clear', action='store_true')
  return parser.parse_args()

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

def load_config(config_file):
  Config = ConfigParser.ConfigParser()
  Config.read(config_file)
  return Config

def main():
  args = parse_args()
  log = init_logging(log_file=args.log, verbose=args.verbose)
  log.info('Start')

  config_file = 'config.ini'
  log.debug('Reading config {}'.format(config_file))
  cfg = load_config(config_file)

  generator = Generator(args.template)
  log.info('Generating {count} docs with template {template}'.format(
    count=args.count, template=args.template))
  docs = [generator.doc() for _ in xrange(args.count)]
  mod = importlib.import_module('echolalia.writer.{}'.format(args.writer))

  if args.name is None:
    args.name = generator.word()
  writer = mod.Writer(cfg)
  writer.do(args, docs)

  log.info('Done')
  sys.exit(0)

if __name__ == '__main__':
  main()
