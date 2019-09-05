import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_bid.spiders.guariglialeiloes_old import GuariglialeiloesSpider

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(GuariglialeiloesSpider)
process.start()