# -*- coding: utf-8 -*-
import scrapy
import validators
import time
import os



class GuariglialeiloesSpider_Old(scrapy.Spider):
    name = 'guariglialeiloes'
    allowed_domains = ['guariglialeiloes.com.br']


    def start_requests(self):
        urls = ['https://www.guariglialeiloes.com.br/']
        if os.path.isfile("bets.txt") == False:
            with open('bets.txt', 'w') as f:
                f.write("DATA / ID , HORA , LEILAO , LOTE , DESCRICAO , VALOR")
        with open('bets.txt', 'r') as f:
            today = time.strftime("%d/%m/%Y")
            print("Today = " + today)
            flag = False
            for line in f:
                print("line = " + line)
                if today in line:
                    flag = True
            with open('bets.txt', 'a+') as f:
                if flag == False:
                    if os.path.getsize('bets.txt') > 0:
                        f.write("\n\n")
                f.write(time.strftime("%d/%m/%Y") + "\n")
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
                #self.logger.info(url);
                yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
            '//ul[contains(@class,"pagination")]/li[7]//a/@href'
        ).extract_first()

        self.logger.info(next_page);

        if next_page:
            self.logger.info(next_page);
            self.log('Next Page: {0}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse_item)

    def parse_detail(self, response):
        leil = Leilao()
        leil['link'] = link = response.url
        leil['title'] = title = response.xpath('//div[contains(@class,"px-1")]//h4/text()').extract()
        leil['view'] = view = response.xpath('//div[contains(@class,"detalhes-lote")]/div/div[3]/div/div[5]/span/text()').extract()
        leil['valor'] = valor = response.xpath('//div[contains(@class,"detalhes-lote")]/div/div[3]/div/div/h3[1]/text()').extract()

        # leil['leilao'] = time.strftime("%d/%m/%Y, %H:%M:%S")

        leil['leilao'] = 'www'


        alphabet = response.xpath('//div[contains(@class,"px-1")]//h4/text()').extract()

        #auction = response.xpath('//div[contains(@class,"text-center")]/span/i/text()').extract()

        #VOLKSWAGEN/SPACEFOX - K*****5 - 2008 - 2009 - ALC/GAS

        data = alphabet[0].split("-")

       # self.logger.info(time.strftime("%d/%m/%Y, %H:%M:%S"))

        for temp in data:
            print
            temp

       # self.logger.info(u'catalogo URL: {0}'.format(response.url))
       # self.logger.info('Título: {0}'.format(title))
       # self.logger.info('Views: {0}'.format(view))
       #  self.logger.info('valor: {0}'.format(valor))

        return leil


class Leilao(scrapy.Item):
    link = scrapy.Field()
    leilao = scrapy.Field()
    timestamp = scrapy.Field()
    spider = scrapy.Field()
    uid = scrapy.Field()
    lote = scrapy.Field()
    title = scrapy.Field()
    view = scrapy.Field()
    valor = scrapy.Field()
    last_updated = scrapy.Field()








