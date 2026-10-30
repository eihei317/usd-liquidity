import sys,sqlite3,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.charts import fetch_chart_series
from scripts.utils import normalize_fred_value
class History(unittest.TestCase):
    def test_coverage_failure_blocks_publication(self):
        from scripts.pipeline import require_history_complete
        require_history_complete({'missing':[],'treasury_failures':[]})
        with self.assertRaises(RuntimeError):require_history_complete({'missing':['JGB5']})
        with self.assertRaises(RuntimeError):require_history_complete({'treasury_failures':['year unavailable']})
    def test_single_stored_spread_cannot_hide_history(self):
        rows={'SOFR':[('2026-10-27',4),('2026-10-28',4.1)],'IORB':[('2026-10-27',3.9),('2026-10-28',3.9)],'BGCR':[('2026-10-27',4),('2026-10-28',4.1)],'TGCR':[('2026-10-27',3.9),('2026-10-28',4)]}
        with patch('scripts.charts.db_metric_series',side_effect=lambda mid,days:rows.get(mid,[])),patch('scripts.charts.db_derived_series',return_value=[('2026-10-28',999)]):
            result=fetch_chart_series(45)
        self.assertEqual(2,len(result['SOFR_ANCHOR']));self.assertAlmostEqual(20,result['SOFR_ANCHOR'][-1][1])
        self.assertEqual(2,len(result['BGCR_TGCR']))
    def test_reserves_unit_consistent_in_early_history(self):
        self.assertEqual(50,normalize_fred_value('WRESBAL',50000,'USD bn'))
        self.assertEqual(3000,normalize_fred_value('WRESBAL',3000000,'USD bn'))
    def test_display_only_history_preserves_model_package(self):
        import json,copy
        from scripts.display_history import fill
        with tempfile.TemporaryDirectory(dir=ROOT/'output') as temp:
            work=Path(temp);latest=work/'output/latest';latest.mkdir(parents=True)
            with sqlite3.connect(work/'output/usd_liquidity.db') as c:
                c.execute('CREATE TABLE jpy_carry_series_ts(series_id TEXT,as_of TEXT,value REAL,unit TEXT,source TEXT,source_url TEXT,snapshot_file TEXT,ingested_at TEXT,UNIQUE(series_id,as_of))')
                c.execute('CREATE TABLE metrics_ts(metric_id TEXT,as_of TEXT,value REAL)')
                c.execute("INSERT INTO metrics_ts VALUES('IORB','2021-07-29',0.15)")
                c.execute('CREATE TABLE derived_signals_ts(signal_id TEXT,as_of TEXT,value REAL)')
                c.execute("INSERT INTO derived_signals_ts VALUES('SOFR_ANCHOR','2018-04-02',3)")
            c.close()
            coverage={'series':[{'kind':'jpy','id':'JGB5','status':'missing_history'}],'missing':['JGB5']}
            (work/'output/history_coverage.json').write_text(json.dumps(coverage),encoding='utf-8')
            (latest/'dashboard_data.json').write_text('{}',encoding='utf-8')
            package={'generated_at_bjt':'2026-10-30','data':{'facts':{}}};before=copy.deepcopy(package)
            with patch('scripts.jpy_carry.fetch_mof_jgb',return_value=({'JGB5':[('2026-10-28',1),('2026-10-29',2),('2026-11-01',3)]},{'source_url':'https://www.mof.go.jp/'})):
                fill(work,latest,package)
            self.assertEqual(before,package)
            value=json.loads((work/'output/history_coverage.json').read_text(encoding='utf-8'))
            self.assertEqual([],value['missing']);self.assertEqual(2,value['series'][0]['observations'])
            with sqlite3.connect(work/'output/usd_liquidity.db') as check:
                self.assertEqual(0,check.execute('SELECT COUNT(*) FROM derived_signals_ts').fetchone()[0])
            check.close()
if __name__=='__main__':unittest.main()
