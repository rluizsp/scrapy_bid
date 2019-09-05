# -*- coding: utf-8 -*-
import scrapy


class WebmotorsSpider2(scrapy.Spider):
    name = "webmotors2"
    allowed_domains = ["webmotors.com.br"]
    start_urls = (
        'https://www.webmotors.com.br/carros/sp/',
    )


    # https://www.webmotors.com.br/carros/sp/land-rover/range-rover-evoque/20-dynamic-4wd-16v-gasolina-4p-automatico/de.2012/ate.2012?estadocidade=S%C3%A3o%20Paulo&tipoveiculo=carros&anoate=2012&anode=2012&marca1=LAND%20ROVER&modelo1=RANGE%20ROVER%20EVOQUE&versao1=2.0%20DYNAMIC%204WD%2016V%20GASOLINA%204P%20AUTOM%C3%81TICO

    def parse(self, response):

        items = response.xpath('//div[@class="WhiteBox WhiteBox--card-vehicle "]')

        print(items)

        for item in items:
            url = item.xpath("/div/a/@href").extract_first()
            name = item.xpath("/div/a/div/div/h2/text()").extract_first()

            print(name)

            # yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
            '//li[contains(@class,"item next")]//a/@href'
        ).extract_first()
        if next_page:
            self.log('Next Page: {0}'.format(next_page))
            # yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        self.log(u'Imóvel URL: {0}'.format(response.url))
        title = response.xpath('normalize-space(//h1[contains(@id,"ad_title")]//.)').extract_first()
        self.log(u'Título: {0}'.format(title))




