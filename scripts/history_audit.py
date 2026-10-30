"""Capture source histories and rebuild every calculable signal by observation date."""
import json, math, sqlite3
from pathlib import Path
from dataclasses import replace, asdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from .utils import Metric, OUTPUT_DIR

def hydrate(metrics):
    from .fetchers import fetch_treasury_par_yield_curve, fetch_treasury_par_real_yield_curve
    cache=OUTPUT_DIR.parent/'.workbuddy/cache/treasury_history'
    cache.mkdir(parents=True,exist_ok=True)
    jobs=[]; historical={}; failures=[]
    def annual(kind,year):
        path=cache/f'{kind}_{year}.json'
        if path.exists():return json.loads(path.read_text(encoding='utf-8'))
        result=(fetch_treasury_par_yield_curve if kind=='nominal' else fetch_treasury_par_real_yield_curve)(year)
        if not result:raise RuntimeError(f'Treasury {kind} {year} unavailable')
        result={k:asdict(v) for k,v in result.items()}
        if year<datetime.now().year:path.write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
        return result
    with ThreadPoolExecutor(max_workers=6) as pool:
        for kind,start in [('nominal',1990),('real',2003)]:
            for year in range(start,datetime.now().year+1):jobs.append(pool.submit(annual,kind,year))
        for f in as_completed(jobs):
            try:
                for mid,row in f.result().items():historical.setdefault((mid,row['source']),[]).extend(row.get('extra',{}).get('history',[]))
            except Exception as e:failures.append(str(e))
    for m in metrics:
        if m.id in ('T10Y2Y','T10Y3M') and m.source.startswith('Treasury.gov'):
            a={r['date']:r['value'] for r in historical.get(('DGS10',m.source),[])}
            b={r['date']:r['value'] for r in historical.get(('DGS2' if m.id=='T10Y2Y' else 'DGS3MO',m.source),[])}
            historical[(m.id,m.source)]=[{'date':d,'value':a[d]-b[d]} for d in sorted(a.keys()&b.keys())]
        extra=historical.get((m.id,m.source),[])
        if extra:
            points={r['date']:r['value'] for r in extra if r['date']<=m.as_of}
            points.update({r['date']:r['value'] for r in m.extra.get('history',[]) if r['date']<=m.as_of})
            m.extra['history']=[{'date':d,'value':v} for d,v in sorted(points.items())]
        m.extra['history_download_failures']=failures if m.source.startswith('Treasury.gov') else []
    return metrics

def rebuild_and_audit(metrics,signals,db_path):
    from .analysis import _build_canonical_metrics
    from . import signals as engine
    canonical,_=_build_canonical_metrics(metrics)
    selected=[]; report=[]; all_dates=set()
    for f in canonical:
        matches=[m for m in metrics if m.id==f['id'] and m.source==f['source'] and m.as_of==f['as_of']]
        if not matches:continue
        m=matches[0]; points={}
        for r in m.extra.get('history',[]):
            d,v=r.get('date'),r.get('value')
            if d and d<=m.as_of and isinstance(v,(int,float)) and math.isfinite(v):points[d]=v
        if m.value is not None and m.as_of:points[m.as_of]=m.value
        rows=sorted(points.items());all_dates.update(points)
        selected.append((m,rows,points))
        report.append({'kind':'metric','id':m.id,'source':m.source,'observations':len(rows),'first':rows[0][0] if rows else None,'last':rows[-1][0] if rows else None,'status':'history_available' if len(rows)>1 else 'missing_history','source_failures':m.extra.get('history_download_failures',[])})
    counts={}; first={};last={}; previous={};index={m.id:0 for m,_,_ in selected}
    original=engine.read_tga_history
    try:
        with sqlite3.connect(db_path) as c:
            # Replace sparse old derived rows, never preserve a stale one-point priority.
            c.execute('DELETE FROM derived_signals_ts')
            for day in sorted(all_dates):
                current=[]
                for m,rows,points in selected:
                    if day not in points:continue
                    i=index[m.id]
                    while i<len(rows) and rows[i][0]<day:i+=1
                    index[m.id]=i
                    prev=rows[i-1] if i else (None,None)
                    current.append(replace(m,as_of=day,value=points[day],previous_as_of=prev[0],previous=prev[1],change=points[day]-prev[1] if prev[1] is not None else None,extra={'history':[]}))
                # Pure historical values, with no access to today's fiscal cache.
                engine.read_tga_history=lambda *a: []
                computed,_,_=engine.derive_signals(current)
                for s in computed:
                    if s.id in {'SOFR_ANCHOR','SOFR_VOLUME_IMPACT'} and not any(m.id=='IORB' for m in current):continue
                    if s.value is None or s.as_of!=day:continue
                    p=previous.get(s.id); ch=s.value-p if p is not None else None
                    c.execute('INSERT INTO derived_signals_ts(signal_id,signal_name,as_of,value,previous,change,unit,severity,snapshot_file,ingested_at) VALUES(?,?,?,?,?,?,?,?,?,?)',(s.id,s.name,day,s.value,p,ch,s.unit,'','history_rebuild',datetime.now().isoformat()))
                    previous[s.id]=s.value;counts[s.id]=counts.get(s.id,0)+1;first.setdefault(s.id,day);last[s.id]=day
    finally:engine.read_tga_history=original
    for s in signals:report.append({'kind':'derived','id':s.id,'observations':counts.get(s.id,0),'first':first.get(s.id),'last':last.get(s.id),'status':'history_available' if counts.get(s.id,0)>1 else 'missing_history','note':'按共同观测日期计算；依赖缺失不补零、不用当前值回填。'})
    jpy=OUTPUT_DIR/'latest/jpy_carry_history.json'
    if jpy.exists():
        for mid,rows in json.loads(jpy.read_text(encoding='utf-8')).get('jpy_carry',{}).get('history',{}).items():
            valid=sorted({r['date'] for r in rows if isinstance(r,dict) and r.get('date') and isinstance(r.get('value'),(int,float))})
            report.append({'kind':'jpy','id':mid,'source':'JPY captured sources; see payload provenance','observations':len(valid),'first':valid[0] if valid else None,'last':valid[-1] if valid else None,'status':'history_available' if len(valid)>1 else 'missing_history'})
    with sqlite3.connect(db_path) as c:
        for mid,n,start,end in c.execute('SELECT series_id,COUNT(*),MIN(as_of),MAX(as_of) FROM jpy_carry_series_ts WHERE value IS NOT NULL GROUP BY series_id'):
            report=[r for r in report if not(r['kind']=='jpy' and r['id']==mid)]
            report.append({'kind':'jpy','id':mid,'source':'JPY captured database; source provenance in payload','observations':n,'first':start,'last':end,'status':'history_available' if n>1 else 'missing_history'})
    result={'scope':'全部本次canonical指标及全部派生信号；向官方源回抓可用历史，逐项列出缺口，不保证源端不存在未发布/停更资料。','series':report,'missing':[r['id'] for r in report if r['status']=='missing_history'],'treasury_failures':sorted(set(e for r in report for e in r.get('source_failures',[])))}
    OUTPUT_DIR.mkdir(exist_ok=True,parents=True)
    (OUTPUT_DIR/'history_coverage.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'[history] {len(report)} series audited; {len(result["missing"])} gaps',flush=True)
    return result
