import unittest
from core import connect,ingest,build_pairs
from features import recommend,coverage
class FeatureTests(unittest.TestCase):
    def setUp(self):
        self.db=connect(':memory:'); self.addCleanup(self.db.close)
        ingest(self.db,[('a','tea'),('a','cake'),('b','tea'),('b','fruit'),('c','tea')]); build_pairs(self.db)
    def test_excludes_owned_and_stable_ties(self): self.assertEqual(recommend(self.db,'c'),[('cake',1),('fruit',1)])
    def test_support_filter(self): self.assertEqual(recommend(self.db,'c',min_support=2),[])
    def test_cold_start(self): self.assertEqual(recommend(self.db,'unknown'),[])
    def test_coverage(self): self.assertEqual(coverage(self.db),{'customers':3,'items':3,'events':5})
