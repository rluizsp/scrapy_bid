# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass

    # -*- coding: utf-8 -*-
    import scrapy

    class ZukermanSpider(scrapy.Spider):
        name = 'zukerman'
        allowed_domains = ['zukerman.com.br']
        start_urls = ['https://www.zukerman.com.br/imoveis-residenciais']

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

                next_page = response.xpath(
                    '//link [contains(@rel,"next")]@href'
                ).extract_first()
                if next_page:
                    self.log('Next Page: {0}'.format(next_page))
                    yield scrapy.Request(url=next_page, callback=self.parse)

            def parse_detail(self, response):
                self.log(u'Imóvel URL: {0}'.format(response.url))
            # title = response.xpath('//div[contains(@class,"s-d-l-m")]//normalize-space(//h1//.)')
            # self.log(u'Título: {0}'.format(title))



