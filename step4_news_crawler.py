# -*- coding: utf-8 -*-
"""步骤4：将 step3 的过程式代码重构为面向对象的 NewsCrawler 类，功能保持不变。
改进点：常量集中、Session 复用连接、逐字段容错、便于扩展。
运行：python step4_news_crawler.py
验收：输出与 step3 一致（result.csv + 终端打印条数）。
"""
import csv
import time

import requests
from bs4 import BeautifulSoup


class NewsCrawler:
    """新闻列表页爬虫：抓取标题、发布时间、作者、链接并保存为 CSV。"""

    TARGET_URL = "https://www.cnblogs.com/"
    HEADERS = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/120.0.0.0 Safari/537.36"),
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    REQUEST_INTERVAL = 2.0
    RETRY_TIMES = 3
    TIMEOUT = 10
    CSV_FILE = "result.csv"
    CSV_HEADERS = ["标题", "发布时间", "作者", "链接"]

    ITEM_SELECTOR = "article.post-item"
    TITLE_SELECTOR = "a.post-item-title"
    TIME_SELECTOR = "span.post-meta-item span"
    AUTHOR_SELECTOR = "a.post-item-author"

    def __init__(self):
        self.session = requests.Session()          # 复用连接，提升性能
        self.session.headers.update(self.HEADERS)

    def fetch_page(self, url):
        """超时/连接失败自动重试 RETRY_TIMES 次，重试间隔 >= REQUEST_INTERVAL 秒。"""
        for attempt in range(1, self.RETRY_TIMES + 1):
            try:
                resp = self.session.get(url, timeout=self.TIMEOUT)
                resp.raise_for_status()
                resp.encoding = resp.apparent_encoding
                print(f"[OK] 第 {attempt} 次请求成功，状态码 {resp.status_code}")
                return resp.text
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                print(f"[重试] 第 {attempt} 次失败（{type(e).__name__}），"
                      f"{self.REQUEST_INTERVAL} 秒后重试……")
                if attempt < self.RETRY_TIMES:
                    time.sleep(self.REQUEST_INTERVAL)
        print("[失败] 重试次数耗尽。")
        return None

    @staticmethod
    def _safe_text(node, selector):
        if node is None:
            return ""
        target = node.select_one(selector)
        return target.get_text(strip=True) if target else ""

    @staticmethod
    def _safe_link(node, selector):
        if node is None:
            return ""
        target = node.select_one(selector)
        return target.get("href", "") if target else ""

    def parse_items(self, html):
        soup = BeautifulSoup(html, "html.parser")
        items = []
        for node in soup.select(self.ITEM_SELECTOR):
            items.append({
                "标题": self._safe_text(node, self.TITLE_SELECTOR),
                "发布时间": self._safe_text(node, self.TIME_SELECTOR),
                "作者": self._safe_text(node, self.AUTHOR_SELECTOR),
                "链接": self._safe_link(node, self.TITLE_SELECTOR),
            })
        return items

    def save_to_csv(self, items):
        with open(self.CSV_FILE, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_HEADERS)
            writer.writeheader()
            writer.writerows(items)

    def run(self):
        html = self.fetch_page(self.TARGET_URL)
        if html is None:
            return
        items = self.parse_items(html)
        if not items:
            print("[提示] 未解析到数据，请核对选择器是否匹配目标网站结构。")
            return
        self.save_to_csv(items)
        print(f"[完成] 成功抓取 {len(items)} 条数据，已保存到 {self.CSV_FILE}")


if __name__ == "__main__":
    NewsCrawler().run()
