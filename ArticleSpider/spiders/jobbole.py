# -*- coding: utf-8 -*-
import scrapy
import re
import sys
from scrapy.http import Request
from urlparse import urljoin
from ArticleSpider.items import JobBoleArticleItem, JobBoleArticleItemLoader
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
reload(sys)
sys.setdefaultencoding('utf8')


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/page/553/']

    def parse(self, response):
        post_nodes = response.xpath('//div[@class="post floated-thumb"]/div[@class="post-thumb"]')
        for post_node in post_nodes:
            image_url = post_node.xpath('a/img/@src').extract_first()
            post_url = post_node.xpath('a/@href').extract_first()
            yield Request(url=urljoin(response.url, post_url), meta={'front_image_url': image_url},
                          callback=self.parse_detail)
        next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first("")
        if next_url:
            yield Request(url=urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        item_loader = JobBoleArticleItemLoader(item=JobBoleArticleItem(), response=response)

        try:
            praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
        except:
            praise_nums = 0
        print praise_nums

        fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)

        if match_re:
            fav_nums = match_re.group(1)
        else:
            fav_nums = 0

        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)
        if match_re:
            comment_nums = match_re.group(1)
        else:
            comment_nums = 0

        front_image_url = response.meta.get("front_image_url", "")

        # front_image_url = response.meta.get("front_image_url", "")
        item_loader.add_xpath('title', '//div[@class="entry-header"]/h1/text()')
        # item_loader.add_xpath('content', "//div[@class='entry']")
        item_loader.add_value('url', response.url)
        item_loader.add_xpath('create_date', "//p[@class='entry-meta-hide-on-mobile']/text()",
                              MapCompose(lambda x: x.strip().replace("·", "").strip(), unicode.title))
        item_loader.add_value('fav_nums', fav_nums)
        item_loader.add_value('comment_nums', comment_nums)
        item_loader.add_xpath('tags', "//p[@class='entry-meta-hide-on-mobile']/a/text()")
        article_item = item_loader.load_item()
        print article_item
        yield article_item
        pass
