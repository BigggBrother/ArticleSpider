# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from datetime import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

def remove_comment_tags(value):
    if "评论" in value:
        return None
    else:
        return value

def date_structure(value):
    try:
        create_date = datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_date = datetime.now().date()
    return create_date

class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field(input_processor=MapCompose(date_structure))
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field(input_processor=MapCompose(remove_comment_tags), output_processor=Join(","))


    # 以下为异步需要用到的代码 todo
    # def get_insert_sql(self):
    #     insert_sql = """INSERT INTO jobbole_article(title, url, create_date, fav_nums, comment_nums, tags)
    #         VALUES ('%s', '%s', '%s', '%s', '%s', '%s');""" \
    #         % (item["title"], item["url"], item["create_date"], item["fav_nums"], item["comment_nums"], item["tags"])

class JobBoleArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

