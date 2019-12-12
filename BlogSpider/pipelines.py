# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import os
from .items import BlogspiderItem
import time
from lxml import html
import html2text


class BlogspiderPipeline(object):
    def __init__(self):
        self.file_head = "---\ntitle: {title}\ndate: {date}\ncategories:\n\t- {categories}\ntags:\n\t- Python\n\t- {tags}\n---\n"
        self.foot = "\n> 文章来源于转载, 如有疑问, 请联系我,转载地址:{} "
        self.tag = None
        self.tags = {
            0: "最新收录",
            1: "热门推荐",
            2: "Crawl",
            3: ["在路上", "旅行"]
        }
        self.category = None
        self.categories = {
            0: "Crawl"
        }

    def process_item(self, item, spider):
        if isinstance(item, BlogspiderItem):
            self.process_runoob(item)
        return item

    def process_runoob(self, item):
        body = item['body']
        utf8_parser = html.HTMLParser(encoding='utf8')
        body_tree = html.fromstring(body, parser=utf8_parser)
        for _item in body_tree.xpath('//img'):
            # print(_item.attrib.keys())
            if "data-src" in _item.attrib.keys():
                _item.attrib['src'] = _item.attrib.pop('data-src'.replace('\n', '').replace('\r', ''))
                print(_item.attrib["src"])
            # elif "data-croporisrc" in _item.attrib.keys():
            #     _item.attrib['src'] = _item.attrib['data-croporisrc']
        body = html.tostring(body_tree, encoding="utf-8")
        file_title = item['title_hash']
        title = item['title']
        if "培训" in title:
            return
        elif "达内" in title:
            return
        else:
            with open('mdfiles/{}.md'.format(file_title),
                      'w', encoding='utf-8') as file:
                self.tag = self.tags[item['category']]
                self.category = self.categories[item['tag']]
                print(self.category)
                if isinstance(self.tag, list):
                    file_head = self.file_head.replace('Python', self.tag[0]).format(
                        title=title, date=item['publish_time'], categories=self.category, tags=self.tag[1])
                else:
                    file_head = self.file_head.format(
                        title=title, date=item['publish_time'], tags=self.tag, categories=None)
                file.write(file_head)
                body = html2text.html2text(body.decode())
                file.write(body)
                file.write(self.foot.format(item['url']))
