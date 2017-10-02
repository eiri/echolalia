import unittest, argparse
from echolalia.formatter.csver import Formatter

class CsverTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = argparse.ArgumentParser()
    self.data = [{'char': chr(i), 'order': i - 96} for i in xrange(97, 100)]
    self.formatter = Formatter()

  def test_add_args(self):
    new_parser = self.formatter.add_args(self.parser)
    self.assertEqual(new_parser, self.parser)
    args = new_parser.parse_args(['--with_header'])
    self.assertTrue(args.with_header)
    args = new_parser.parse_args([])
    self.assertFalse(args.with_header)      

  def test_marshall_no_header(self):
    new_parser = self.formatter.add_args(self.parser)
    args = new_parser.parse_args([])
    result = self.formatter.marshall(args, self.data)
    expect = "a,1\r\nb,2\r\nc,3\r\n"
    self.assertEqual(result, expect)

  def test_marshall_with_header(self):
    new_parser = self.formatter.add_args(self.parser)
    args = new_parser.parse_args(['--with_header'])
    result = self.formatter.marshall(args, self.data)
    expect = "char,order\r\na,1\r\nb,2\r\nc,3\r\n"
    self.assertEqual(result, expect)

