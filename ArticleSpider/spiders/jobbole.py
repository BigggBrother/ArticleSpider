# -*- coding: utf-8 -*-
import scrapy
import re
import sys
from scrapy.http import Request
from urlparse import urljoin
from ArticleSpider.items import JobBoleArticleItem
reload(sys)
sys.setdefaultencoding('utf8')


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts']

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
        article_item = JobBoleArticleItem()


        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        create_date = response.xpath("//p[@class='entry-meta-hide-on-mobile']/text()").extract()[0].strip().replace("·", "").strip()
        praise_nums = response.xpath("//span[contains(@class, 'vote-post-up')]/h10/text()").extract()[0]
        fav_nums = response.xpath("//span[contains(@class, 'bookmark-btn')]/text()").extract()[0]
        match_re = re.match(".*?(\d+).*", fav_nums)


        if match_re:
            fav_nums = match_re.group(1)

        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re = re.match(".*?(\d+).*", comment_nums)

        if match_re:
            comment_nums = match_re.group(1)

        content = response.xpath("//div[@class='entry']").extract()[0]
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)

        front_image_url = response.meta.get("front_image_url", "")

        article_item["title"] = title
        article_item["url"] = response.url
        article_item["create_date"] = create_date
        article_item["front_image_url"] = [front_image_url]
        article_item["praise_nums"] = praise_nums
        article_item["comment_nums"] = comment_nums
        article_item["fav_nums"] = fav_nums
        article_item["tags"] = tags
        article_item["content"] = content


        # article_item = item_loader.load_item()
        yield article_item
        pass
