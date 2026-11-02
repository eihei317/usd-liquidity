"""Source-specific rolling refreshes; full source history remains in every snapshot."""
import json
import math
import os
import threading
from datetime import date, timedelta
from pathlib import Path
from .utils import ROOT

CACHE = ROOT / '.workbuddy/cache/source_history'
_seed_lock = threading.Lock()
_seeds = None
OVERLAP_DAYS = 400
FULL_REFRESH_DAYS = 30

def _seed(key):
    global _seeds
    with _seed_lock:
        if _seeds is None:
            try:
                payload = json.loads((ROOT/'output/latest/snapshot.json').read_text(encoding='utf-8'))
                _seeds = {('fred:'+m['id']): dict(m, _capture_date=payload.get('generated_at_bjt','')[:10]) for m in payload['metrics'] if m.get('source', '').startswith('FRED') and m.get('status') == 'ok'}
            except (OSError, ValueError, KeyError):
                _seeds = {}
        return _seeds.get(key)

def _valid(rows):
    return (isinstance(rows, list) and len(rows) > 1 and
            all(isinstance(r, dict) and isinstance(r.get('date'), str) and
                isinstance(r.get('value'), (int, float)) and math.isfinite(r['value']) for r in rows))

def prepare(key, source, unit, full_start='1900-01-01'):
    """Only FRED caches of identical provenance/units can seed an incremental fetch."""
    path = CACHE/(key.replace(':', '_')+'.json')
    today = date.today()
    cached = None
    try:
        cached = json.loads(path.read_text(encoding='utf-8'))
        if cached['source'] != source or cached['unit'] != unit or not _valid(cached['rows']):
            cached = None
    except (OSError, ValueError, KeyError, TypeError):
        cached = None
    if cached is None:
        seed = _seed(key)
        if seed and seed.get('source') == source and seed.get('unit') == unit and _valid(seed.get('extra', {}).get('history')):
            cached = {'source': source, 'unit': unit, 'rows': seed['extra']['history'],
                      'full_refresh': str(seed.get('extra', {}).get('full_history_refresh') or seed.get('extra', {}).get('captured_at') or '')[:10]}
            # Legacy snapshots were full captures; never reset age on incremental runs.
            if not cached['full_refresh']:
                cached['full_refresh']=seed.get('_capture_date','')
    incremental = False
    if cached and os.environ.get('LIQUIDITY_FULL_HISTORY') != '1':
        try:
            age=(today-date.fromisoformat(cached['full_refresh'])).days
            incremental = 0 <= age < FULL_REFRESH_DAYS
        except (ValueError, KeyError, TypeError):
            pass
    start = max(full_start, (date.fromisoformat(max(r['date'] for r in cached['rows']))-timedelta(days=OVERLAP_DAYS)).isoformat()) if incremental else full_start
    return {'path': path, 'source': source, 'unit': unit, 'cached': cached,
            'start': start, 'incremental': incremental, 'today': today.isoformat()}

def finish(plan, rows):
    """A failed/truncated response never becomes a successful stale-cache fallback."""
    if not rows:
        raise ValueError('Empty source response; historical cache cannot substitute for a fetch')
    fresh = dict(rows)
    if not all(isinstance(v,(int,float)) and math.isfinite(v) for v in fresh.values()):
        raise ValueError('Non-finite source history')
    cached = plan['cached']
    if plan['incremental']:
        old = {r['date']:r['value'] for r in cached['rows']}
        if max(fresh) < max(old):
            raise ValueError('Source response regressed behind captured history')
        expected = [d for d in old if d >= plan['start']]
        if expected and (date.fromisoformat(min(fresh))-date.fromisoformat(min(expected))).days > 90:
            raise ValueError('Source response omitted the requested historical interval')
        # The refreshed interval is authoritative, including missing/retracted observations.
        merged = {d:v for d,v in old.items() if d < plan['start']}
        merged.update(fresh)
    else:
        merged=fresh
    ordered=sorted(merged.items())
    full_refresh=cached['full_refresh'] if plan['incremental'] else plan['today']
    payload={'source':plan['source'], 'unit':plan['unit'], 'full_refresh':full_refresh,
             'rows':[{'date':d,'value':v} for d,v in ordered]}
    plan['path'].parent.mkdir(parents=True,exist_ok=True)
    temp=plan['path'].with_suffix('.tmp')
    temp.write_text(json.dumps(payload,ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    temp.replace(plan['path'])
    return ordered, {'history_fetch_mode':'incremental' if plan['incremental'] else 'full',
                     'history_refresh_start':plan['start'], 'full_history_refresh':full_refresh}
