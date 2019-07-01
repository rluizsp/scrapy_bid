# -*- coding: utf-8 -*-
import scrapy


class BidSpider(scrapy.Spider):
    name = 'bid'
    allowed_domains = ['zukerman.com.br']

    start_urls = (
        'https://www.zukerman.com.br/imoveis-residenciais',
    )

    def parse(self, response):
        items = response.xpath(
            '//div[contains(@class,"s-it-cd")]//div[contains'
            '(@class,"cd-0")]'
        )
        for item in items:
            url = item.xpath(
                ".//a[contains(@class,'cd-it-img')]/@href"
            ).extract_first()
            yield scrapy.Request(url=url, callback=self.parse_detail)

    def parse_detail(self, response):
        self.log(u'Imóvel URL: {0}'.format(response.url))
        title = response.xpath('//div[@class="s-d-l-m"]//normalize-space(h1)')
        self.log(u'Título: {0}'.format(title))






