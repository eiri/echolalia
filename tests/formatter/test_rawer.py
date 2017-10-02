import unittest, argparse
from echolalia.formatter.rawer import Formatter

class RawerTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = argparse.ArgumentParser()
    self.data = [{'char': chr(i), 'order': i - 96} for i in xrange(97, 100)]
    self.formatter = Formatter()

  def test_add_args(self):
    self.assertEqual(self.formatter.add_args(self.parser), self.parser)

  def test_marshall(self):
    args = self.parser.parse_args([])
    result = self.formatter.marshall(args, self.data)
    self.assertEqual(result, self.data)
