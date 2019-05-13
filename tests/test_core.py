import unittest
from core import connect,ingest,build_pairs
class CoreTests(unittest.TestCase):
    def setUp(self): self.db=connect(':memory:'); self.addCleanup(self.db.close)
    def test_dedup(self): self.assertEqual(ingest(self.db,[('a','tea'),('a','tea')]),1)
    def test_support(self):
        ingest(self.db,[('a','tea'),('a','cake'),('b','tea'),('b','cake')],1)
        self.assertEqual(build_pairs(self.db),1)
        self.assertEqual(self.db.execute('SELECT * FROM pairs').fetchone(),('cake','tea',2))
    def test_rebuild_not_additive(self):
        ingest(self.db,[('a','x'),('a','y')]); build_pairs(self.db); build_pairs(self.db)
        self.assertEqual(self.db.execute('SELECT support FROM pairs').fetchone()[0],1)
