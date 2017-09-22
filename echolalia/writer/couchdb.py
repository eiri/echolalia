import logging, requests


class Writer:

  def __init__(self):
    logging.basicConfig()
    self.log = logging.getLogger(__name__)
    requests_logger_name = 'requests.packages.urllib3.connectionpool'
    requests_log = logging.getLogger(requests_logger_name)
    requests_log.disabled = True
    return None

  def add_args(self, parser):
    parser.add_argument('--whitelist', type=str, action='append', default=[])
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5984)
    parser.add_argument('--name', type=str)
    parser.add_argument('--user', type=str)
    parser.add_argument('--password', type=str)
    parser.add_argument('--bulk_size', type=int, default=10)
    parser.add_argument('--clear', action='store_true')
    return parser

  def configure(self, args):
    self.base_url = 'http://{0:s}:{1:d}'.format(args.host, args.port)
    self.headers = {'content-type': 'application/json'}
    if args.user:
      user = args.user
      password = args.password
      self.auth = (user, password)
    else:
      self.auth = ()

    self.whitelist = []
    for n in args.whitelist:
      self.whitelist.append(n.strip())
    if args.whitelist is not None:
      self.whitelist.extend(args.whitelist)

    self.bulk_size = args.bulk_size
    return None

  def do(self, args, docs):
    self.configure(args)
    if args.clear:
      self.remove_all_dbs()
    else:
      self.create_db(args.name)
      self.create_docs(args.name, docs)

  def create_db(self, db_name):
    url = '{base_url}/{db_name}'.format(
      base_url=self.base_url, db_name=db_name)
    resp = requests.put(url, auth=self.auth, headers=self.headers)
    if resp.status_code != 201:
      raise ValueError(resp.json())
    self.log.info('Created database {db_name}'.format(db_name=db_name))
    return db_name

  def bulk_insert(self, db_name, docs):
    url = '{base_url}/{db_name}/_bulk_docs'.format(
      base_url=self.base_url, db_name=db_name)
    resp = requests.post(url, auth=self.auth, headers=self.headers,
      json={'docs': docs})
    if resp.status_code != 201:
      raise ValueError(resp.json())
    self.log.debug('Added {0:d} docs to database {db_name}'.format(len(docs),
      db_name=db_name))

  def create_docs(self, db_name, docs):
    size = self.bulk_size
    chunks = [docs[i:i + size] for i in range(0, len(docs), size)]
    self.log.info('Populating database {db}'.format(db=db_name))
    for chunk in chunks:
      self.bulk_insert(db_name, chunk)
    return True

  def remove_all_dbs(self):
    url = '{base_url}/_all_dbs'.format(base_url=self.base_url)
    resp = requests.get(url, auth=self.auth, headers=self.headers)
    for db_name in resp.json():
      if db_name.startswith('_'):
        self.log.info('Skipping system database {db_name}'.format(
          db_name=db_name))
        continue
      if db_name in self.whitelist:
        self.log.info('Skipping whitelisted database {db_name}'.format(
          db_name=db_name))
        continue
      url = '{base_url}/{db_name}'.format(base_url=self.base_url,
        db_name=db_name)
      resp = requests.delete(url, auth=self.auth, headers=self.headers)
      if resp.status_code == requests.codes.ok:
        self.log.info('Deleted database {db_name}'.format(db_name=db_name))
