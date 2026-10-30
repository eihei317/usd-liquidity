"""Offline migration/replay of captured raw data; never fetches sources."""
from pathlib import Path
import json,sys,sqlite3
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from scripts.utils import Metric
from scripts.signals import derive_signals
from scripts.analysis import build_model_input_package
from scripts.dashboard import build_dashboard_data
L=ROOT/'output/latest'
def write(name,d):(L/name).write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
s=json.loads((L/'snapshot.json').read_text(encoding='utf-8'))
j=json.loads((L/'jpy_carry_history.json').read_text(encoding='utf-8'))
cut=s['generated_at_bjt'][:10]
h=j['jpy_carry']['history']
for key in ('JGB2','JGB5','JGB10','JGB30'):
    if key in h:h[key]=[r for r in h[key] if r['date']>=cut]
for key in ('US_JP_2Y','US_JP_10Y'):h[key]=[]
for chart in j.get('charts',[]):
    for series in chart.get('series',[]):
        key=series.get('id')
        if key in h and (key.startswith('JGB') or key.startswith('US_JP')):
            series['points']=h[key]
j['jpy_carry'].setdefault('notes',[]).append('旧版日债日期回填影响的历史已隔离；当前保留本轮实际报价，美日利差缺同期观测，保持未知。')
write('jpy_carry_history.json',j)
metrics=[Metric(**r) for r in s['metrics']];signals,score,highlights=derive_signals(metrics)
from dataclasses import asdict
s['derived_signals']=[asdict(r) for r in signals];s['method_version']='2.0'
write('snapshot.json',s)
m=build_model_input_package(s.get('trigger','离线修复回放'),s['generated_at_bjt'],metrics,signals,s.get('upcoming_auctions'));m['method_version']='2.0';write('model_input.json',m)
charts=json.loads((L/'charts.json').read_text(encoding='utf-8'))
d=build_dashboard_data(s.get('trigger','离线修复回放'),s['generated_at_bjt'],s,metrics,signals,charts,[],s.get('upcoming_auctions'));write('dashboard_data.json',d)
with sqlite3.connect(str(ROOT/'output/usd_liquidity.db')) as c:
    ids=('JGB2','JGB5','JGB10','JGB30','US_JP_2Y','US_JP_10Y')
    c.execute('CREATE TABLE IF NOT EXISTS quarantine_jpy_v1 AS SELECT * FROM jpy_carry_series_ts WHERE 0')
    for key in ids:
        c.execute('INSERT INTO quarantine_jpy_v1 SELECT * FROM jpy_carry_series_ts WHERE series_id=? AND as_of < ?',(key,cut))
        c.execute('DELETE FROM jpy_carry_series_ts WHERE series_id=? AND as_of < ?',(key,cut))
print('Offline fact rebuild complete; no network calls')
