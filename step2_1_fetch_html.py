# -*- coding: utf-8 -*-
"""步骤2.1：仅发送请求并获取 HTML，验证能否拿到状态码 200 及 HTML 内容。
运行：python step2_1_fetch_html.py
验收：终端打印状态码 200，并输出 HTML 前 500 字符。
"""
import requests

TARGET_URL = "https://www.cnblogs.com/"          # TODO: 替换为目标网站 URL
HEADERS = {                                       # User-Agent 伪装
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/120.0.0.0 Safari/537.36"),
    "Accept-Language": "zh-CN,zh;q=0.9",
}

resp = requests.get(TARGET_URL, headers=HEADERS, timeout=10)
print("状态码:", resp.status_code)
resp.encoding = resp.apparent_encoding            # 自动识别编码，避免乱码
print("HTML 前 500 字符:\n", resp.text[:500])
