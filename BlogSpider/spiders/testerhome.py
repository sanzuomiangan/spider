# -*- coding: utf-8 -*-
import os
from hashlib import md5
from scrapy import Spider, Request
from ..items import BlogspiderItem
import json
import time
from scrapy_splash import SplashRequest, SlotPolicy


class JianShu(Spider):
    name = "testerhome"
    base_url = 'http://www.jianshu.com'
    start_urls = [
        "https://testerhome.com/topics/6058"]

    def parse(self, response):
        # print(response.text)
        # print(json.loads(response.text))
        row = response.text
        item = BlogspiderItem()
        url = "https://testerhome.com/topics/6557"
        # item["title"] = row["name"]
        # item["title_hash"] = md5(row["name"].encode()).hexdigest()
        # item["publish_time"] = row["publishTime"]
        item['category'] = 3
        item['tag'] = 0
        item["url"] = url
        # print(url)
        # print(item)
        yield Request(url, self.parse_body, meta={"item": item})
    #
    def parse_body(self, response):
        pattern = '//*[@class="panel-body markdown markdown-toc"]'
        title = '//*[@class="title"]'
        timeage = '//*[@class="timeago"]'
        title = response.xpath(title).extract()
        timeage = response.xpath(timeage).extract()
        print("="*10)
        # print(response)
        body = response.xpath(pattern).extract()
        print(body)
        if not body:
            return
        item = response.meta["item"]
        item["title"] = title[0]
        item["publish_time"] = timeage[0]
        item["title_hash"] = md5(item["title"].encode()).hexdigest()
        item["body"] = body[0]
        # print(item["body"])
        print({"url": item["url"], "title": item["title"], "hash": item["title_hash"]})
        return item
