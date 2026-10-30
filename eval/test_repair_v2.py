"""Offline regression cases for observed defects; no network or state writes."""
import copy,json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.analysis_validator import _collect_facts,_validate_claim_numbers,_validate_p0
class Regression(unittest.TestCase):
    def setUp(self):
        self.facts={'metric:TGCR':{'value':3.92,'change':-.02,'unit':'%','as_of':'2026-10-28'},'metric:SOFR_VOLUME':{'value':3074,'change':-73,'unit':'USD bn','as_of':'2026-10-28'}}
    def check(self,text,fid):
        errors=[];_validate_claim_numbers('$',{'evidence':[text],'fact_ids':[fid]},self.facts,errors);return errors
    def test_bp(self):self.assertFalse(self.check('TGCR -2.00bp（2026-10-28，-2.00bp）','metric:TGCR'))
    def test_wrong_unit(self):self.assertTrue(self.check('SOFR 3074.00bp','metric:SOFR_VOLUME'))
    def test_wrong_date(self):self.assertTrue(self.check('TGCR 3.92%（1999-01-01，-2.00bp）','metric:TGCR'))
    def test_p0(self):
        errors=[];_validate_p0({'risk_flags':[{'priority':'P0','type':'market','severity':'high','claim_type':'scenario','fact_ids':['metric:SOFR','derived:SOFR_ANCHOR']}]},{'metric:SOFR':{'value':4},'derived:SOFR_ANCHOR':{'value':1,'base_fact_ids':['metric:SOFR']}},errors);self.assertGreaterEqual(len(errors),2)
if __name__=='__main__':unittest.main()
