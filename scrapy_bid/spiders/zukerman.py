# -*- coding: utf-8 -*-
import scrapy


class ZukermanSpider(scrapy.Spider):
    name = 'zukerman'
    allowed_domains = ['zukerman.com.br']
    start_urls = ['https://www.zukerman.com.br/imoveis-residenciais']

    def parse(self, response):
        items = response.xpath(
            '//div[contains(@class,"cd-it-img")]'
        )

        for item in items:
            url = item.xpath(
                ".//a/@href"
            ).extract_first()
            self.log(item)
            yield scrapy.Request(url=url, callback=self.parse_detail)

        next_page = response.xpath(
            '//link[contains(@rel,"next")]/@href'
        ).extract_first()

        self.logger.info('next_page: {0}'.format(next_page))

        if next_page:
            self.log('Next Page: {0}'.format(next_page))
            yield scrapy.Request(url=next_page, callback=self.parse)

    def parse_detail(self, response):
        title   = response.xpath('//div[contains(@class,"s-d-l-m")]//h1/text()').extract()
        auction = response.xpath('//div[contains(@class,"m-l-o")]/text()').extract()
        view    = response.xpath('//div[contains(@class,"s-d-lf-na")]/text()').extract()
        status  = response.xpath('//div[contains(@class,"s-d-lb2")]/text()').extract()
        round_one_value = response.xpath('//span[contains(@class,"dvlf")]/text()').extract()
        round_one_date = response.xpath('//span[contains(@class,"dvlf")]//div/text()').extract()


        round_two_value = response.xpath('//span[contains(@class,"dvla")]/text()').extract()
        round_two_date = response.xpath('//span[contains(@class,"dvla")]//div/text()').extract()

        address = response.xpath('//div[contains(@class,"s-d-ld-i-main")]//div/text()').extract()
        info = response.xpath('//div[contains(@class,"s-d-ld-i3")]').extract()
        desc = response.xpath('//div[contains(@class,"s-d-ld-i1")]').extract()
        bid_desc = response.xpath('//div[contains(@class,"s-d-il-i-main")]').extract()



        self.logger.info(u'Imóvel URL: {0}'.format(response.url))
        self.logger.info(u'auction: {0}'.format(auction))
        self.logger.info('Título: {0}'.format(title))
        self.logger.info('Views: {0}'.format(view))
        self.logger.info('Status: {0}'.format(status))
        self.logger.info('round_one_value: {0}'.format(round_one_value))
        self.logger.info('round_one_date: {0}'.format(round_one_date))

        self.logger.info('round_two_value: {0}'.format(round_two_value))
        self.logger.info('round_two_date: {0}'.format(round_two_date))

        self.logger.info('address: {0}'.format(address))
        self.logger.info('info: {0}'.format(info))
        self.logger.info('desc: {0}'.format(desc))
        self.logger.info('bid_desc: {0}'.format(bid_desc))



        #round_one_value = response.xpath('//span[contains(@class,"dvlf")]/.').extract()
        #round_one_date = response.xpath('//div[contains(@class,"daet")]/text()').extract()
        #self.logger.info('round_one_value: {0}'.format(round_one_value))
        #self.logger.info('round_one_date: {0}'.format(round_one_date))

        auction_name
        auction_domains

        auction_start_date
        auction_initial_price
        auction_increment
        auction_actual_close_date
        auction_planned_close_date
        auction_successful_bidder
        auction_conclusion_mode
        auction_comments






















        #
        # # Documentation
        # auction_documents
        #
        # # Bid
        # auction_bid_number
        # auction_bid_date
        # auction_bid_price
        # auction_bid_comments
        #
        # # Bidders
        # auction_bidder_id
        # auction_bidder_name
        # auction_bidder_address
        # auction_bidder_email
        # auction_bidder_phone
        # auction_bidder_credit_details
        #
        # # Status
        # status_code
        # status_description
        #
        # # Round n
        # auction_start_date_round_one
        # auction_start_price_round_one
        #
        # auction_start_date_round_two
        # auction_start_price_round_two
        #
        # auction_start_date_round_three
        # auction_start_price_round_three
        #
        # # Item information
        # item_id
        # item_description
        # item_category_code
        # item_category_description
        #
        # # Legal Detail
        # item_legal_process_number
        # item_legal_observation
        #
        # # Register Detail
        # item_register_number
        # item_register_size
        # item_in_use
        #
        # # Registry of item - Address
        # item_registry_address_country
        # item_registry_address_state
        # item_registry_address_city
        # item_registry_address_neighbourhood
        # item_registry_address_zipcode
        #
