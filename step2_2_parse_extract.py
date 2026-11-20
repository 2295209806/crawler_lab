# -*- coding: utf-8 -*-
"""步骤2.2：解析 HTML，提取标题/发布时间/作者/链接，打印前 3 条验证解析逻辑。
运行：python step2_2_parse_extract.py
验收：打印前 3 条数据的标题与链接，字段值与网页一致。
"""
import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://www.cnblogs.com/"
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0.0.0 Safari/537.36"),
    "Accept-Language": "zh-CN,zh;q=0.9",
}

resp = requests.get(TARGET_URL, headers=HEADERS, timeout=10)
resp.encoding = resp.apparent_encoding
soup = BeautifulSoup(resp.text, "html.parser")

# 选择器需对应目标网站真实结构（浏览器 F12 查看）
ITEM_SELECTOR = "article.post-item"
TITLE_SELECTOR = "a.post-item-title"
TIME_SELECTOR = "span.post-meta-item span"
AUTHOR_SELECTOR = "a.post-item-author"

for i, node in enumerate(soup.select(ITEM_SELECTOR)[:3]):
    a = node.select_one(TITLE_SELECTOR)
    t = node.select_one(TIME_SELECTOR)
    au = node.select_one(AUTHOR_SELECTOR)
    print(f"第 {i + 1} 条")
    print("  标题:", a.get_text(strip=True) if a else "")
    print("  链接:", a.get("href", "") if a else "")
    print("  时间:", t.get_text(strip=True) if t else "")
    print("  作者:", au.get_text(strip=True) if au else "")
