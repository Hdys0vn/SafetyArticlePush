"""
@File : send_data.py
@Description :
@Author : Shaun
@Modify Time : 2023/10/8 9:21
"""
import datetime
import xml.etree.ElementTree as ET
import requests
import feedparser

class Rss(object):
    """
    RSS类
    """
    def __init__(self):
        """
        初始化
        """
        # 解析XML文件
        tree = ET.parse('conf/rss.xml')  # 将'config.xml'替换为您的配置文件路径
        root = tree.getroot()

        # 获取所有text和xmlUrl的内容
        self.rss_data = {}
        for outline in root.findall(".//outline[@type='rss']"):
            text = outline.attrib['text']
            xml_url = outline.attrib['xmlUrl']
            self.rss_data[text] = xml_url

    def get_rss_data(self):
        """
        获取最新订阅数据
        :return:
        """
        error_list = []
        add_number = 0
        result_dict = {}
        for key, value in self.rss_data.items():
            print(f"正在爬取{key} - {value}")
            # 发起HTTP请求
            try:
                response = requests.get(value, timeout=20)

                # 解析XML结果
                if response.status_code == 200:
                    xml_data = response.content
                    root = ET.fromstring(xml_data)
                    # 找到所有的item元素
                    if b"http://www.w3.org/2005/Atom" in xml_data and (b"xmlns:atom=" not in xml_data):
                        items = root.findall('{http://www.w3.org/2005/Atom}entry')
                    elif b"xmlns:atom=" in xml_data:
                        feed = feedparser.parse(value)
                        items = feed.entries
                    else:
                        items = root.findall('.//item')
                    if not items:
                        print(f"error: {key} - {value}")
                    # 遍历每个item元素并解析
                    for item in items:
                        if b"http://www.w3.org/2005/Atom" in xml_data and (b"xmlns:atom=" not in xml_data):
                            title = item.find('{http://www.w3.org/2005/Atom}title')
                            link = item.find('{http://www.w3.org/2005/Atom}link')
                            description = item.find('{http://www.w3.org/2005/Atom}content')
                            author = item.find('{http://www.w3.org/2005/Atom}author')
                            category = item.find('{http://www.w3.org/2005/Atom}category')
                            pub_date = item.find('{http://www.w3.org/2005/Atom}updated')
                        elif b"xmlns:atom=" in xml_data:
                            title = item.get("title", "")
                            link= item.get("link", "")
                            description = item.get("description", "")
                            author = item.get("author", "")
                            category = item.get("category", "")
                            pub_date = item.get("pubDate", "")
                            result_dict[title] = {
                                "title": title,
                                "link": link,
                                "description": description,
                                "author": author,
                                "category": category,
                                "pubDate": pub_date
                            }
                            continue
                        else:
                            title = item.find('title')
                            link = item.find('link')
                            description = item.find('description')
                            author = item.find('author')
                            category = item.find('category')
                            pub_date = item.find('pubDate')
                        if (b"http://www.w3.org/2005/Atom" in xml_data) and ("/feed" not in value) and (link is not None):
                            link = link.attrib["href"]
                        elif (link is not None):
                            link = link.text
                        else:
                            continue
                        if (title is not None):
                            title = title.text
                        else:
                            continue
                        if description is not None:
                            description = description.text
                            if not description:
                                description = ""
                        else:
                            description = ""
                        if author is not None:
                            author = author.text
                        else:
                            author = ""
                        if category is not None:
                            category = category.text
                        if pub_date is not None:
                            pub_date = pub_date.text
                        result_dict[title] = {
                            "title": title,
                            "link": link,
                            "description": description,
                            "author": author,
                            "category": category,
                            "pubDate": pub_date
                        }
            except Exception as e:
                error_list.append(f"{key} - {value} - {str(e)}")
                continue
            print(f"已爬取完{key} - {value}，当前总样本：{len(result_dict.keys())} - 新增样本：{len(result_dict.keys()) - add_number}")
            add_number = len(result_dict.keys())
        return result_dict

    def check_rss(self):
        """
        测试rss是否有出现问题
        :return:
        """
        error_list = []
        for key, value in self.rss_data.items():
            print(f"正在测试{key} - {value}")
            try:
                response = requests.get(value)
            except Exception as e:
                error_list.append(f"{key} - {value}")
        print(error_list)


if __name__ == "__main__":
    rss_test = Rss()
    print(rss_test.get_rss_data())
