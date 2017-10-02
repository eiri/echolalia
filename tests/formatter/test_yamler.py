import unittest, argparse
from echolalia.formatter.yamler import Formatter

class YamlerTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = argparse.ArgumentParser()
    self.data = [{'char': chr(i), 'order': i - 96} for i in xrange(97, 100)]
    self.formatter = Formatter()

  def test_add_args(self):
    new_parser = self.formatter.add_args(self.parser)
    self.assertEqual(new_parser, self.parser)

  def test_marshall_header(self):
    new_parser = self.formatter.add_args(self.parser)
    args = new_parser.parse_args([])
    result = self.formatter.marshall(args, self.data)
    expect = "- char: a\n  order: 1\n- char: b\n  order: 2\n- char: c\n  order: 3\n"
    self.assertEqual(result, expect)
