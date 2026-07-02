"""SQLite database initialization and snapshot ingestion (merged from init_liquidity_db.py + ingest_snapshot.py)."""

from __future__ import annotations

import json
import os
import sqlite3
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .utils import BJT, ROOT

DB_PATH = ROOT / "output" / "usd_liquidity.db"


# Canonical table definitions. The `create` statement must match the schema the
# rest of the code expects. `unique` is the exact ordered column list of the
# UNIQUE/PRIMARY-KEY constraint the upsert statements target with ON CONFLICT.
TABLE_DEFS = [
    {
        'name': 'metrics_ts',
        'unique': ['metric_id', 'as_of'],
        'columns': ['metric_id', 'metric_name', 'category', 'as_of', 'value',
                    'previous', 'change', 'unit', 'frequency', 'source',
                    'source_url', 'status', 'stale_days', 'snapshot_file',
                    'ingested_at'],
        'create': '''CREATE TABLE IF NOT EXISTS metrics_ts (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_id       TEXT    NOT NULL,
            metric_name     TEXT,
            category        TEXT,
            as_of           TEXT    NOT NULL,
            value           REAL,
            previous        REAL,
            change          REAL,
            unit            TEXT,
            frequency       TEXT,
            source          TEXT,
            source_url      TEXT,
            status          TEXT,
            stale_days      INTEGER,
            snapshot_file   TEXT,
            ingested_at     TEXT    NOT NULL,
            UNIQUE(metric_id, as_of)
        )''',
    },
    {
        'name': 'derived_signals_ts',
        'unique': ['signal_id', 'as_of'],
        'columns': ['signal_id', 'signal_name', 'as_of', 'value', 'previous',
                    'change', 'unit', 'severity', 'snapshot_file', 'ingested_at'],
        'create': '''CREATE TABLE IF NOT EXISTS derived_signals_ts (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            signal_id         TEXT    NOT NULL,
            signal_name       TEXT,
            as_of             TEXT    NOT NULL,
            value             REAL,
            previous          REAL,
            change            REAL,
            unit              TEXT,
            severity          TEXT,
            snapshot_file     TEXT,
            ingested_at       TEXT    NOT NULL,
            UNIQUE(signal_id, as_of)
        )''',
    },
    {
        'name': 'snapshots',
        'unique': ['snapshot_file'],
        'columns': ['run_at', 'snapshot_file', 'data_as_of', 'rrP_balance',
                    'tga_balance', 'sofr', 'effr', 'vix', 'real_10y', 'note'],
        'create': '''CREATE TABLE IF NOT EXISTS snapshots (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            run_at            TEXT    NOT NULL,
            snapshot_file     TEXT,
            model_input_file  TEXT,
            data_as_of        TEXT,
            rrP_balance      REAL,
            tga_balance      REAL,
            sofr              REAL,
            effr              REAL,
            vix               REAL,
            real_10y          REAL,
            note              TEXT,
            UNIQUE(snapshot_file)
        )''',
    },
    {
        'name': 'treasury_auctions_ts',
        'unique': ['snapshot_file', 'auction_date', 'cusip', 'security_type', 'security_term'],
        'columns': ['snapshot_file', 'ingested_at', 'calendar_as_of', 'auction_date',
                    'issue_date', 'announcement_date', 'security_type', 'security_term',
                    'offering_amount_bn', 'offering_amount_text', 'cusip', 'is_bill',
                    'is_note_or_bond', 'source_url', 'status', 'raw_json'],
        'create': '''CREATE TABLE IF NOT EXISTS treasury_auctions_ts (
            id                    INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_file         TEXT    NOT NULL,
            ingested_at           TEXT    NOT NULL,
            calendar_as_of        TEXT,
            auction_date          TEXT    NOT NULL,
            issue_date            TEXT,
            announcement_date     TEXT,
            security_type         TEXT,
            security_term         TEXT,
            offering_amount_bn    REAL,
            offering_amount_text  TEXT,
            cusip                 TEXT,
            is_bill               INTEGER,
            is_note_or_bond       INTEGER,
            source_url            TEXT,
            status                TEXT,
            raw_json              TEXT,
            UNIQUE(snapshot_file, auction_date, cusip, security_type, security_term)
        )''',
    },
    {
        'name': 'treasury_bill_supply_schedule_ts',
        'unique': ['snapshot_file', 'auction_date'],
        'columns': ['snapshot_file', 'ingested_at', 'calendar_as_of', 'auction_date',
                    'total_bill_offering_bn', 'item_count', 'terms', 'source_url'],
        'create': '''CREATE TABLE IF NOT EXISTS treasury_bill_supply_schedule_ts (
            id                    INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_file         TEXT    NOT NULL,
            ingested_at           TEXT    NOT NULL,
            calendar_as_of        TEXT,
            auction_date          TEXT    NOT NULL,
            total_bill_offering_bn REAL,
            item_count            INTEGER,
            terms                 TEXT,
            source_url            TEXT,
            UNIQUE(snapshot_file, auction_date)
        )''',
    },
    {
        'name': 'engineered_series_ts',
        'unique': ['series_id', 'as_of'],
        'columns': ['series_id', 'series_name', 'category', 'as_of', 'value',
                    'unit', 'source', 'source_url', 'snapshot_file', 'ingested_at',
                    'notes'],
        'create': '''CREATE TABLE IF NOT EXISTS engineered_series_ts (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id       TEXT    NOT NULL,
            series_name     TEXT,
            category        TEXT,
            as_of           TEXT    NOT NULL,
            value           REAL,
            unit            TEXT,
            source          TEXT,
            source_url      TEXT,
            snapshot_file   TEXT    NOT NULL,
            ingested_at     TEXT    NOT NULL,
            notes           TEXT,
            UNIQUE(series_id, as_of)
        )''',
    },
    {
        'name': 'jpy_carry_series_ts',
        'unique': ['series_id', 'as_of'],
        'columns': ['series_id', 'series_name', 'category', 'as_of', 'value',
                    'unit', 'source', 'source_url', 'snapshot_file', 'ingested_at',
                    'notes'],
        'create': '''CREATE TABLE IF NOT EXISTS jpy_carry_series_ts (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            series_id       TEXT    NOT NULL,
            series_name     TEXT,
            category        TEXT,
            as_of           TEXT    NOT NULL,
            value           REAL,
            unit            TEXT,
            source          TEXT,
            source_url      TEXT,
            snapshot_file   TEXT    NOT NULL,
            ingested_at     TEXT    NOT NULL,
            notes           TEXT,
            UNIQUE(series_id, as_of)
        )''',
    },
]


