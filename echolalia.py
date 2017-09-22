#!/usr/bin/env python
# coding: utf-8

"""
Generate random data for your application
"""

import os, sys, argparse, logging, ConfigParser, importlib
from echolalia.generator import Generator

def add_args(add_help=True):
  parser = argparse.ArgumentParser(
    description='Generate random data for your application',
    add_help=add_help)
  parser.add_argument('-w', '--writer', type=str)
  parser.add_argument('-t', '--template', type=str)
  parser.add_argument('-c', '--count', type=int)
  parser.add_argument('-l', '--log', type=str)
  parser.add_argument('-v', '--verbose', action='store_true')
  return parser

def configure(cfg, args):
  if not cfg.has_section('main'):
    cfg.add_section('main')
  for key, value in vars(args).iteritems():
    if value is not None:
      cfg.set('main', key, str(value))
  return cfg

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

def show_config(log, cfg):
  for section in cfg.sections():
    log.info('[{}]'.format(section))
    for (item, value) in cfg.items(section):
      log.info('{} = {}'.format(item, value))

def main():
  pre_parser = add_args(add_help=False)
  (pre_args, _) = pre_parser.parse_known_args()
  # TODO change approach to pass-through default writer
  if pre_args.writer is None:
    pre_parser.print_help()
    pre_parser.exit(0)

  log = init_logging(log_file=pre_args.log, verbose=pre_args.verbose)

  cfg = ConfigParser.ConfigParser()
  config_file = os.getenv('ECHOLALIA_CONFIG', "~/.echolalia")
  if os.path.isfile(config_file):
    cfg.read(config_file)
  cfg = configure(cfg, pre_args)
  if not cfg.has_option('main', 'count'):
    cfg.set('main', 'count', '10')
  # FIXME - will need something more civilized here
  if not cfg.has_option('main', 'template'):
    cfg.set('main', 'template', 'people')

  mod = importlib.import_module('echolalia.writer.{}'.format(pre_args.writer))
  writer = mod.Writer()
  parser = add_args()
  parser = writer.add_args(parser)
  args = parser.parse_args()
  cfg = writer.configure(cfg, args)

  log.info('Start')

  tpl = cfg.get('main', 'template')
  count = cfg.getint('main', 'count')
  generator = Generator(tpl)
  log.info('Generating {count} docs with template {template}'.format(
    count=count, template=tpl))
  docs = [generator.doc() for _ in xrange(count)]

  # FIXME - *facepalm*
  if args.writer is 'couchdb':
    if args.name is None:
      cfg.set('couchdb', 'name', generator.word())
    else:
      cfg.set('couchdb', 'name', args.name)

  writer.do(cfg, docs)

  log.info('Done')
  sys.exit(0)

if __name__ == '__main__':
  main()
