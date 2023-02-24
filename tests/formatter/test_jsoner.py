import unittest, argparse
from echolalia.formatter.jsoner import Formatter

class JsonerTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = argparse.ArgumentParser()
    self.data = [{'char': chr(i), 'order': i - 96} for i in range(97, 100)]
    self.formatter = Formatter()

  def test_add_args(self):
    self.assertEqual(self.formatter.add_args(self.parser), self.parser)

  def test_marshall(self):
    args = self.parser.parse_args([])
    result = self.formatter.marshall(args, self.data)
    expect = '[{"char": "a", "order": 1}, {"char": "b", "order": 2}, {"char": "c", "order": 3}]'
    self.assertEqual(result, expect)
