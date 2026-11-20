# -*- coding: utf-8 -*-
"""步骤5（进阶）：动态渲染网站爬取 —— 方案二：接口分析（推荐，无需浏览器）。

动态渲染页面的数据其实来自后端 JSON 接口（XHR），直接抓接口比渲染浏览器更快、更稳，
还不需要下载 200MB 的浏览器内核。这里以 quotes.toscrape.com 为例。
运行：python step5_api_analysis.py（只需 requests，已安装）
"""
import csv
import time

import requests

BASE_API = "https://quotes.toscrape.com/api/quotes?page={}"
REQUEST_INTERVAL = 2.0   # 请求间隔（秒），不低于 2 秒

rows = []
for page in range(1, 4):                       # 抓前 3 页
    resp = requests.get(BASE_API.format(page), timeout=10)
    resp.raise_for_status()
    data = resp.json()
    for q in data.get("quotes", []):
        rows.append({
            "内容": q.get("text", ""),
            "作者": q.get("author", {}).get("name", ""),
            "标签": ",".join(q.get("tags", [])),
        })
    if not data.get("has_next"):               # 没有下一页就停
        break
    time.sleep(REQUEST_INTERVAL)

with open("result_dynamic.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=["内容", "作者", "标签"])
    writer.writeheader()
    writer.writerows(rows)

print(f"成功抓取 {len(rows)} 条，已保存到 result_dynamic.csv")
