"""
@File : send_data.py
@Description :
@Author : Shaun
@Modify Time : 2023/10/8 9:21
"""
import sys
import time

import requests
from db.SqliteDb import SqliteDb
import datetime
from conf import conf
from rss.rss import Rss


def usePY2WeChatGroup(sql_conn, url, result_list):
    """
    发送数据
    :param result_list:
    :return:
    """
    try:
        number = 0
        for result in result_list:
            message = f"""叮叮，新增安全类文章：<font color="warning">{len(result)}</font>"""
            for one in result:
                number += 1
                if "<" in one["description"]:
                    message += f"""\r\n>{number}、<font color="comment">[{one["title"]}]({one["link"]})</font>"""
                else:
                    message += f"""\r\n>{number}、<font color="comment">[{one["title"]}]({one["link"]})</font>\r\n{one["description"][:100]}"""

            data = {
                    "msgtype": "markdown",
                    "markdown": {
                        "content": message
                    }
                }

            requests.post(url, json=data)
            number = 0
            # 更新数据库
            for one in result:
                sql_conn.insert_data(one["title"], one["link"], one["description"], one["author"], one["category"], one["pub_date"])
    except Exception as e:
        print(e)


def run(sql_conn, rss_console):
    """
    从微信文章中获取最新的文章
    :return:
    """
    # 安全文章
    SafetyArticleList = []
    # 漏洞预警
    VulnerabilityWarningList = []
    # 漏洞复现
    VulnerabilityRecurrenceList =[]
    # 免杀
    KillImmuneList = []
    # 实战攻防
    OffensiveAndDefensiveProjectList = []

    result_dict = rss_console.get_rss_data()

    # 遍历每个item元素并解析
    for key, item in result_dict.items():
        title = item['title']
        link = item['link']
        description = item['description']
        author = item['author']
        category = item['category']
        pub_date = item['pubDate']
        if not title:
            continue
        if sql_conn.find_name_if_exits(title, description):
            continue
        else:
            if any(blackword in title for blackword in conf.SafetyArticleBlackKeyWord):
                continue
            elif any(blackword in title for blackword in conf.SafetyArticleKeyWord):
                SafetyArticleList.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "author": author,
                    "category": category,
                    "pub_date": pub_date
                    })
            elif any(blackword in title for blackword in conf.VulnerabilityWarningKeyWord):
                VulnerabilityWarningList.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "author": author,
                    "category": category,
                    "pub_date": pub_date
                    })
            elif any(blackword in title for blackword in conf.OffensiveAndDefensiveProjectKeyWord):
                OffensiveAndDefensiveProjectList.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "author": author,
                    "category": category,
                    "pub_date": pub_date
                })
            elif any(blackword in title for blackword in conf.KillImmuneKeyWord):
                KillImmuneList.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "author": author,
                    "category": category,
                    "pub_date": pub_date
                })
            elif any(blackword in title for blackword in conf.VulnerabilityRecurrenceKeyWord):
                VulnerabilityRecurrenceList.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "author": author,
                    "category": category,
                    "pub_date": pub_date
                })
            else:
                SafetyArticleList.append({
                    "title": title,
                    "link": link,
                    "description": description,
                    "author": author,
                    "category": category,
                    "pub_date": pub_date
                })

    if SafetyArticleList:
        print(f"{datetime.datetime.now()} - 新增安全文章： {len(SafetyArticleList)}")
        usePY2WeChatGroup(sql_conn, conf.SafetyArticle, [SafetyArticleList[i:i+10] for i in range(0, len(SafetyArticleList), 10)])
    if VulnerabilityWarningList:
        print(f"{datetime.datetime.now()} - 新增漏洞预警： {len(VulnerabilityWarningList)}")
        usePY2WeChatGroup(sql_conn, conf.VulnerabilityWarning, [VulnerabilityWarningList[i:i+10] for i in range(0, len(VulnerabilityWarningList), 10)])
    if VulnerabilityRecurrenceList:
        print(f"{datetime.datetime.now()} - 新增漏洞复现： {len(VulnerabilityRecurrenceList)}")
        usePY2WeChatGroup(sql_conn, conf.VulnerabilityRecurrence, [VulnerabilityRecurrenceList[i:i+10] for i in range(0, len(VulnerabilityRecurrenceList), 10)])
    if KillImmuneList:
        print(f"{datetime.datetime.now()} - 新增免杀： {len(KillImmuneList)}")
        usePY2WeChatGroup(sql_conn, conf.KillImmune, [KillImmuneList[i:i+10] for i in range(0, len(KillImmuneList), 10)])
    if OffensiveAndDefensiveProjectList:
        print(f"{datetime.datetime.now()} - 新增实战攻防： {len(OffensiveAndDefensiveProjectList)}")
        usePY2WeChatGroup(sql_conn, conf.OffensiveAndDefensiveProject, [OffensiveAndDefensiveProjectList[i:i+10] for i in range(0, len(OffensiveAndDefensiveProjectList), 10)])


def main():
    """
    主函数
    :return:
    """
    sql_conn = SqliteDb()
    rss_console = Rss()
    while True:
        run(sql_conn, rss_console)
        print(f"【～】当前时间：{datetime.datetime.now()}")
        time.sleep(600)


if __name__ == "__main__":
    main()