def _table_unique_cols(conn: sqlite3.Connection, name: str):
    """Return the column list of the table's unique/primary-key index, else []."""
    cur = conn.cursor()
    for r in cur.execute(f"PRAGMA index_list('{name}')"):
        # PRAGMA index_list rows: (seq, name, unique, origin, partial)
        if len(r) >= 3 and r[2]:
            idx = r[1]
            cols = [row[2] for row in cur.execute(f"PRAGMA index_info('{idx}')")]
            return cols
    return []


def _rebuild_table_preserve(conn: sqlite3.Connection, d: dict):
    """Recreate a table with the canonical schema, preserving existing rows
    (de-duplicated to the unique key, keeping the latest ingested row)."""
    name = d['name']
    cur = conn.cursor()
    tmp = '_old_' + name
    cur.execute(f'DROP TABLE IF EXISTS "{tmp}"')
    cur.execute(f'ALTER TABLE "{name}" RENAME TO "{tmp}"')
    cur.execute(d['create'])
    cols = d['columns']
    col_list = ', '.join(f'"{c}"' for c in cols)
    unique_list = ', '.join(f'"{c}"' for c in d['unique'])
    order_col = 'ingested_at' if 'ingested_at' in cols else d['unique'][0]
    sel = (
        f'SELECT {col_list} FROM ('
        f'  SELECT {col_list},'
        f'    ROW_NUMBER() OVER (PARTITION BY {unique_list} ORDER BY "{order_col}" DESC) rn'
        f'  FROM "{tmp}"'
        f') WHERE rn = 1'
    )
    cur.execute(f'INSERT INTO "{name}" ({col_list}) {sel}')
    cur.execute(f'DROP TABLE "{tmp}"')


def _ensure_table(conn: sqlite3.Connection, d: dict):
    name = d['name']
    cur = conn.cursor()
    exists = cur.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (name,)
    ).fetchone()
    if not exists:
        cur.execute(d['create'])
        return
    if _table_unique_cols(conn, name) == d['unique']:
        return
    # Schema mismatch on the unique constraint -> rebuild preserving history.
    _rebuild_table_preserve(conn, d)


def _heal_schema(conn: sqlite3.Connection):
    """Make sure every table matches TABLE_DEFS, rebuilding any that drifted
    (e.g. an older CREATE TABLE IF NOT EXISTS left a stale UNIQUE constraint)."""
    for d in TABLE_DEFS:
        _ensure_table(conn, d)


