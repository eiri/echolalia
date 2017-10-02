import unittest
from echolalia.generator import Generator

class GeneratorTestCase(unittest.TestCase):

  def setUp(self):
    self.items = ['pystr', 'pyint']

  def test_generate(self):
    generator = Generator(items=self.items)
    docs = generator.generate(3)
    self.assertEqual(len(docs), 3)
    for doc in docs:
      self.assertIn('pystr', doc)
      self.assertIn('pyint', doc)
      self.assertIsInstance(doc, dict)
      self.assertIsInstance(doc['pystr'], str)
      self.assertIsInstance(doc['pyint'], int)
