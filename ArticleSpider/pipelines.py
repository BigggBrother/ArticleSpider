# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
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
        self.conn = MySQLdb.connect('192.2.4.22', 'root', 'root.com',
                                    'article_spider', charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()
    def process_item(self, item, spider):
        insert_sql = """INSERT INTO jobbole_article(title, url, create_date, fav_nums, comment_nums) 
                        VALUES ('%s', '%s', '%s', '%s', '%s');""" \
                     % (item["title"], item["url"], item["create_date"], item["fav_nums"], item["comment_nums"])
        self.cursor.execute(insert_sql)
        self.conn.commit()