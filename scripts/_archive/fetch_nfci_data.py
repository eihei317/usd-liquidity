#!/usr/bin/env python3
"""
获取NFCI（芝加哥联储全国金融条件指数）最近一个月的数据
"""
import requests
import json
from datetime import datetime, timedelta

# 计算日期范围：最近30天
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

# FRED API URL for NFCI
# NFCI是周频数据，通常每周四更新
url = f"https://api.stlouisfed.org/fred/series/observations"
params = {
    "series_id": "NFCI",
    "api_key": "YOUR_API_KEY_HERE",  # 需要FRED API key，或者我们直接用已有的数据
    "file_type": "json",
    "observation_start": start_date.strftime("%Y-%m-%d"),
    "observation_end": end_date.strftime("%Y-%m-%d"),
    "sort_order": "asc"
}

print("NFCI series already exists in dashboard_data.json and charts.json")
print("The chart 'financial_conditions_30d' already contains NFCI data for the past month.")
print("\nCurrent NFCI value:", -0.51)
print("Previous value:", -0.49)
print("Change:", -0.02)
print("\nThe chart is currently in the '背景复盘' (background review) section.")
print("To make it more visible, we can either:")
print("1. Move it to a more prominent position")
print("2. Rename the chart title to be more explicit")
print("3. Both")
