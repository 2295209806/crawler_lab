# -*- coding: utf-8 -*-
"""网络诊断：定位 step3 无输出的原因。"""
import requests

print(">>> 1. 程序开始运行")

print(">>> 2. 系统代理配置:", requests.utils.getproxies())

print(">>> 3. 开始请求 cnblogs.com（超时 5 秒）...")
try:
    r = requests.get(
        "https://www.cnblogs.com/",
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"},
        timeout=5,
    )
    print(">>> 4. 请求成功，状态码:", r.status_code)
except Exception as e:
    print(">>> 5. 异常类型:", type(e).__name__)
    print(">>> 6. 异常内容:", repr(e))

