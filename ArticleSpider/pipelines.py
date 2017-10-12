# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from MySQLdb import cursors
from twisted.enterprise import adbapi
from scrapy.pipelines.images import ImagesPipeline

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

class ArticleImagePipline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok, value in results:
            image_file_path = value['path']
        item['front_image_path'] = image_file_path
        return item

class MysqlPipeline(object):
    def __init__(self):
        self.conn = MySQLdb.connect('localhost', 'root', 'qwe123',
                                    'article_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """INSERT INTO jobbole_article(title, url, create_date, fav_nums, comment_nums, tags)
                        VALUES ('%s', '%s', '%s', '%s', '%s', '%s');""" \
                     % (item["title"], item["url"], item["create_date"], item["fav_nums"], item["comment_nums"], item["tags"])
        self.cursor.execute(insert_sql)
        self.conn.commit()


# 以下为异步mysql，todo
# class MysqlTwistedPipline(object):
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbparms = dict(
#             host = settings["MYSQL_HOST"],
#             db = settings["MYSQL_DBNAME"],
#             user = settings["MYSQL_USER"],
#             passwd = settings["MYSQL_PASSWORD"],
#             charset = 'utf8',
#             use_unicode = True,
#             cursorclass = cursors.DictCursor,
#         )
#         dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
#         return cls(dbpool)
#
#     def handle_error(self, failure, item, spider):
#         print failure
#
#     def do_insert(self, cursor, item):
#         inset = item.job
