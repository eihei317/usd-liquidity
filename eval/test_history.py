import sys,sqlite3,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.charts import fetch_chart_series
from scripts.utils import normalize_fred_value
class History(unittest.TestCase):
    def test_single_stored_spread_cannot_hide_history(self):
        rows={'SOFR':[('2026-10-27',4),('2026-10-28',4.1)],'IORB':[('2026-10-27',3.9),('2026-10-28',3.9)],'BGCR':[('2026-10-27',4),('2026-10-28',4.1)],'TGCR':[('2026-10-27',3.9),('2026-10-28',4)]}
        with patch('scripts.charts.db_metric_series',side_effect=lambda mid,days:rows.get(mid,[])),patch('scripts.charts.db_derived_series',return_value=[('2026-10-28',999)]):
            result=fetch_chart_series(45)
        self.assertEqual(2,len(result['SOFR_ANCHOR']));self.assertAlmostEqual(20,result['SOFR_ANCHOR'][-1][1])
        self.assertEqual(2,len(result['BGCR_TGCR']))
    def test_reserves_unit_consistent_in_early_history(self):
        self.assertEqual(50,normalize_fred_value('WRESBAL',50000,'USD bn'))
        self.assertEqual(3000,normalize_fred_value('WRESBAL',3000000,'USD bn'))
if __name__=='__main__':unittest.main()
