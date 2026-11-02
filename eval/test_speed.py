"""Offline correctness tests for parallel capture, revisions and incremental rebuilds."""
from contextlib import closing
import copy
import json
import sqlite3
import sys
import tempfile
import threading
import time
import unittest
from datetime import date,timedelta
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import history_cache as cache
from scripts.fetch_runtime import run_jobs
from scripts.utils import make_metric
from scripts.signals import derive_signals
from scripts.history_audit import rebuild_and_audit

class Speed(unittest.TestCase):
    def test_parallel_order_and_measured_concurrency(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'output') as folder:
            barrier=threading.Barrier(6)
            def job(i):
                if i<6:barrier.wait(timeout=3)
                time.sleep((12-i)*.001)
                return i
            path=Path(folder)/'timings.json'
            result=run_jobs([(str(i),lambda i=i:job(i)) for i in range(12)],report_path=path)
            self.assertEqual(list(range(12)),result)
            report=json.loads(path.read_text())
            self.assertEqual(6,report['observed_concurrency'])
            self.assertEqual(12,len(report['jobs']))

    def test_exception_blocks_and_saves_timing(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'output') as folder:
            def fail():raise RuntimeError('source failed')
            path=Path(folder)/'timings.json'
            with self.assertRaises(RuntimeError):run_jobs([('fail',fail)],report_path=path)
            self.assertEqual('exception',json.loads(path.read_text())['jobs'][0]['status'])

    def test_incremental_revision_retains_older_history(self):
        today=date.today()
        old=(today-timedelta(days=1000)).isoformat()
        recent=(today-timedelta(days=5)).isoformat()
        seed={'source':'FRED CSV','unit':'%','_capture_date':today.isoformat(),
              'extra':{'history':[{'date':old,'value':1},{'date':recent,'value':2}]}}
        with tempfile.TemporaryDirectory(dir=ROOT/'output') as folder,patch.object(cache,'CACHE',Path(folder)),patch.object(cache,'_seed',return_value=seed):
            plan=cache.prepare('fred:TEST','FRED CSV','%')
            self.assertTrue(plan['incremental'])
            rows,meta=cache.finish(plan,[(recent,3),(today.isoformat(),4)])
            self.assertEqual([(old,1),(recent,3),(today.isoformat(),4)],rows)
            self.assertEqual('incremental',meta['history_fetch_mode'])
            before=plan['path'].read_bytes()
            with self.assertRaises(ValueError):cache.finish(plan,[])
            self.assertEqual(before,plan['path'].read_bytes())
            with self.assertRaises(ValueError):cache.finish(plan,[(old,1)])
            self.assertEqual(before,plan['path'].read_bytes())

    def test_periodic_full_and_provenance_change(self):
        today=date.today()
        seed={'source':'FRED CSV','unit':'%','_capture_date':(today-timedelta(days=31)).isoformat(),
              'extra':{'history':[{'date':'2000-01-01','value':1},{'date':'2020-01-01','value':2}]}}
        with tempfile.TemporaryDirectory(dir=ROOT/'output') as folder,patch.object(cache,'CACHE',Path(folder)),patch.object(cache,'_seed',return_value=seed):
            self.assertFalse(cache.prepare('fred:TEST','FRED CSV','%')['incremental'])
            self.assertFalse(cache.prepare('fred:TEST','FRED API','%')['incremental'])
            self.assertFalse(cache.prepare('fred:TEST','FRED CSV','USD bn')['incremental'])

    def test_real_fetch_uses_refresh_window_and_never_stale_fallback(self):
        from scripts import fetchers
        today=date.today(); old=(today-timedelta(days=800)).isoformat(); recent=(today-timedelta(days=1)).isoformat()
        seed={'source':'FRED CSV','unit':'%','_capture_date':today.isoformat(),
              'extra':{'history':[{'date':old,'value':1},{'date':recent,'value':2}]}}
        with tempfile.TemporaryDirectory(dir=ROOT/'output') as folder,patch.object(cache,'CACHE',Path(folder)),patch.object(cache,'_seed',return_value=seed),patch.object(fetchers,'get_fred_api_key',return_value=''):
            csv=f'observation_date,TEST\n{recent},2.5\n{today.isoformat()},3\n'
            with patch.object(fetchers,'http_get_text',return_value=csv) as http:
                value=fetchers.fetch_fred_series('TEST','Test','test','%','daily')
                self.assertNotIn('1900-01-01',http.call_args.args[0])
                self.assertEqual(3,value.value)
                self.assertEqual(2.5,value.previous)
                self.assertEqual(old,value.extra['history'][0]['date'])
            with patch.object(fetchers,'http_get_text',side_effect=RuntimeError('network failed')):
                value=fetchers.fetch_fred_series('TEST','Test','test','%','daily')
                self.assertNotEqual('ok',value.status)
                self.assertIsNone(value.value)

    def test_sync_reuses_only_hash_verified_archive(self):
        from scripts import sync_to_github as sync
        with tempfile.TemporaryDirectory(dir=ROOT/'output') as folder:
            root=Path(folder);repo=root/'.sync/repository';(repo/'.git').mkdir(parents=True)
            for name in ('scripts','prompts','frontend','eval'):(root/name).mkdir()
            run=root/'output/runs/test';latest=run/'work/output/latest';latest.mkdir(parents=True)
            (latest/'snapshot.json').write_text('{}')
            (latest.parent/'usd_liquidity.db').write_bytes(b'public test database')
            def git(*args):
                if args[:3]==('remote','get-url','origin'):return sync.REMOTE
                if args[:2]==('branch','--show-current'):return 'main'
                if args[0]=='ls-remote':return 'a'*40+' refs/heads/main'
                if args[:2]==('rev-parse','HEAD'):return 'a'*40
                return ''
            with patch.object(sync,'ROOT',root),patch.object(sync,'REPO',repo),patch.object(sync,'git',side_effect=git):
                sync.sync(run,'capture')
                with patch.object(sync.gzip,'open',side_effect=AssertionError('must reuse captured database')):
                    sync.sync(run,'result')
                (repo/'artifacts/runs/test/history.sqlite.gz').write_bytes(b'corrupt')
                with patch.object(sync.gzip,'open',side_effect=RuntimeError('recompression required')):
                    with self.assertRaisesRegex(RuntimeError,'recompression required'):sync.sync(run,'result')

    def test_incremental_equals_full_after_revision_deletion_and_append(self):
        from scripts import history_audit
        def metrics(rows):
            out=[]
            for sid,base in [('SOFR',4),('IORB',3.9),('BGCR',3.95),('TGCR',3.9)]:
                values=[(d,base+v) for d,v in rows]
                out.append(make_metric(sid,sid,'test',values[-1],values[-2],'%','daily','FRED CSV','https://example.test',extra={'history':[{'date':d,'value':v} for d,v in values]}))
            return out
        def create(db):
            with closing(sqlite3.connect(db)) as c, c:
                c.execute('CREATE TABLE derived_signals_ts(signal_id TEXT,signal_name TEXT,as_of TEXT,value REAL,previous REAL,change REAL,unit TEXT,severity TEXT,snapshot_file TEXT,ingested_at TEXT)')
                c.execute('CREATE TABLE jpy_carry_series_ts(series_id TEXT,as_of TEXT,value REAL)')
        def rows(db):
            with closing(sqlite3.connect(db)) as c, c:return c.execute('SELECT signal_id,as_of,value,previous,change,unit FROM derived_signals_ts ORDER BY signal_id,as_of').fetchall()
        with tempfile.TemporaryDirectory(dir=ROOT/'output') as folder:
            base=Path(folder);a=base/'inc';b=base/'full';a.mkdir();b.mkdir()
            x=[((date.today()-timedelta(days=120-i)).isoformat(),(i%7)*.01) for i in range(100)]
            for f in (a,b):create(f/'history.db')
            m=metrics(x);sig=derive_signals(m)[0]
            with patch.object(history_audit,'OUTPUT_DIR',a):rebuild_and_audit(m,sig,a/'history.db')
            # Include an old revision, a retraction and a new observation.
            revised=copy.deepcopy(x);revised[30]=(revised[30][0],.37);del revised[50]
            revised.append(((date.today()-timedelta(days=20)).isoformat(),.25))
            m=metrics(revised);sig=derive_signals(m)[0]
            with patch.object(history_audit,'OUTPUT_DIR',a):report=rebuild_and_audit(m,sig,a/'history.db')
            with patch.object(history_audit,'OUTPUT_DIR',b):rebuild_and_audit(m,sig,b/'history.db')
            self.assertEqual('incremental',report['rebuild']['mode'])
            self.assertEqual(rows(b/'history.db'),rows(a/'history.db'))
            self.assertEqual(30,len([d for d in x if d[0]<report['rebuild']['from']]))

if __name__=='__main__':unittest.main()
