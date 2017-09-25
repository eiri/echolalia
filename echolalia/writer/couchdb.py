import logging, requests


class Writer:

  def add_args(self, parser):
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5984)
    parser.add_argument('--name', type=str, required=True)
    parser.add_argument('--user', type=str)
    parser.add_argument('--password', type=str)
    parser.add_argument('--bulk_size', type=int, default=10)
    return parser

  def write(self, args, docs):
    self._configure(args)
    self._create_db(args.name)
    self._create_docs(args.name, docs)


  def __init__(self):
    self.log = logging.getLogger(__name__)
    requests_logger_name = 'requests.packages.urllib3.connectionpool'
    requests_log = logging.getLogger(requests_logger_name)
    requests_log.disabled = True
    return None

  def _configure(self, args):
    if args.format != 'raw':
      raise ValueError('Only accept format is "raw"')
    self.base_url = 'http://{0:s}:{1:d}'.format(args.host, args.port)
    self.headers = {'content-type': 'application/json'}
    if args.user:
      user = args.user
      password = args.password
      self.auth = (user, password)
    else:
      self.auth = ()
    self.bulk_size = args.bulk_size
    return None

  def _create_db(self, db_name):
    url = '{base_url}/{db_name}'.format(
      base_url=self.base_url, db_name=db_name)
    resp = requests.put(url, auth=self.auth, headers=self.headers)
    if resp.status_code != 201:
      raise ValueError(resp.json())
    self.log.debug('Created database {db_name}'.format(db_name=db_name))
    return db_name

  def _create_docs(self, db_name, docs):
    size = self.bulk_size
    chunks = [docs[i:i + size] for i in range(0, len(docs), size)]
    self.log.debug('Populating database {db}'.format(db=db_name))
    for chunk in chunks:
      self._bulk_insert(db_name, chunk)
    return True

  def _bulk_insert(self, db_name, docs):
    url = '{base_url}/{db_name}/_bulk_docs'.format(
      base_url=self.base_url, db_name=db_name)
    resp = requests.post(url, auth=self.auth, headers=self.headers,
      json={'docs': docs})
    if resp.status_code != 201:
      raise ValueError(resp.json())
    self.log.debug('Added {0:d} docs to database {db_name}'.format(len(docs),
      db_name=db_name))
