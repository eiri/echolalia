import unittest, argparse, json
from echolalia.formatter.jsoner import Formatter

class JsonerTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = argparse.ArgumentParser()
    self.data = [{chr(i): i - 96} for i in xrange(97, 123)]
    self.formatter = Formatter()

  def test_add_args(self):
    self.assertEqual(self.formatter.add_args(self.parser), self.parser)

  def test_marshall(self):
    args = self.parser.parse_args([])
    result = self.formatter.marshall(args, self.data)
    self.assertEqual(result, json.dumps(self.data))
