#!/usr/bin/env python3
"""
初始化美元流动性历史数据库 SQLite。
表设计：
  metrics_ts  : 指标时间序列主表（每个指标每天一条）
  snapshots   : 每次运行的快照记录（便于回溯某天全量状态）
  derived_signals_ts : 衍生信号时间序列
"""
import sqlite3, os, json
from datetime import datetime, timezone, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'output', 'usd_liquidity.db')

def init_db(db_path=DB_PATH):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    # 1. 指标主表：每个指标每个 as_of 日期一条记录
    c.execute('''
    CREATE TABLE IF NOT EXISTS metrics_ts (
        id              INTEGER PRIMARY KEY AUTOINCREMENT,
        metric_id       TEXT    NOT NULL,   -- e.g. RRPONTSYD, DGS10, SOFR
        metric_name     TEXT,
        category        TEXT,
        as_of           TEXT    NOT NULL,   -- 数据日期 YYYY-MM-DD
        value           REAL,
        previous        REAL,
        change          REAL,
        unit            TEXT,
        frequency       TEXT,
        source          TEXT,
        source_url      TEXT,
        status          TEXT,
        stale_days      INTEGER,
        snapshot_file   TEXT,                -- 来源快照文件名（不含路径）
        ingested_at     TEXT    NOT NULL,     -- 入库时间 BJT
        UNIQUE(metric_id, as_of, snapshot_file)
    )
    ''')

    # 2. 衍生信号表
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
        UNIQUE(signal_id, as_of, snapshot_file)
    )
    ''')

    # 3. 快照运行记录表
    c.execute('''
    CREATE TABLE IF NOT EXISTS snapshots (
        id                INTEGER PRIMARY KEY AUTOINCREMENT,
        run_at            TEXT    NOT NULL,   -- 运行时间 BJT
        snapshot_file     TEXT,
        model_input_file  TEXT,
        data_as_of        TEXT,                -- 最新数据覆盖到的日期
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

    # 索引
    c.execute('CREATE INDEX IF NOT EXISTS idx_metrics_id_date ON metrics_ts(metric_id, as_of)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_derived_id_date ON derived_signals_ts(signal_id, as_of)')
    c.execute('CREATE INDEX IF NOT EXISTS idx_snapshots_run_at ON snapshots(run_at)')

    conn.commit()
    conn.close()
    print(f'[init] DB initialized: {db_path}')
    return db_path

if __name__ == '__main__':
    init_db()
