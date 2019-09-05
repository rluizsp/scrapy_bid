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
            url = catalog.xpath(".//a/@href").extract_first()
            self.log(catalog)

            if validators.url(url):
                self.logger.info("catalog: "+url);
                yield scrapy.Request(url=url, callback=self.parse_item)

    def parse_item(self, response):
        items = response.xpath('//div[@class="lote rounded"]')

        for item in items:
            #
            url = item.xpath("./div/div[3]/div/a/@href").extract_first()
            bid = Bid()
            bid['item_description'] = item.xpath('normalize-space(//div[contains(@class,"body-lote")]/a/p/text()[2])').extract_first()
            # bid['bid_name'] = item.xpath('//div[contains(@class,"body-lote")]//a/div/img').extract_first()
            bid['bid_name'] = response.url
            item_name = item.xpath('normalize-space(./div/div[2]/div/a/p/text()[2])').extract_first()
            bid['item_description'] = item.xpath('normalize-space(./div/div[2]/div/a/p/span/text())').extract_first()
            # # ttimestamp'] =
            bid['item_model_desc'] = item.xpath('./div/div[2]/div/a/p/text()[2]').extract_first()
            bid['item_model_year'] = item.xpath('./div/div[2]/div/a/p/text()[5]').extract_first()
            item_made_year = item.xpath('normalize-space(./div/div[2]/div/a/p/text()[5])').extract_first()
            bid['item_url'] = url
            bid['item_color'] = item.xpath('./div/div[2]/div/a/p/text()[6]').extract_first()
            bid['item_fuel'] = item.xpath('./div/div[2]/div/a/p/text()[7]').extract_first()
            bid['item_km'] = item.xpath('./div/div[2]/div/a/p/text()[8]').extract_first()
            bid['item_local'] = item.xpath('./div/div[2]/div/a/p/strong/text()').extract_first()
            bid['item_tax'] = item.xpath('./div/div[2]/div/a/table/tbody/tr/td[1]/p/text()').extract_first()
            bid['item_documentation'] = item.xpath('./div/div[2]/div/a/p/strong[2]').extract_first()
            bid['item_view_count'] = '0'
            #

            item_price = item.xpath('normalize-space(./div/div[3]/div/a/div[2]/text())').extract_first()

            try:
                numexp = re.compile(r'[-]?\d[\d,]*[\.]*[\,]?[\d{2}]*')  # optional - in front
                numbers = numexp.findall(item_price)
                numbers = [x.replace('.', '') for x in numbers]

                bid['item_price'] = numbers[0] + "." + numbers[1]




            except IndexError:
                bid['item_price'] = 0

            try:
                data = item_name.split("/")
                bid['item_name'] = data[0]
                bid['item_model_desc'] = data[1]

            except IndexError:
                bid['item_name'] = 0
                bid['item_model_desc'] = 0

            try:
                numexpp = re.compile(r'[-]?\d[\d,]*[\]?[\d{2}]*')  # optional - in front
                numbersp = numexpp.findall(str(item_made_year))

                bid['item_made_year'] = numbersp[0]
                bid['item_model_year'] = numbersp[1]

            except IndexError:
                bid['item_made_year'] = 0
                bid['item_model_year'] = 0

            yield bid

            # Call show details from the new page
            #if validators.url(url):
                # self.logger.info(url);
                # yield scrapy.Request(url=url, callback=self.parse_detail)

        arr_next_page = response.xpath('//div[@class="lista-lotes"]/div[2]/ul/li/a/@href').extract()

        try:
            next_page = str(arr_next_page[len(arr_next_page) - 1])
            print(next_page)

        except IndexError:
            next_page = ""


        # self.logger.info("next_page",next_page)

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

        numexp = re.compile(r'[-]?\d[\d,]*[\.]*[\,]?[\d{2}]*')  # optional - in front
        numbers = numexp.findall(str(item_price))

        numbers = [x.replace(',', '') for x in numbers]
        s = '.'
        s.join(numbers)
        print(s)

        bid['item_price'] = s
        bid['bid_name'] = 'guariglialeiloes'

        alphabet = response.xpath('//div[contains(@class,"px-1")]//h4/text()').extract()

        data = alphabet[0].split("-")

        return bid


class Bid(scrapy.Item):
    uid = scrapy.Field()
    spider = scrapy.Field()
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
    item_color = scrapy.Field()
    item_fuel = scrapy.Field()
    item_km = scrapy.Field()
    item_local = scrapy.Field()
    item_tax = scrapy.Field()
    item_documentation = scrapy.Field()