def init_db(db_path: Optional[str] = None) -> str:
    db_path = db_path or str(DB_PATH)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    _heal_schema(conn)

    c.execute('''
    CREATE TABLE IF NOT EXISTS metrics_ts (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        metric_id       TEXT    NOT NULL,
        metric_name     TEXT,
        category        TEXT,
        as_of           TEXT    NOT NULL,
        value           REAL,
        previous        REAL,
        change          REAL,
        unit            TEXT,
        frequency       TEXT,
        source          TEXT,
        source_url      TEXT,
        status          TEXT,
        stale_days      INTEGER,
        snapshot_file   TEXT,
        ingested_at     TEXT    NOT NULL,
        UNIQUE(metric_id, as_of)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS derived_signals_ts (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        signal_id         TEXT    NOT NULL,
        signal_name       TEXT,
        as_of             TEXT    NOT NULL,
        value             REAL,
        previous          REAL,
        change            REAL,
        unit              TEXT,
        severity          TEXT,
        snapshot_file     TEXT,
        ingested_at       TEXT    NOT NULL,
        UNIQUE(signal_id, as_of)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS snapshots (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        run_at            TEXT    NOT NULL,
        snapshot_file     TEXT,
        model_input_file  TEXT,
        data_as_of        TEXT,
        rrP_balance      REAL,
        tga_balance      REAL,
        sofr              REAL,
        effr              REAL,
        vix               REAL,
        real_10y          REAL,
        note              TEXT,
        UNIQUE(snapshot_file)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS treasury_auctions_ts (
        id                    INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_file         TEXT    NOT NULL,
        ingested_at           TEXT    NOT NULL,
        calendar_as_of        TEXT,
        auction_date          TEXT    NOT NULL,
        issue_date            TEXT,
        announcement_date     TEXT,
        security_type         TEXT,
        security_term         TEXT,
        offering_amount_bn    REAL,
        offering_amount_text  TEXT,
        cusip                 TEXT,
        is_bill               INTEGER,
        is_note_or_bond       INTEGER,
        source_url            TEXT,
        status                TEXT,
        raw_json              TEXT,
        UNIQUE(snapshot_file, auction_date, cusip, security_type, security_term)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS treasury_bill_supply_schedule_ts (
        id                    INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_file         TEXT    NOT NULL,
        ingested_at           TEXT    NOT NULL,
        calendar_as_of        TEXT,
        auction_date          TEXT    NOT NULL,
        total_bill_offering_bn REAL,
        item_count            INTEGER,
        terms                 TEXT,
        source_url            TEXT,
        UNIQUE(snapshot_file, auction_date)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS engineered_series_ts (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        series_id       TEXT    NOT NULL,
        series_name     TEXT,
        category        TEXT,
        as_of           TEXT    NOT NULL,
        value           REAL,
        unit            TEXT,
        source          TEXT,
        source_url      TEXT,
        snapshot_file   TEXT    NOT NULL,
        ingested_at     TEXT    NOT NULL,
        notes           TEXT,
        UNIQUE(series_id, as_of)
    )
    ''')

    c.execute('''
    CREATE TABLE IF NOT EXISTS jpy_carry_series_ts (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        series_id       TEXT    NOT NULL,
        series_name     TEXT,
        category        TEXT,
        as_of           TEXT    NOT NULL,
        value           REAL,
        unit            TEXT,
        source          TEXT,
        source_url      TEXT,
        snapshot_file   TEXT    NOT NULL,
        ingested_at     TEXT    NOT NULL,
        notes           TEXT,
        UNIQUE(series_id, as_of)
    )
    ''')

    c.execute('CREATE INDEX IF NOT EXISTS idx_metrics_id_date ON metrics_ts(metric_id, as_of)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_derived_id_date ON derived_signals_ts(signal_id, as_of)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_snapshots_run_at ON snapshots(run_at)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_auctions_date ON treasury_auctions_ts(auction_date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_bill_supply_date ON treasury_bill_supply_schedule_ts(auction_date)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_engineered_series_id_date ON engineered_series_ts(series_id, as_of)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_jpy_series_id_date ON jpy_carry_series_ts(series_id, as_of)')

    conn.commit()
    conn.close()
    return db_path


def get_db(db_path: Optional[str] = None) -> sqlite3.Connection:
    db_path = db_path or str(DB_PATH)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)


