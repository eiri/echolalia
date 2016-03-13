#!/usr/bin/env python
# coding: utf-8

"""
Generate random data for your application
"""

import sys, argparse, logging, ConfigParser, json
from pprint import pformat
import requests

from echolalia.generator import Generator

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-v', '--verbose', action='store_true')
  parser.add_argument('-l', '--log', type=str)
  parser.add_argument('--whitelist', type=str, action='append')
  parser.add_argument('-t', '--template', type=str, default='people')
  parser.add_argument('-c', '--count', type=int, default=10)
  parser.add_argument('-n', '--name', type=str)
  parser.add_argument('--clear', action='store_true')
  return parser.parse_args()

def init_logging(log_file=None, verbose=False):
  requests_log = logging.getLogger('requests.packages.urllib3.connectionpool')
  if log_file is None:
    if verbose:
      level = logging.DEBUG
      fmt = '%(levelname)-9s %(funcName)s:%(lineno)d - %(message)s'
      requests_log.setLevel(level)
    else:
      level = logging.INFO
      fmt = '%(asctime)s - %(message)s'
      requests_log.disabled = True
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
    requests_log.disabled = True
  global log
  log = logging.getLogger()
  return True

def load_config(config_file):
  Config = ConfigParser.ConfigParser({
    'user' : None,
    'password' : '',
    'whitelist': '',
    'bulk_size': '10'
  })
  Config.read(config_file)
  return Config

def setup_client(cfg):
  global base_url
  global auth
  global headers
  host = cfg.get('couchdb', 'host')
  port = int(cfg.get('couchdb', 'port'))
  base_url = 'http://{0:s}:{1:d}'.format(host, port)
  headers = {'content-type': 'application/json'}
  if cfg.get('couchdb', 'user') is not None:
    user = cfg.get('couchdb', 'user')
    password = cfg.get('couchdb', 'password')
    auth = (user, password)
  else:
    auth = ()
  return True

def create_db(db_name):
  url = '{base_url}/{db_name}'.format(base_url=base_url, db_name=db_name)
  resp = requests.put(url, auth=auth, headers=headers)
  if resp.status_code != 201:
    raise ValueError(pformat(resp.json()))
  log.info('Created database {db_name}'.format(db_name=db_name))
  return db_name

def bulk_insert(db_name, docs):
  url = '{base_url}/{db_name}/_bulk_docs'.format(base_url=base_url,
    db_name=db_name)
  data = json.dumps({'docs': docs})
  resp = requests.post(url, auth=auth, headers=headers, data=data)
  if resp.status_code != 201:
    raise ValueError(pformat(resp.json()))
  log.info('Added {0:d} docs to database {db_name}'.format(len(docs),
    db_name=db_name))

def create_docs(db_name, docs, bulk_size):
  if bulk_size < 1:
    raise ValueError('bulk_size has to exceed 0')
  chunks = [docs[i:i + bulk_size] for i in range(0, len(docs), bulk_size)]
  for chunk in chunks:
    bulk_insert(db_name, chunk)
  return True

def remove_all_dbs(whitelist):
  url = '{base_url}/_all_dbs'.format(base_url=base_url)
  resp = requests.get(url, auth=auth, headers=headers)
  for db_name in resp.json():
    if db_name.startswith('_'):
      log.info('Skipping system database {db_name}'.format(db_name=db_name))
      continue
    if db_name in whitelist:
      log.info('Skipping whitelisted database {db_name}'.format(
        db_name=db_name))
      continue
    url = '{base_url}/{db_name}'.format(base_url=base_url, db_name=db_name)
    resp = requests.delete(url, auth=auth, headers=headers)
    if resp.status_code == requests.codes.ok:
      log.info('Deleted database {db_name}'.format(db_name=db_name))

def main():
  args = parse_args()
  init_logging(log_file=args.log, verbose=args.verbose)

  config_file = 'config.ini'
  log.debug('Reading config {}'.format(config_file))
  cfg = load_config(config_file)

  generator = Generator(args.template)
  setup_client(cfg)

  if args.clear:
    whitelist = [n.strip() for n in cfg.get('couchdb', 'whitelist').split(',')]
    if args.whitelist is not None:
      whitelist.extend(args.whitelist)
    remove_all_dbs(whitelist)
  else:
    db_name = args.name if args.name is not None else generator.word()
    create_db(db_name)
    log.info('Populating database with template {}'.format(args.template))
    bulk_size = int(cfg.get('couchdb', 'bulk_size'))
    docs = [generator.doc() for _ in xrange(args.count)]
    create_docs(db_name, docs, bulk_size=bulk_size)

  log.info('Done')
  sys.exit(0)

if __name__ == '__main__':
  main()
