# Scrapy settings for news project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'news'

SPIDER_MODULES = ['news.spiders']
NEWSPIDER_MODULE = 'news.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'news (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

MONGO_URI = 'mongodb://huyhn:775748@localhost:27017'
MONGO_DATABASE = 'scraper-news'
MONGO_COLLECTION = 'articles'

ITEM_PIPELINES = {
    'news.pipelines.MongoDB': 300,
}

HOST = 'localhost'
PORT = 5501

UPDATE_NEWS_CRAWLER_STATUS_API_URL = 'http://localhost:8080/api/internal/crawler/news'
