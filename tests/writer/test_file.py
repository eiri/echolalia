import unittest, argparse, os, tempfile
from echolalia.writer.file import Writer

class FileTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = argparse.ArgumentParser()
    self.data = [{chr(i): i - 96} for i in range(97, 123)]
    self.writer = Writer()

  def test_add_args(self):
    new_parser = self.writer.add_args(self.parser)
    self.assertEqual(new_parser, self.parser)
    args = new_parser.parse_args(['-o', 'output.json'])
    self.assertEqual(args.output, 'output.json')
    with self.assertRaises(SystemExit):
      new_parser.parse_args([])

  def test_write(self):
    temp = tempfile.NamedTemporaryFile(delete=False)
    try:
      args = self.parser.parse_args([])
      args.output = temp.name
      self.writer.write(args, self.data)
      with open(temp.name, 'r') as f:
        self.assertEqual(f.read(), "{}\n".format(self.data))
    finally:
      os.unlink(temp.name)
