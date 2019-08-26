# -*- coding: utf-8 -*-
import scrapy
import validators
import re



class GuariglialeiloesSpider(scrapy.Spider):
    name = 'guariglialeiloes'
    allowed_domains = ['guariglialeiloes.com.br']

    def start_requests(self):
        urls = ['http://guariglialeiloes.com.br/']

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        catalogs = response.xpath(
            '//div[contains(@class,"card-body")]'
        )

        for catalog in catalogs:
            url = catalog.xpath(
                ".//a/@href"
            ).extract_first()
            self.log(catalog)

            if validators.url(url):
                self.logger.info("catalog: "+url);
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
                # self.logger.info(url);
                yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
            '//ul[contains(@class,"pagination")]/li[7]//a/@href'
        ).extract_first()

        # self.logger.info("next_page"next_page);

        if next_page:
            self.logger.info("next_page: "+next_page);
            self.log('Next Page: {0}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse_item)

    def parse_detail(self, response):
        bid = Bid()
        bid['item_url'] = response.url
        bid['item_name'] = response.xpath('//div[contains(@class,"px-1")]//h4/text()').extract()
        bid['item_view_count'] = response.xpath('//div[contains(@class,"detalhes-lote")]/div/div[3]/div/div[5]/span/text()').extract()
        item_price = response.xpath('//div[contains(@class,"detalhes-lote")]/div/div[3]/div/div/h3[1]/text()').extract()

        a = item_price.replace('R$','')
        b = a.replace('.','')
        c = b.replace(',','.')


        bid['item_price'] = c

        # leil['leilao'] = time.strftime("%d/%m/%Y, %H:%M:%S")

        bid['bid_name'] = 'guariglialeiloes'

        alphabet = response.xpath('//div[contains(@class,"px-1")]//h4/text()').extract()

        print(self.find_numbers(bid['item_price']))

        data = alphabet[0].split("-")

        print(bid['item_price'])

        return leil


    def find_numbers(string, ints=True):
        numexp = re.compile(r'[-]?\d[\d,]*[\.]?[\d{2}]*')  # optional - in front
        numbers = numexp.findall(string)
        numbers = [x.replace(',', '') for x in numbers]
        if ints is True:
            return [int(x.replace(',', '').split('.')[0]) for x in numbers]
        else:
            return numbers

class Bid(scrapy.Item):
    bid_name = scrapy.Field()
    item_name = scrapy.Field()
    item_price = scrapy.Field()
    item_description = scrapy.Field()
    ttimestamp = scrapy.Field()
    item_model_desc = scrapy.Field()
    item_model_year = scrapy.Field()
    item_made_year = scrapy.Field()
    item_url = scrapy.Field()
    item_view_count = scrapy.Field()


