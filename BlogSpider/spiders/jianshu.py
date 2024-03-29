

import os
from hashlib import md5
from scrapy import Spider, Request
from ..items import BlogspiderItem


class JianShu(Spider):
    name = "jianshu"
    base_url = 'http://www.jianshu.com'
    
    def start_requests(self):
        start_urls = ['https://www.jianshu.com/c/22f2ca261b85',
                      'https://www.jianshu.com/c/22f2ca261b85?order_by=top',
                      'https://www.jianshu.com/c/5AUzod?order_by=hot']
        for item in start_urls:
            self.settings['HEADERS']['Referer'] = item
            yield Request(item, callback=self.parse, headers=self.settings['HEADERS'],
                          dont_filter=True)

    def parse(self, response):
        category = 0
        if 'top' in response.url:
            category = 1
        elif 'hot' in response.url:
            category = 3
        
        meta = {"category": category}
        result = response.xpath('//*[@class="note-list"]/li/a')
        for item in result:
            url = self.base_url + item.xpath('@href').extract()[0]
            yield Request(url,
                          callback=self.get_page_info,
                          headers=self.settings['HEADERS'],
                          meta=meta,
                          dont_filter=True,
                          )

    def get_page_info(self, response):
        item = BlogspiderItem()
        try:
            title = response.xpath('//*[@class="title"]/text()').extract()[0]
        except:
            print(response.text)
            os._exit(0)
        item['publish_time'] = response.xpath('//*[@class="publish-time"]/text()').extract()[0]
        title_hash = md5(title.encode()).hexdigest()
        category = response.meta['category']
        body = response.xpath('//*[@class="show-content"]').extract()[0]
        item['title'] = title
        item['title_hash'] = title_hash
        item['body'] = body
        item['url'] = response.url
        item['category'] = category
        yield item
