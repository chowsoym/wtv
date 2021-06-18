#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import random
from time import sleep
from m3u_parser import M3uParser

useragent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"


def sleep_random():
    """随机等待5-10秒防止IP被封"""
    sleep_s = random.randint(1, 5)
    sleep(sleep_s)


def check_url_ok(url):
    """检测连接是否可用"""
    print("\n正在检查URL %s \n" % url)
    try:
        result = requests.get(url, headers={"User-Agent": useragent}, timeout=8)
        return result.status_code == 200
    except requests.exceptions.ConnectionError:
        print("URL %s 访问超时" % url)
    return False


if __name__ == "__main__":
    # URL 合集
    urls = [
        "../m3u/cn-gbk.m3u",
        # "../m3u/hk.m3u",
        # "../m3u/tw.m3u"
    ]
    m3u_playlist = M3uParser(timeout=5, useragent=useragent)
    for url in urls:
        output = []
        m3u_playlist.parse_m3u(url)
        # print(m3u_playlist.get_list())
        m3u_list = map(lambda item: {"name": item.get("name", ""), "url": item.get("url", "")}, m3u_playlist.get_list())
        for m in m3u_list:
            try:
                sleep_random()
                url = (m.get("url", ""))
                if not check_url_ok(url):
                    continue
                m3nItem = "#EXTINF:-1 ,{name}\n\r{url}".format(name=m.get("name"), url=url)
                output.append(m3nItem)
                print(m3nItem)
            except Exception as ex:
                print("URL %s ex:" % url, ex)
        f = open("%s.out" % url, "w", encoding="utf-8")
        f.write("\n\r".join(output))
        f.close()

