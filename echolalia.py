#!/usr/bin/env python
# coding: utf-8

"""
Generate random data for your CouchDB
"""

import sys, os, argparse, logging, ConfigParser, json
from pprint import pformat
import requests
from faker import Factory

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '--debug', action='store_true')
  parser.add_argument('--clear', action='store_true')
  parser.add_argument('-t', '--template', type=str, default='people')
  parser.add_argument('-c', '--count', type=int, default=10)
  parser.add_argument('-n', '--name', type=str)
  return parser.parse_args()

def init_logging(log_file, debug=True):
  requests_log = logging.getLogger('requests.packages.urllib3.connectionpool')
  if debug:
    logging.basicConfig(
      format='%(levelname)-9s %(funcName)s:%(lineno)d - %(message)s',
      level=logging.DEBUG)
    requests_log.setLevel(logging.DEBUG)
  else:
    logging.basicConfig(
      format='%(asctime)s [%(levelname)s] - %(message)s',
      filename=log_file,
      datefmt="%Y-%m-%d %H:%M:%S",
      level=logging.INFO)
    requests_log.disabled = True
  global log
  log = logging.getLogger()
  return True

def load_config(config_file):
  Config = ConfigParser.ConfigParser({'user' : None, 'password' : ''})
  Config.read(config_file)
  return Config

def init_faker():
  global fake
  fake = Factory.create()
  return True

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

def generate_value(tpl):
  if isinstance(tpl, dict):
    if 'attr' in tpl:
      attr = tpl['attr']
      args = tpl['args']
    else:
      attr = generate_doc(tpl)
  else:
    attr = tpl
    args = ()
  if isinstance(attr, basestring) and hasattr(fake, attr):
    fun = getattr(fake, attr)
    value = fun(*args)
  else:
    value = attr
  if isinstance(value, (list,dict,str,unicode,int,float,bool,type(None))):
    return value
  else:
    return str(value)

def generate_doc(tpl):
  doc = {key: generate_value(value) for key, value in tpl.iteritems()}
  log.debug('Generated doc {}'.format(pformat(doc)))
  return doc

def bulk_insert(db_name, docs):
  url = '{base_url}/{db_name}/_bulk_docs'.format(base_url=base_url,
    db_name=db_name)
  data = json.dumps({'docs': docs})
  resp = requests.post(url, auth=auth, headers=headers, data=data)
  if resp.status_code != 201:
    raise ValueError(pformat(resp.json()))
  log.info('Added {0:d} docs to database {db_name}'.format(len(docs),
    db_name=db_name))

def create_docs(db_name, template={}, count=10, bulk_size=10):
  for _ in xrange(count / bulk_size):
    docs = []
    for _ in xrange(bulk_size):
      doc = generate_doc(template)
      docs.append(doc)
    bulk_insert(db_name, docs)
  docs = []
  for _ in xrange(count % bulk_size):
    doc = generate_doc(template)
    docs.append(doc)
  if len(docs) > 0:
    bulk_insert(db_name, docs)
  return True

def remove_all_dbs():
  url = '{base_url}/_all_dbs'.format(base_url=base_url)
  resp = requests.get(url, auth=auth, headers=headers)
  for db_name in resp.json():
    if db_name.startswith('_'):
      continue
    url = '{base_url}/{db_name}'.format(base_url=base_url, db_name=db_name)
    resp = requests.delete(url, auth=auth, headers=headers)
    if resp.status_code == requests.codes.ok:
      log.info('Deleted database {db_name}'.format(db_name=db_name))

def main():
  args = parse_args()
  script_name = os.path.splitext(os.path.basename(__file__))[0]
  log_file = '{}.log'.format(script_name)
  init_logging(log_file, args.debug)
  init_faker()

  config_file = 'config.ini'
  log.debug('Reading config {}'.format(config_file))
  cfg = load_config(config_file)

  setup_client(cfg)
  if args.clear:
    remove_all_dbs()
  else:
    db_name = args.name if args.name is not None else fake.word()
    create_db(db_name)
    log.info('Populating database with template {}'.format(args.template))
    if os.path.isfile(args.template):
      template_file = args.template
    else:
      template_file = 'templates/{}.json'.format(args.template)
    log.debug('Reading template {}'.format(template_file))
    with open(template_file) as tpl:
      template = json.load(tpl)
    create_docs(db_name, template=template, count=args.count)

  log.info('Done')
  sys.exit(0)

if __name__ == '__main__':
  main()