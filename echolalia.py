#!/usr/bin/env python
# coding: utf-8

"""
Generate random data for your CouchDB
"""

import sys, os, argparse, logging, ConfigParser, pprint
import requests
from faker import Factory

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--debug', action='store_true')
  parser.add_argument('--integer', type=int, default=1)
  return parser.parse_args()

def init_logging(log_file, debug=True):
  requests_log = logging.getLogger('requests.packages.urllib3.connectionpool')
  if debug:
    logging.basicConfig(
      format='%(module)-14s %(funcName)s:%(lineno)d - %(message)s',
      level=logging.DEBUG)
    requests_log.setLevel(logging.DEBUG)
  else:
    logging.basicConfig(
      format='%(asctime)s [%(levelname)s] - %(message)s',
      filename=log_file,
      datefmt="%Y-%m-%d %H:%M:%S",
      level=logging.INFO)
    requests_log.disabled = True
  return logging.getLogger()

def load_config(config_file):
  Config = ConfigParser.ConfigParser()
  Config.read(config_file)
  return Config

def init_faker():
  return Factory.create()

def init_pprint():
  return pprint.PrettyPrinter(indent=4)

def main():
  args = parse_args()
  me = os.path.splitext(os.path.basename(__file__))[0]
  log_file = '{}.log'.format(me)
  pp = init_pprint()
  log = init_logging(log_file, args.debug)
  config_file = 'config.ini'
  log.debug('Reading config {}'.format(config_file))
  cfg = load_config(config_file)
  fake = init_faker()

  host = cfg.get('couchdb', 'host')
  port = int(cfg.get('couchdb', 'port'))
  log.info('Ohai {0}! Couch is on {1:s}:{2:d}'.format(fake.name(),
    host, port))

  base_url = 'http://{0:s}:{1:d}'.format(host, port)
  resp = requests.get(base_url)
  log.info(pp.pformat(resp.json()))
  log.debug('Done')
  sys.exit(0)

if __name__ == '__main__':
  main()