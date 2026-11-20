# -*- coding: utf-8 -*-
"""步骤5（进阶）：动态渲染网站（Vue/React）爬取 —— 方案一：Playwright 浏览器渲染。

目标站 quotes.toscrape.com/js 的内容由 JS 注入，requests 抓 HTML 是空壳（.quote 数量为 0），
必须等浏览器渲染完成后再提取。
依赖：pip install playwright  &&  playwright install chromium
运行：python step5_dynamic_render.py
"""
from playwright.sync_api import sync_playwright

TARGET_URL = "https://quotes.toscrape.com/js/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(TARGET_URL, wait_until="networkidle")   # 等 JS 渲染完成
    page.wait_for_selector("div.quote", timeout=10000)
    nodes = page.query_selector_all("div.quote")
    data = []
    for node in nodes:
        text = node.query_selector("span.text")
        author = node.query_selector("small.author")
        data.append({
            "内容": text.inner_text() if text else "",
            "作者": author.inner_text() if author else "",
        })
    browser.close()

print(f"抓取到 {len(data)} 条：")
for item in data[:3]:
    print("  ", item["内容"], "——", item["作者"])
