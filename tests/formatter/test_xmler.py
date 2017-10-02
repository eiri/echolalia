import unittest, argparse
from echolalia.formatter.xmler import Formatter

class XmlerTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = argparse.ArgumentParser()
    self.data = [{'char': chr(i), 'order': i - 96} for i in xrange(97, 100)]
    self.formatter = Formatter()

  def test_add_args(self):
    new_parser = self.formatter.add_args(self.parser)
    self.assertEqual(new_parser, self.parser)
    args = new_parser.parse_args(['--root', 'channel'])
    self.assertEqual(args.root, 'channel')
    args = new_parser.parse_args([])
    self.assertEqual(args.root, 'document')      

  def test_marshall_default_root(self):
    new_parser = self.formatter.add_args(self.parser)
    args = new_parser.parse_args([])
    result = self.formatter.marshall(args, self.data)
    expect = u'<?xml version="1.0" encoding="utf-8"?>\n<document>\n    <char>a</char>\n    <order>1</order>\n</document>\n<document>\n    <char>b</char>\n    <order>2</order>\n</document>\n<document>\n    <char>c</char>\n    <order>3</order>\n</document>'
    self.assertEqual(result, expect)

  def test_marshall_custom_root(self):
    new_parser = self.formatter.add_args(self.parser)
    args = new_parser.parse_args(['--root', 'channel'])
    result = self.formatter.marshall(args, self.data)
    expect = u'<?xml version="1.0" encoding="utf-8"?>\n<channel>\n    <char>a</char>\n    <order>1</order>\n</channel>\n<channel>\n    <char>b</char>\n    <order>2</order>\n</channel>\n<channel>\n    <char>c</char>\n    <order>3</order>\n</channel>'
    self.assertEqual(result, expect)
