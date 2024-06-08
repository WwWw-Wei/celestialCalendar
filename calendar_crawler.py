#!/user/bin/env python
# -*- coding:utf-8 -*-
"""
@File: calendar_crawler.py
@Author：Webb
@Create： 2024/06/07
@Update：~
@Function：obtain celestial events from sky_walks
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from lxml import etree

# events = []
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Mobile Safari/537.36'}
# r = requests.get('https://starwalk.space/zh-Hans/news/astronomy-calendar-2024', headers=headers)
# # pagetitle = soup.find("title")
# soup = BeautifulSoup(r.text, 'lxml')
# info = soup.select('h3')
# for a in info:
#     events.append(a.get_text())
#
# del events[-4:]


def get_events(url):
    events = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.100 Mobile Safari/537.36'}
    r = requests.get(url, headers=headers)
    # pagetitle = soup.find("title")
    soup = BeautifulSoup(r.text, 'lxml')
    info = soup.select('h3')
    for a in info:
        events.append(a.get_text())
    del events[-4:]

    return events

def refine_events(ori_events, year):
    dates, events = [], []
    for event in ori_events:
        dates.append(datetime.strptime(f'{year}年' + re.findall(r'(.+?)日', event)[0] + '日', '%Y年%m月%d日').strftime('%Y%m%d'))  # re.findall()[0] 将list元素转为str元素用于拼接
        events.append(re.findall(r'：(.+)', event)[0])  # ------------------------^^-----------------------
    return dates, events


u = 'https://starwalk.space/zh-Hans/news/astronomy-calendar-2024'

events = get_events(u)

dates, events = refine_events(events, 2024)

# print(dates)
# print(events)
# print(len(dates), len(events))



# 使用etree + xpath解析
# html = etree.HTML(r.text)
# info = html.xpath('//ul[@class = "toc"]//text()')
# print(info)