"""资料与现有领域接口的核对。"""
import unittest,tempfile,json
from pathlib import Path
from lake.storage import Storage
from lake.resources import inspect

class DomainTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.store=Storage(self.root/'objects')
        self.data=json.loads(Path('data/source.json').read_text(encoding='utf-8'))
    def test_existing_reader(self):
        self.assertTrue(inspect(self.data,self.store,self.root))

    def test_revoke_is_not_release(self):
        from lake.resources import Ledger
        l=Ledger(10,10);l.grant('x',8);l.request_revoke('x')
        with self.assertRaises(ValueError):l.grant('y',3)
        self.assertEqual(l.used['x'],(8,0));l.release('x',4);l.grant('y',3)
        with self.assertRaises(ValueError):l.release('x',5)

    def test_operator_safe_point(self):
        from lake.operators import Operator
        op=Operator('x',self.store);op.append({'v':1});used=op.resident();receipt=op.spill_at_safe_point()
        self.assertEqual(receipt['released'],used);self.assertEqual(op.resident(),0);self.assertEqual(self.store.read(receipt['object']),[{'v':1}])
