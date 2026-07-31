#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
美元流动性观测系统 · Agent 0-1 构建评测 · 产物自动检查器
==================================================================
对每个被测 Agent 的产物目录做机判初筛，输出可读报告 + JSON。

设计原则：不干涉交付物。检查器按扩展名与启发式发现产物，
不要求固定文件名（不再硬性要求 liquidity_data.csv / index.html）。

检查项（详见 EVAL_RULES.md）：
  C-file    交付文件齐全（至少一份数据表 + 一个看板 + 一份源码）
  C-fresh   数据表最新日期新鲜（距今天 <= FRESH_MAX_DAYS，非未来）
  C-span    回抓历史跨度足够（默认 >= MIN_SPAN_DAYS，约一个月）
  C-dedup   数据表按日期无重复行（落表去重）
  C-fake    编造信号检测（整列全0 / placeholder / 非数值 / 未来日期）
  C-html    HTML 可解析、含图表容器与更新字样
  C-csv     含 date 列 + >=2 数值列、按日期升序
  C-key     源码读取 FRED_API_KEY 环境变量且无硬编码 key
  C-live    （可选，无需 key）重抓 SOFR 与数据表最新值比对一致性

用法：
  python score.py <产物目录> [--live] [--json out.json]
退出码：所有必过项通过=0，否则=1
"""
import argparse
import csv
import glob
import json
import os
import re
import sys
from datetime import datetime, date

MIN_SPAN_DAYS = 30       # 回抓历史最低跨度（约一个月，视情况可调整）
FRESH_MAX_DAYS = 14      # 数据新鲜度容忍窗口

DATE_FORMATS = ["%Y-%m-%d", "%Y/%m/%d", "%m/%d/%Y", "%d-%m-%Y", "%Y-%m-%d %H:%M:%S"]


def find_col(header, patterns):
    for i, h in enumerate(header):
        hl = h.lower().strip()
        for p in patterns:
            if p in hl:
                return i
    return None


def parse_date(s):
    s = s.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def load_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = [r for r in csv.reader(f) if any(c.strip() for c in r)]
    if not rows:
        return None, []
    return rows[0], rows[1:]


def is_number(x):
    try:
        float(x)
        return True
    except (ValueError, TypeError):
        return False


def discover(directory):
    csv_files = sorted(glob.glob(os.path.join(directory, "*.csv")))
    html_files = sorted(glob.glob(os.path.join(directory, "*.html")))
    py_files = sorted(glob.glob(os.path.join(directory, "*.py")))
    readme = sorted(glob.glob(os.path.join(directory, "README*")))
    return csv_files, html_files, py_files, readme


def pick_main_csv(csv_files):
    """选含 date 列且数值列最多的 csv 作为主数据表。"""
    best, best_score, best_data = None, -1, ([], [])
    for p in csv_files:
        h, data = load_csv(p)
        if h is None:
            continue
        di = find_col(h, ["date", "日期"])
        if di is None:
            continue
        num = sum(1 for i, _ in enumerate(h)
                  if i != di and any(is_number(r[i]) for r in data if i < len(r)))
        if num > best_score:
            best_score, best, best_data = num, p, (h, data)
    return best, best_data


def check_dir(directory):
    results = []
    gates = []

    def add(name, passed, detail, gate=False):
        results.append({"check": name, "pass": bool(passed), "detail": detail})
        if gate:
            gates.append(bool(passed))
        return passed

    csv_files, html_files, py_files, readme = discover(directory)

    # ---- C-file：不要求固定文件名，按存在性判断 ----
    has_csv = len(csv_files) > 0
    has_html = len(html_files) > 0
    has_src = len(py_files) > 0
    missing = []
    if not has_csv:
        missing.append("数据表(csv)")
    if not has_html:
        missing.append("看板(html)")
    if not has_src:
        missing.append("源码(py)")
    add("C-file", has_csv and has_html and has_src,
        "齐全" if not missing else f"缺失: {missing}", gate=True)

    # ---- 选取主数据表 ----
    csv_path, (header, data) = pick_main_csv(csv_files)
    if csv_path is None and csv_files:
        header, data = load_csv(csv_files[0])

    dates = []
    if header is not None:
        date_i = find_col(header, ["date", "日期"])
        numeric_cols = 0
        for i, h in enumerate(header):
            if i == date_i:
                continue
            if any(is_number(r[i]) for r in data if i < len(r)):
                numeric_cols += 1
        sorted_ok = True
        seen = set()
        dup = False
        for r in data:
            if date_i is None or date_i >= len(r):
                continue
            d = parse_date(r[date_i])
            if d:
                dates.append(d)
                if d in seen:
                    dup = True
                seen.add(d)
        if len(dates) >= 2:
            sorted_ok = all(dates[i] <= dates[i + 1] for i in range(len(dates) - 1))
        span = (max(dates) - min(dates)).days if len(dates) >= 2 else -1

        add("C-csv",
            date_i is not None and numeric_cols >= 2 and sorted_ok and not dup,
            f"date列={'有' if date_i is not None else '无'}; 数值列={numeric_cols}; "
            f"升序={'是' if sorted_ok else '否'}; 历史跨度={span}天")
        add("C-dedup", not dup,
            "无重复日期行" if not dup else "存在重复日期行（落表未去重）", gate=True)
        add("C-span", span >= MIN_SPAN_DAYS,
            f"历史跨度 {span} 天（要求>={MIN_SPAN_DAYS}）")
    else:
        add("C-csv", False, "数据表缺失或为空", gate=True)
        add("C-dedup", False, "无数据", gate=True)
        add("C-span", False, "无数据")

    # ---- C-fresh 新鲜度 ----
    latest_d = max(dates) if dates else None
    today = date.today()
    if latest_d:
        delta = (today - latest_d).days
        fresh = 0 <= delta <= FRESH_MAX_DAYS
        add("C-fresh", fresh,
            f"最新日期 {latest_d.isoformat()}，距今天 {delta} 天" +
            ("（未来日期！）" if delta < 0 else ""), gate=True)
    else:
        add("C-fresh", False, "无有效日期", gate=True)

    # ---- C-fake 编造信号 ----
    if header is not None and data:
        fake = []
        for i, h in enumerate(header):
            if i == date_i:
                continue
            vals = [float(r[i]) for r in data if i < len(r) and is_number(r[i])]
            if vals and all(v == 0 for v in vals):
                fake.append(f"{h} 整列全0（疑似占位）")
        raw = " ".join(" ".join(r) for r in data).lower()
        for tok in ["placeholder", "todo", "示例", "xxx", "test data", "fake"]:
            if tok in raw:
                fake.append(f"发现占位词 '{tok}'")
        add("C-fake", len(fake) == 0,
            "无编造信号" if not fake else "; ".join(fake[:4]), gate=True)
    else:
        add("C-fake", False, "无数据可判", gate=True)

    # ---- C-html ----
    html_ok = False
    html_detail = "未找到 html"
    for hp in html_files:
        txt = open(hp, encoding="utf-8", errors="ignore").read()
        has_canvas = ("<canvas" in txt.lower()) or ("chart" in txt.lower())
        has_update = bool(re.search(r"as of|最后更新|updated|截至|数据截至|更新时间", txt, re.I))
        if len(txt) > 500 and has_canvas and has_update:
            html_ok, html_detail = True, f"{os.path.basename(hp)} 大小 {len(txt)}B; 图表容器有; 更新字样有"
            break
        html_detail = f"{os.path.basename(hp)} 大小 {len(txt)}B; 图表容器={'有' if has_canvas else '无'}; 更新字样={'有' if has_update else '无'}"
    add("C-html", html_ok, html_detail)

    # ---- C-key ----
    reads_env = False
    hardcoded = False
    for pf in py_files:
        src = open(pf, encoding="utf-8", errors="ignore").read()
        if re.search(r"os\.(environ|getenv).*FRED_API_KEY|FRED_API_KEY.*os\.(environ|getenv)", src):
            reads_env = True
        if re.search(r"['\"][0-9a-fA-F]{32}['\"]", src):
            hardcoded = True
    add("C-key", (reads_env or not py_files) and not hardcoded,
        f"读取环境变量={'是' if reads_env else '否/无需'}; 硬编码key={'有(违规)' if hardcoded else '无'}")
    if readme:
        add("C-readme", True, f"发现 {os.path.basename(readme[0])}")
    else:
        add("C-readme", False, "未见运行说明文件（建议补充）")

    return results, gates


def live_crosscheck(directory):
    """无需 key 重抓 SOFR 与数据表最新值比对（可选 --live）。"""
    import urllib.request
    csv_files, _, _, _ = discover(directory)
    main, (header, data) = pick_main_csv(csv_files)
    if main is None or header is None:
        return None
    sofr_i = find_col(header, ["sofr"])
    if sofr_i is None or not data:
        return {"skipped": "数据表无 sofr 列（Agent 自选指标，跳过）"}
    try:
        last = float(data[-1][sofr_i])
    except (ValueError, IndexError):
        return None
    try:
        url = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=SOFR"
        req = urllib.request.Request(url, headers={"User-Agent": "eval-checker/1.0"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            remote = resp.read().decode().strip().splitlines()
        rlast = float(remote[-1].split(",")[1])
        ok = abs(rlast - last) / max(abs(rlast), 1e-9) <= 0.005
        return {"live_sofr_remote": rlast, "csv_sofr": last, "match": ok}
    except Exception as e:
        return {"error": str(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("directory", help="模型产物目录")
    ap.add_argument("--live", action="store_true", help="开启 SOFR 实时交叉校验（无需 key）")
    ap.add_argument("--json", help="将报告写入该 JSON 路径")
    args = ap.parse_args()

    if not os.path.isdir(args.directory):
        print(f"[ERROR] 目录不存在: {args.directory}")
        sys.exit(2)

    results, gates = check_dir(args.directory)
    live = live_crosscheck(args.directory) if args.live else None

    print("=" * 60)
    print(f"产物检查：{args.directory}")
    print("=" * 60)
    for r in results:
        mark = "PASS" if r["pass"] else "FAIL"
        print(f"[{mark}] {r['check']:<8} {r['detail']}")
    if live is not None:
        print(f"[LIVE] SOFR 重抓校验: {json.dumps(live, ensure_ascii=False)}")
    all_pass = all(gates)
    print("-" * 60)
    print(f"必过门槛（C-file/C-fresh/C-fake/C-dedup）: {'全部通过 ✅' if all_pass else '存在失败 ❌'}")
    print(f"RUN STATUS: {'SUCCESS-POSSIBLE' if all_pass else 'FAIL/GATE-BLOCKED'}")
    print("=" * 60)

    report = {"directory": args.directory, "checks": results, "gates_all_pass": all_pass, "live": live}
    if args.json:
        with open(args.json, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"报告已写入 {args.json}")

    sys.exit(0 if all_pass else 1)


if __name__ == "__main__":
    main()
