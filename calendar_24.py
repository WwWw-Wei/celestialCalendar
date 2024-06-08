#!/user/bin/env python
# -*- coding:utf-8 -*-
"""
@File: calendar_24.py
@Author：Webb
@Create： 2024/06/07
@Update：~
@Function：generate the ics format file to describe the calendar of celestials in 2024
"""

from datetime import datetime
from calendar_crawler import get_events, refine_events


now = datetime.now().strftime('%Y%m%dT%H:%M:%S')


def set_ics_header(name):
    return "BEGIN:VCALENDAR\n" \
        + "PRODID:NULL\n" \
        + "VERSION:2.0\n" \
        + "CALSCALE:GREGORIAN\n" \
        + "METHOD:PUBLISH\n" \
        + f"X-WR-CALNAME:{name}\n" \
        + "X-WR-TIMEZONE:Asia/Shanghai\n" \
        + f"X-WR-CALDESC:{name}\n" \
        + "BEGIN:VTIMEZONE\n" \
        + "TZID:Asia/Shanghai\n" \
        + "X-LIC-LOCATION:Asia/Shanghai\n" \
        + "BEGIN:STANDARD\n" \
        + "TZOFFSETFROM:+0800\n" \
        + "TZOFFSETTO:+0800\n" \
        + "TZNAME:CST\n" \
        + "DTSTART:19700101T000000\n" \
        + "END:STANDARD\n" \
        + "END:VTIMEZONE\n"


def set_ce_ics(ce, date, uid):  # ce: 天文事件，date：日期，uid：编序
    return "BEGIN:VEVENT\n" \
        + f"DTSTART;VALUE=DATE:{date}\n" \
        + f"DTEND;VALUE=DATE:{date}\n" \
        + f"DTSTAMP:{date}T000001\n" \
        + f"UID:{date}T{uid:0>6}_jr\n" \
        + f"CREATED:{date}T000001\n" \
        + f"DESCRIPTION:{ce}\n" \
        + f"LAST-MODIFIED:{now}\n" \
        + "SEQUENCE:0\n" \
        + "STATUS:CONFIRMED\n" \
        + f"SUMMARY:{ce}\n" \
        + "TRANSP:TRANSPARENT\n" \
        + "END:VEVENT\n"


# 返回一个完整的ics文件内容
def concat_ics(c_name, event_list, date_list):
    header = set_ics_header(c_name)
    # 将节日进行编号，生成list转成字符串
    cc_ics = ''.join(list(map(set_ce_ics, event_list, date_list, list(range(len(event_list))))))
    return header + cc_ics + 'END:VCALENDAR'


# 保存文件
def save_ics(fname, text):
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(text)


if __name__ == '__main__':
    calendarName = 'CelestialCalendar_2024'
    year = 2024
    events_source = 'https://starwalk.space/zh-Hans/news/astronomy-calendar-2024'
    events = get_events(events_source)
    dates, events = refine_events(events, year)
    CC_ics = concat_ics(calendarName, events, dates)
    save_ics(f'calendar_{calendarName}.ics', CC_ics)
