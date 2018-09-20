# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jianshu.items import JianshuItem


class JsSpider(CrawlSpider):
    name = 'js'
    #allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/p/3289940289cd']

    rules = (
        Rule(LinkExtractor(allow=r'.*/p/[0-9a-z]{12}.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.xpath('//div[@class="article"]/h1/text()').get()
        author = response.xpath('//div[@class="author"]/div[@class="info"]/span/a/text()').get()
        content = response.xpath('//div[@class="show-content"]').get()
        # content_origin = content.xpath('.//p/text()').getall()
        # content = "".join(content_origin)
        # content = replace("<p>","")
        avatar = response.xpath('//a[@class="avatar"]/img/@src').get()
        pub_time = response.xpath('//span[@class="publish-time"]/text()').get().replace("*", "")
        
        url = response.url
        url1 = url.split('?')[0]
        article_id = url1.split('/')[-1]

        item = JianshuItem(title=title,
            content=content,
            author=author,
            avatar=avatar,
            pub_time=pub_time,
            origin_url=response.url,
            article_id=article_id)
        yield item

