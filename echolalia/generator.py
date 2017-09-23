import os, re, logging, json
from faker import Factory

class Generator:

  def generate(self, count):
      return [self.doc() for _ in xrange(count)]


  def __init__(self, template):
    if template is None:
      raise ValueError('missing required argument "tempalte"')
    logging.basicConfig()
    self.log = logging.getLogger(__name__)
    self.fake = Factory.create()
    self.set_template(template)
    return None

  def normalize_to_json_type(self, value):
    known_types = (list, dict, str, unicode, int, float, bool, type(None))
    if not isinstance(value, known_types):
      value = str(value)
    return value

  def do_postprocess(self, value, pplist):
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

  def parse_attr(self, string):
    attrs = re.findall(r'{(\w+)}', string)
    if len(attrs) > 0:
      return(string, attrs)
    else:
      return ('{{{}}}'.format(string), [string])

  def preprocess_value(self, tpl):
    if isinstance(tpl, basestring):
      (frmt, attr) = self.parse_attr(tpl)
      post_tpl = {'frmt': frmt, 'attr': attr, 'args': ()}
    elif isinstance(tpl, dict):
      if 'attr' in tpl:
        if not isinstance(tpl['attr'], list):
          (frmt, attr) = self.parse_attr(tpl['attr'])
          tpl['attr'] = attr
          if not 'frmt' in tpl:
            tpl['frmt'] = frmt
        else:
          if not 'frmt' in tpl:
            frmt = []
            for attr in tpl['attr']:
              frmt.append('{{{}}}'.format(attr))
            tpl['frmt'] = " ".join(frmt)
        if not 'args' in tpl:
          tpl['args'] = ()
        if 'postprocess' in tpl and not isinstance(tpl['postprocess'], list):
          tpl['postprocess'] = [tpl['postprocess']]
        post_tpl = tpl
      else:
        post_tpl = self.preprocess_template(tpl)
    else:
      post_tpl = [self.preprocess_value(value) for value in tpl]
    return post_tpl

  def preprocess_template(self, tpl):
    items = tpl.iteritems()
    post_tpl = {key: self.preprocess_value(value) for key, value in items}
    return post_tpl

  def set_template(self, template):
    if os.path.isfile(template):
      template_file = template
    else:
      template_file = 'templates/{}.json'.format(template)
    self.log.debug('Reading template {}'.format(template_file))
    with open(template_file) as tpl:
      template = json.load(tpl)
      self.template = self.preprocess_template(template)
    return True

  def generate_value(self, tpl):
    if isinstance(tpl, list):
      value = [self.generate_value(value) for value in tpl]
    elif 'attr' in tpl:
      frmt = tpl['frmt']
      args = tpl['args']
      values = {}
      for attr in tpl['attr']:
        if not hasattr(self.fake, attr):
          raise ValueError('Unknown fake method {}'.format(attr))
        fun = getattr(self.fake, attr)
        values[attr] = fun(*args)
      if len(values) > 1 or isinstance(values.values()[0], (str, unicode)):
        value = frmt.format(**values)
      else:
        value = values.values()[0]
    else:
      value = self.doc(tpl)
    value = self.normalize_to_json_type(value)
    if isinstance(tpl, dict) and 'postprocess' in tpl:
      value = self.do_postprocess(value, tpl['postprocess'])
    return value

  def doc(self, tpl=None):
    if tpl is None:
      items = self.template.iteritems()
    else:
      items = tpl.iteritems()
    doc = {key: self.generate_value(value) for key, value in items}
    if tpl is None:
      self.log.debug('Generated doc {}'.format(doc))
    return doc

  def word(self):
    return self.fake.word()
