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
  if isinstance(tpl, list):
    value = [generate_value(value) for value in tpl]
  elif 'attr' in tpl:
    frmt = tpl['frmt']
    attr = tpl['attr']
    args = tpl['args']
    if not hasattr(fake, attr):
      raise ValueError('Unknown fake method {}'.format(attr))
    fun = getattr(fake, attr)
    value = fun(*args)
    if isinstance(value, (str,unicode)):
      value = frmt.format(**{attr : value})
  else:
    value = generate_doc(tpl)
  value = normalize_to_json_type(value)
  if isinstance(tpl, dict) and 'postprocess' in tpl:
    value = do_postprocess(value, tpl['postprocess'])
  return value

def generate_doc(tpl):
  doc = {key: generate_value(value) for key, value in tpl.iteritems()}
  log.debug('Generated doc {}'.format(pformat(doc)))
  return doc

def normalize_to_json_type(value):
  if not isinstance(value, (list,dict,str,unicode,int,float,bool,type(None))):
    value = str(value)
  return value

def do_postprocess(value, pplist):
  value = str(value)
  for pp in pplist:
    if isinstance(pp, dict):
      attr = pp['attr']
      args = [value]
      args.extend(pp['args'])
    else:
      attr = pp
      args = [value]
    if not hasattr(str, attr):
      continue
    fun = getattr(str, attr)
    value = fun(*args)
  return value

def preprocess_value(tpl):
  if isinstance(tpl, basestring):
    post_tpl = {'frmt': '{{{}}}'.format(tpl), 'attr': tpl, 'args': ()}
  elif isinstance(tpl, dict):
    if 'attr' in tpl:
      if not 'frmt' in tpl:
        tpl['frmt'] = '{{{}}}'.format(tpl['attr'])
      if not 'args' in tpl:
        tpl['args'] = ()
      if 'postprocess' in tpl and not isinstance(tpl['postprocess'], list):
        tpl['postprocess'] = [tpl['postprocess']]
      post_tpl = tpl
    else:
      post_tpl = preprocess_template(tpl)
  else:
    post_tpl = [preprocess_value(value) for value in tpl]
  return post_tpl

def preprocess_template(tpl):
  post_tpl = {key: preprocess_value(value) for key, value in tpl.iteritems()}
  return post_tpl

def bulk_insert(db_name, docs):
  url = '{base_url}/{db_name}/_bulk_docs'.format(base_url=base_url,
    db_name=db_name)
  data = json.dumps({'docs': docs})
  resp = requests.post(url, auth=auth, headers=headers, data=data)
  if resp.status_code != 201:
    raise ValueError(pformat(resp.json()))
  log.info('Added {0:d} docs to database {db_name}'.format(len(docs),
    db_name=db_name))

def create_docs(db_name, template, count, bulk_size):
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
  init_faker()

  config_file = 'config.ini'
  log.debug('Reading config {}'.format(config_file))
  cfg = load_config(config_file)

  setup_client(cfg)
  if args.clear:
    whitelist = [n.strip() for n in cfg.get('couchdb', 'whitelist').split(',')]
    if args.whitelist is not None:
      whitelist.extend(args.whitelist)
    remove_all_dbs(whitelist)
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
      template = preprocess_template(template)
    bulk_size = int(cfg.get('couchdb', 'bulk_size'))
    create_docs(db_name, template=template, count=args.count,
      bulk_size=bulk_size)

  log.info('Done')
  sys.exit(0)

if __name__ == '__main__':
  main()