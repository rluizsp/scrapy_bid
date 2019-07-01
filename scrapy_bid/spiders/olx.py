# -*- coding: utf-8 -*-
import scrapy


class OlxSpider(scrapy.Spider):
    name = "olx"
    allowed_domains = ["pe.olx.com.br"]
    start_urls = (
        'http://pe.olx.com.br/imoveis/aluguel',
    )

    def parse(self, response):
        items =  response.xpath(
            '//div[contains(@class,"section_OLXad-list")]//li[contains'
            '(@class,"item")]'
        )
        for item in items:
            url = item.xpath(
                ".//a[contains(@class,'OLXad-list-link')]/@href"
            ).extract_first()
            yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
            '//li[contains(@class,"item next")]//a/@href'
        ).extract_first()
        if next_page:
            self.log('Next Page: {0}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        self.log(u'Imóvel URL: {0}'.format(response.url))
        title = response.xpath('normalize-space(//h1[contains(@id,"ad_title")]//.)').extract_first()
        self.log(u'Título: {0}'.format(title))




