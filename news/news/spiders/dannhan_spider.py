import re
import uuid
import datetime
import scrapy
from scrapy.http.response import Response


class NhanDanSpider(scrapy.Spider):
    name = 'nhandan'

    def start_requests(self):
        urls_dict = {
            "https://nhandan.com.vn/chinhtri": "chinh-tri",
            "https://nhandan.com.vn/xahoi": "xa-hoi",
            "https://nhandan.com.vn/vanhoa": "van-hoa",
            "https://nhandan.com.vn/giaoduc": "giao-duc",
            "https://nhandan.com.vn/khoahoc-congnghe": "khoa-hoc",
            "https://nhandan.com.vn/y-te": "y-te",
            "https://nhandan.com.vn/thethao": "the-thao",
        }
        for url in urls_dict:
            yield scrapy.Request(url=url, callback=self.parse_article_url_list, meta={"category_url": url,
                                                                                      "category": urls_dict[url]})

    def parse_article_url_list(self, response):
        urls = response.css('.boxlist-list').re(r'(\/[^"]*-\d+\/)')
        urls = list(set(urls))
        for url in urls:
            yield scrapy.Request(url="https://nhandan.com.vn" + url, callback=self.parse_content_article, meta=response.meta)

    def parse_content_article(self, response: Response):
        content = " ".join(response.css('.box-content-detail p::text').getall())
        article = {
            'uuid_url': str(uuid.uuid5(uuid.NAMESPACE_DNS, response.url)),
            'url': response.url,
            'domain': self.name,
            'title': response.css('h1::text').get().strip(),
            'category_url': response.meta['category_url'],
            'category': response.meta['category'],
            'time': self.parse_datetime(response.css('.box-date::text').get()),
            'content': content
        }
        yield article

    def parse_datetime(self, datetime_str):
        try:
            date_pattern = re.compile(r"\d{1,2}\/\d{1,2}\/\d{4}")
            time_pattern = re.compile(r"\d{1,2}:\d{1,2}")

            date_str = re.findall(date_pattern, datetime_str)
            if len(date_str) == 1:
                date_str = date_str[0]
            else:
                raise Exception(f"Cannot parser date from {datetime_str}")

            time_str = re.findall(time_pattern, datetime_str)
            if len(time_str) == 1:
                time_str = time_str[0]
            else:
                raise Exception(f"Cannot parser time from {datetime_str}")
        except(Exception,) as exc:
            return datetime.datetime.now()

        datetime_str = date_str + " " + time_str
        return datetime.datetime.strptime(datetime_str, '%d/%m/%Y %H:%M')