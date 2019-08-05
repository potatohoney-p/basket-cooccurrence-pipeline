import unittest
from core import connect,ingest,build_pairs
from features import recommend
class EdgeTests(unittest.TestCase):
    def test_empty_pairs(self):
        db=connect(':memory:'); self.addCleanup(db.close); self.assertEqual(build_pairs(db),0)
        self.assertEqual(recommend(db,'x'),[])
    def test_invalid_event(self):
        db=connect(':memory:'); self.addCleanup(db.close)
        with self.assertRaises(ValueError): ingest(db,[('','tea')])
    def test_parameterized_identity(self):
        db=connect(':memory:'); self.addCleanup(db.close); ingest(db,[("x' OR 1=1 --",'tea')]); build_pairs(db)
        self.assertEqual(recommend(db,'other'),[])
