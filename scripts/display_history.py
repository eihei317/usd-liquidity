"""Repair an uncited display-only history in a new run without changing frozen model facts."""
import json,sqlite3
from contextlib import closing
from datetime import datetime
def fill(work,latest,package):
    db=work/'output/usd_liquidity.db'
    with closing(sqlite3.connect(db)) as c:
        first=c.execute("SELECT MIN(as_of) FROM metrics_ts WHERE metric_id='IORB' AND value IS NOT NULL").fetchone()[0]
        if first:
            c.execute("DELETE FROM derived_signals_ts WHERE signal_id IN ('SOFR_ANCHOR','SOFR_VOLUME_IMPACT') AND as_of < ?",(first,))
        if c.execute("SELECT COUNT(*) FROM jpy_carry_series_ts WHERE series_id='JGB5'").fetchone()[0]<=1:
            from scripts.analysis_validator import _collect_facts
            if 'jpy:JGB5' in _collect_facts(package)[0]:raise RuntimeError('JGB5 is a model input; require a new analysis')
            from scripts.jpy_carry import fetch_mof_jgb
            series,meta=fetch_mof_jgb();cut=package['generated_at_bjt'][:10]
            rows=[(d,v) for d,v in series['JGB5'] if d<=cut]
            if len(rows)<2:raise RuntimeError('Official JGB5 history remains incomplete')
            for d,v in rows:
                c.execute("INSERT INTO jpy_carry_series_ts(series_id,as_of,value,unit,source,source_url,snapshot_file,ingested_at) VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(series_id,as_of) DO UPDATE SET value=excluded.value,source=excluded.source,source_url=excluded.source_url",('JGB5',d,v,'%','MOF',meta['source_url'],'official_display_history',datetime.now().isoformat()))
        n,start,end=c.execute("SELECT COUNT(*),MIN(as_of),MAX(as_of) FROM jpy_carry_series_ts WHERE series_id='JGB5'").fetchone()
        corrected={sid:c.execute('SELECT COUNT(*),MIN(as_of),MAX(as_of) FROM derived_signals_ts WHERE signal_id=?',(sid,)).fetchone() for sid in ('SOFR_ANCHOR','SOFR_VOLUME_IMPACT')}
        c.commit()
    coverage_path=work/'output/history_coverage.json'
    coverage=json.loads(coverage_path.read_text(encoding='utf-8'))
    for row in coverage['series']:
        if row['kind']=='jpy' and row['id']=='JGB5':row.update(observations=n,first=start,last=end,status='history_available',source='MOF official historical CSV + actual latest quote')
    for row in coverage['series']:
        if row['kind']=='derived' and row['id'] in corrected:
            size,begin,finish=corrected[row['id']];row.update(observations=size,first=begin,last=finish,note='仅使用同日IORB实际存在后的利差，不混入早期目标上限代理。')
    context_path=latest/'investment_market_context.json'
    if context_path.exists() and not any(r['kind']=='market' for r in coverage['series']):
        from scripts.investment_facts import build_market_context
        old=json.loads(context_path.read_text(encoding='utf-8'))
        fetched=build_market_context(package['generated_at_bjt'],fetch=True,previous_context=old)
        for sid,prior in old.get('price_history',{}).items():
            earliest=min((p['date'] for p in prior),default='9999-12-31')
            earlier=[p for p in fetched.get('price_history',{}).get(sid,[]) if p['date']<earliest]
            merged=earlier+prior
            old['price_history'][sid]=merged
            coverage['series'].append({'kind':'market','id':sid,'source':'FRED public source history','observations':len(merged),'first':merged[0]['date'] if merged else None,'last':merged[-1]['date'] if merged else None,'status':'history_available' if len(merged)>1 else 'missing_history'})
        # Preserve every original recent quote: frozen model facts are unchanged.
        context_path.write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf-8')
    coverage['missing']=[r['id'] for r in coverage['series'] if r['status']=='missing_history']
    coverage_path.write_text(json.dumps(coverage,ensure_ascii=False,indent=2),encoding='utf-8')
    p=latest/'dashboard_data.json';dashboard=json.loads(p.read_text(encoding='utf-8'));dashboard['history_coverage']=coverage;p.write_text(json.dumps(dashboard,ensure_ascii=False,indent=2),encoding='utf-8')
