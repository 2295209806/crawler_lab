# -*- coding: utf-8 -*-
"""步骤3：完整爬虫——抓取列表页，提取四字段，写入 result.csv 并打印条数。
约束：UA 伪装；请求间隔 >= 2 秒；超时重试 3 次；字段缺失填空串。
运行：python step3_crawler.py
验收：生成 result.csv（UTF-8），终端打印成功抓取条数。
"""
import csv
import time

import requests
from bs4 import BeautifulSoup

TARGET_URL = "https://www.cnblogs.com/"
HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0.0.0 Safari/537.36"),
    "Accept-Language": "zh-CN,zh;q=0.9",
}
REQUEST_INTERVAL = 2.0    # 请求间隔（秒），不低于 2 秒
RETRY_TIMES = 3           # 网络超时重试次数
TIMEOUT = 10              # 单次请求超时（秒）
CSV_FILE = "result.csv"
CSV_HEADERS = ["标题", "发布时间", "作者", "链接"]

ITEM_SELECTOR = "article.post-item"
TITLE_SELECTOR = "a.post-item-title"
TIME_SELECTOR = "span.post-meta-item span"
AUTHOR_SELECTOR = "a.post-item-author"


def fetch_page(url):
    """发送请求并返回 HTML 文本；超时/连接失败重试 RETRY_TIMES 次。"""
    for attempt in range(1, RETRY_TIMES + 1):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            print(f"[OK] 第 {attempt} 次请求成功，状态码 {resp.status_code}")
            return resp.text
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            print(f"[重试] 第 {attempt} 次失败（{type(e).__name__}），"
                  f"{REQUEST_INTERVAL} 秒后重试……")
            if attempt < RETRY_TIMES:
                time.sleep(REQUEST_INTERVAL)
    print("[失败] 重试次数耗尽。")
    return None


def parse_items(html):
    """解析 HTML，字段缺失时填空字符串，避免崩溃。"""
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for node in soup.select(ITEM_SELECTOR):
        a = node.select_one(TITLE_SELECTOR)
        t = node.select_one(TIME_SELECTOR)
        au = node.select_one(AUTHOR_SELECTOR)
        items.append({
            "标题": a.get_text(strip=True) if a else "",
            "发布时间": t.get_text(strip=True) if t else "",
            "作者": au.get_text(strip=True) if au else "",
            "链接": a.get("href", "") if a else "",
        })
    return items


def save_to_csv(items):
    """写入 result.csv（UTF-8 带 BOM，Excel 打开不乱码）。"""
    with open(CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(items)


def main():
    html = fetch_page(TARGET_URL)
    if html is None:
        print("未获取到页面内容，流程终止。")
        return
    items = parse_items(html)
    save_to_csv(items)
    print(f"[完成] 成功抓取 {len(items)} 条数据，已保存到 {CSV_FILE}")


if __name__ == "__main__":
    main()