def ingest_snapshot(snapshot_path: str, db_conn: Optional[sqlite3.Connection] = None) -> Tuple[int, int]:
    """Ingest a snapshot JSON file into the SQLite database. Returns (metrics_inserted, signals_inserted)."""
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
        metric_id = m.get('id', '')
        metric_name = m.get('name', '')
        category = m.get('category', '')
        as_of = m.get('as_of', '')
        value = m.get('value', None)
        previous = m.get('previous', None)
        change = m.get('change', None)
        unit = m.get('unit', '')
        frequency = m.get('frequency', '')
        source = m.get('source', '')
        source_url = m.get('source_url', '')
        status = m.get('status', '')
        stale_days = m.get('stale_days', None)

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
                ON CONFLICT(metric_id, as_of) DO UPDATE SET
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

    derived = snap.get('derived_signals', [])
    inserted_d = 0
    skipped_d = 0
    for d in derived:
        signal_id = d.get('id', '')
        signal_name = d.get('name', '')
        as_of = d.get('as_of', '') or snap.get('generated_at_bjt', '')[:10]
        value = d.get('value', None)
        previous = d.get('previous', None)
        change = d.get('change', None)
        unit = d.get('unit', '')
        severity = d.get('severity', '')

        if not signal_id:
            skipped_d += 1
            continue

        try:
            c.execute(
                '''INSERT INTO derived_signals_ts
                    (signal_id, signal_name, as_of, value, previous, change,
                     unit, severity, snapshot_file, ingested_at)
                VALUES (?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(signal_id, as_of) DO UPDATE SET
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

    upcoming = snap.get('upcoming_auctions') or {}
    inserted_a = 0
    inserted_bs = 0
    if isinstance(upcoming, dict) and upcoming.get('status') == 'ok':
        calendar_as_of = upcoming.get('as_of', '')
        source_url = upcoming.get('source_url', '')
        for a in upcoming.get('auctions', []):
            if not isinstance(a, dict):
                continue
            auction_date = a.get('auctionDate') or ''
            if not auction_date:
                continue
            try:
                c.execute(
                    '''INSERT INTO treasury_auctions_ts
                        (snapshot_file, ingested_at, calendar_as_of, auction_date, issue_date,
                         announcement_date, security_type, security_term, offering_amount_bn,
                         offering_amount_text, cusip, is_bill, is_note_or_bond, source_url,
                         status, raw_json)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(snapshot_file, auction_date, cusip, security_type, security_term) DO UPDATE SET
                        ingested_at          = excluded.ingested_at,
                        calendar_as_of       = excluded.calendar_as_of,
                        issue_date           = excluded.issue_date,
                        announcement_date    = excluded.announcement_date,
                        offering_amount_bn   = excluded.offering_amount_bn,
                        offering_amount_text = excluded.offering_amount_text,
                        source_url           = excluded.source_url,
                        status               = excluded.status,
                        raw_json             = excluded.raw_json''',
                    (
                        snapshot_file, ingested_at, calendar_as_of, auction_date,
                        a.get('issueDate') or '', a.get('announcementDate') or '',
                        a.get('securityType') or '', a.get('securityTerm') or '',
                        a.get('offeringAmount'), a.get('offeringAmountText') or '',
                        a.get('cusip') or '', 1 if a.get('is_bill') else 0,
                        1 if a.get('is_note_or_bond') else 0, source_url,
                        upcoming.get('status') or '', json.dumps(a, ensure_ascii=False),
                    )
                )
                inserted_a += 1
            except Exception as e:
                print(f'  [WARN] skip auction {auction_date}: {e}')
        for day in upcoming.get('bill_schedule', []):
            if not isinstance(day, dict):
                continue
            auction_date = day.get('auctionDate') or ''
            if not auction_date:
                continue
            items = day.get('items', []) if isinstance(day.get('items'), list) else []
            terms = ', '.join(sorted({str(item.get('securityTerm') or '') for item in items if item.get('securityTerm')}))
            try:
                c.execute(
                    '''INSERT INTO treasury_bill_supply_schedule_ts
                        (snapshot_file, ingested_at, calendar_as_of, auction_date,
                         total_bill_offering_bn, item_count, terms, source_url)
                    VALUES (?,?,?,?,?,?,?,?)
                    ON CONFLICT(snapshot_file, auction_date) DO UPDATE SET
                        ingested_at            = excluded.ingested_at,
                        calendar_as_of         = excluded.calendar_as_of,
                        total_bill_offering_bn = excluded.total_bill_offering_bn,
                        item_count             = excluded.item_count,
                        terms                  = excluded.terms,
                        source_url             = excluded.source_url''',
                    (
                        snapshot_file, ingested_at, calendar_as_of, auction_date,
                        day.get('totalBillOffering'), len(items), terms, source_url,
                    )
                )
                inserted_bs += 1
            except Exception as e:
                print(f'  [WARN] skip bill schedule {auction_date}: {e}')

    try:
        data_as_of = snap.get('data_as_of', '')
        rrP = next((m['value'] for m in metrics if m['id'] == 'RRPONTSYD'), None)
        tga = next((m['value'] for m in metrics if m['id'] == 'TGA'), None)
        sofr = next((m['value'] for m in metrics if m['id'] == 'SOFR'), None)
        effr = next((m['value'] for m in metrics if m['id'] == 'EFFR'), None)
        vix = next((m['value'] for m in metrics if m['id'] == 'VIXCLS'), None)
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
    print(f'[ingest] upcoming_auctions: {inserted_a} details, {inserted_bs} bill-day aggregates')
    print(f'[ingest] snapshot recorded: {snapshot_file}')
    return inserted_m, inserted_d
