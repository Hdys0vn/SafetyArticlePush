"""
@File : SqliteDb
@Description : 
@Author : Shaun
@Modify Time : 2023/10/8 12:21
"""
import sqlite3


class SqliteDb(object):
    """
    操作SQLite3数据操作类
    """

    def __init__(self):
        """初始化"""
        # 连接到数据库（如果不存在则会创建一个新的数据库）
        self.conn = sqlite3.connect('example.db')

        # 创建一个游标对象
        self.cursor = self.conn.cursor()

        # 创建表格（如果不存在）
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS title (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                link TEXT,
                description TEXT,
                author TEXT,
                category TEXT,
                pub_date TEXT
            )
        ''')

    def insert_data(self, name, link, description, author, category, pub_date):
        """
        插入数据
        :param name:
        :param link:
        :param description:
        :param author:
        :param category:
        :param pub_date:
        :return:
        """
        self.cursor.execute('INSERT INTO title (name, link, description, author, category, pub_date) VALUES (?, ?, ?, ?, ?, ?)', (name, link, description, author, category, pub_date))
        self.conn.commit()

    def find_name_if_exits(self, name, description):
        """
        根据name进行查找
        :param name:
        :return:
        """
        self.cursor.execute('SELECT * FROM title where name=? and description=?', (name, description,))
        rows = self.cursor.fetchall()
        if rows:
            return True
        else:
            return False


if __name__ == "__main__":

    sql_connect = SqliteDb();
    sql_connect.insert_data("1", "https://mp.weixin.qq.com/s?__biz=MzI3MDQ1NDE2OA==&mid=2247490021&idx=2&sn=eadc638622e6c88fe5dc80b0ebd83467", "None", "安全后厨", "安全后厨", "Sat, 07 Oct 2023 18:00:23 +0800")
    print(sql_connect.find_name_if_exits("2"))
