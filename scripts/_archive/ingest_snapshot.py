#!/usr/bin/env python3
"""
将 snapshot JSON 中的全量指标落库到 SQLite 历史数据库。
用法：python3 ingest_snapshot.py <snapshot_json_path>
"""
import sqlite3, json, os, sys
from datetime import datetime, timezone, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'output', 'usd_liquidity.db')
BJT = timezone(timedelta(hours=8))

def get_db():
    db_path = os.path.abspath(DB_PATH)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)

def ingest_snapshot(snapshot_path, db_conn=None):
    snapshot_path = os.path.abspath(snapshot_path)
    snapshot_file = os.path.basename(snapshot_path)
    ingested_at = datetime.now(BJT).strftime('%Y-%m-%d %H:%M:%S UTC+08:00')

    with open(snapshot_path, 'r', encoding='utf-8') as f:
        snap = json.load(f)

    own_conn = db_conn is None
    conn = db_conn or get_db()
    c = conn.cursor()

    metrics = snap.get('metrics', [])
    inserted_m = 0
    skipped_m = 0

    for m in metrics:
        metric_id   = m.get('id', '')
        metric_name = m.get('name', '')
        category    = m.get('category', '')
        as_of       = m.get('as_of', '')
        value       = m.get('value', None)
        previous    = m.get('previous', None)
        change      = m.get('change', None)
        unit        = m.get('unit', '')
        frequency   = m.get('frequency', '')
        source      = m.get('source', '')
        source_url  = m.get('source_url', '')
        status      = m.get('status', '')
        stale_days  = m.get('stale_days', None)

        if not as_of or not metric_id:
            skipped_m += 1
            continue

        try:
            c.execute(
                '''INSERT INTO metrics_ts
                    (metric_id, metric_name, category, as_of, value, previous, change,
                     unit, frequency, source, source_url, status, stale_days,
                     snapshot_file, ingested_at)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(metric_id, as_of, snapshot_file) DO UPDATE SET
                    value       = excluded.value,
                    previous    = excluded.previous,
                    change      = excluded.change,
                    stale_days  = excluded.stale_days,
                    ingested_at = excluded.ingested_at''',
                (metric_id, metric_name, category, as_of, value, previous, change,
                 unit, frequency, source, source_url, status, stale_days,
                 snapshot_file, ingested_at)
            )
            inserted_m += 1
        except Exception as e:
            print(f'  [WARN] skip {metric_id}@{as_of}: {e}')
            skipped_m += 1

    # 衍生信号
    derived = snap.get('derived_signals', [])
    inserted_d = 0
    skipped_d = 0
    for d in derived:
        signal_id   = d.get('id', '')
        signal_name = d.get('name', '')
        as_of       = d.get('as_of', '') or snap.get('generated_at_bjt', '')[:10]
        value       = d.get('value', None)
        previous    = d.get('previous', None)
        change      = d.get('change', None)
        unit        = d.get('unit', '')
        severity    = d.get('severity', '')

        if not signal_id:
            skipped_d += 1
            continue

        try:
            c.execute(
                '''INSERT INTO derived_signals_ts
                    (signal_id, signal_name, as_of, value, previous, change,
                     unit, severity, snapshot_file, ingested_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(signal_id, as_of, snapshot_file) DO UPDATE SET
                    value       = excluded.value,
                    previous    = excluded.previous,
                    change      = excluded.change,
                    ingested_at = excluded.ingested_at''',
                (signal_id, signal_name, as_of, value, previous, change,
                 unit, severity, snapshot_file, ingested_at)
            )
            inserted_d += 1
        except Exception as e:
            print(f'  [WARN] skip signal {signal_id}: {e}')
            skipped_d += 1

    # 快照记录
    try:
        data_as_of = snap.get('data_as_of', '')
        rrP = next((m['value'] for m in metrics if m['id'] == 'RRPONTSYD'), None)
        tga = next((m['value'] for m in metrics if m['id'] == 'TGA'), None)
        sofr = next((m['value'] for m in metrics if m['id'] == 'SOFR'), None)
        effr = next((m['value'] for m in metrics if m['id'] == 'EFFR'), None)
        vix  = next((m['value'] for m in metrics if m['id'] == 'VIXCLS'), None)
        real10y = next((m['value'] for m in metrics if m['id'] == 'DFII10'), None)

        c.execute(
            '''INSERT INTO snapshots
                (run_at, snapshot_file, data_as_of,
                 rrP_balance, tga_balance, sofr, effr, vix, real_10y)
            VALUES (?,?,?,?,?,?,?,?,?)
            ON CONFLICT(snapshot_file) DO UPDATE SET
                run_at      = excluded.run_at,
                data_as_of   = excluded.data_as_of,
                rrP_balance = excluded.rrP_balance,
                tga_balance = excluded.tga_balance,
                sofr         = excluded.sofr,
                effr         = excluded.effr,
                vix          = excluded.vix,
                real_10y     = excluded.real_10y''',
            (ingested_at, snapshot_file, data_as_of,
             rrP, tga, sofr, effr, vix, real10y)
        )
    except Exception as e:
        print(f'  [WARN] snapshot record: {e}')

    conn.commit()
    if own_conn:
        conn.close()

    print(f'[ingest] metrics: {inserted_m} inserted, {skipped_m} skipped')
    print(f'[ingest] derived_signals: {inserted_d} inserted, {skipped_d} skipped')
    print(f'[ingest] snapshot recorded: {snapshot_file}')
    return inserted_m, inserted_d


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 ingest_snapshot.py <snapshot.json>')
        sys.exit(1)
    ingest_snapshot(sys.argv[1])
