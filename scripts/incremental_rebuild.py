"""Find the earliest changed observation; re-evaluate its entire derived suffix."""
import hashlib
import json
import os
from pathlib import Path

def plan_rebuild(selected, signals, state_path):
    signatures=[]
    daily={}
    for metric,rows,_ in selected:
        signatures.append((metric.id,metric.source,metric.unit,metric.frequency))
        for day,value in rows:
            daily.setdefault(day,[]).append((metric.id,value))
    fingerprints={d:hashlib.sha256(json.dumps(sorted(v),separators=(',',':')).encode()).hexdigest() for d,v in daily.items()}
    root=Path(__file__).parent
    engine=hashlib.sha256(b''.join((root/name).read_bytes() for name in ('signals.py','utils.py','history_audit.py','incremental_rebuild.py'))+json.dumps(sorted(signatures)).encode()).hexdigest()
    state={'engine_sha256':engine,'observations':fingerprints}
    try:
        old=json.loads(state_path.read_text(encoding='utf-8'))
    except (OSError,ValueError):
        old={}
    full = old.get('engine_sha256') != engine or os.environ.get('LIQUIDITY_FULL_HISTORY')=='1'
    cutoff=None
    if not full:
        previous=old.get('observations',{})
        changed=[d for d in fingerprints.keys()|previous.keys() if fingerprints.get(d)!=previous.get(d)]
        # Snapshot ingestion writes current derived rows before the audit. Rebuild these
        # too, including old weekly dates, to restore strict same-date provenance.
        changed += [s.as_of for s in signals if s.as_of]
        cutoff=min(changed) if changed else None
    return state, full, cutoff

def save_state(path,state):
    temp=path.with_suffix('.tmp')
    temp.write_text(json.dumps(state,separators=(',',':')),encoding='utf-8')
    temp.replace(path)
