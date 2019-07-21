# -*- coding: utf-8 -*-
import scrapy
import validators


class GuariglialeiloesSpider(scrapy.Spider):
    name = 'guariglialeiloes'
    allowed_domains = ['guariglialeiloes.com.br']
    start_urls = ['https://www.guariglialeiloes.com.br/']

    def parse(self, response):
        catalogs = response.xpath(
            '//div[contains(@class,"infinitescroll")]'
        )

        for catalog in catalogs:
            url = catalog.xpath(
                "./div/div/div/div//a/@href"
            ).extract_first()
            self.log(catalog)
            self.logger.info(url);

            yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        items = response.xpath(
            '//div[contains(@class,"body-lote")]'
        )

        for item in items:
            url = item.xpath(
                 ".//a/@href"
            ).extract_first()
            self.log(item)

            if validators.url(url):
                self.logger.info(url);

          #  yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
            '//ul[contains(@class,"pagination")]/div[2]/@href'
        ).extract_first()

        self.logger.info('next_page: {0}'.format(next_page))

        if next_page:
            self.log('Next Page: {0}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        title   = response.xpath('//div[contains(@class,"px-1")]//h4/text()').extract()
     #   auction = response.xpath('//div[contains(@class,"text-center")]/span/i/text()').extract()
        view    = response.xpath('//div[contains(@class,"text-center")]/span/i/text()').extract()
        self.logger.info(u'catalogo URL: {0}'.format(response.url))
    #   self.logger.info(u'auction: {0}'.format(auction))
        self.logger.info('Título: {0}'.format(title))
        self.logger.info('Views: {0}'.format(view))














