import unittest, argparse, sys, io
from echolalia.writer.stdout import Writer

class StdoutTestCase(unittest.TestCase):

  def setUp(self):
    self.parser = argparse.ArgumentParser()
    self.data = [{chr(i): i - 96} for i in range(97, 123)]
    self.writer = Writer()

  def test_add_args(self):
    self.assertEqual(self.writer.add_args(self.parser), self.parser)

  def test_write(self):
    saved_stdout = sys.stdout
    try:
      output = io.StringIO()
      sys.stdout = output
      args = self.parser.parse_args([])
      self.writer.write(args, self.data)
      self.assertEqual(output.getvalue(), "{}\n".format(self.data))
      output.close()
    finally:
      sys.stdout = saved_stdout
