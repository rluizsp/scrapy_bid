# -*- coding: utf-8 -*-
import scrapy


class WebmotorsSpider(scrapy.Spider):
    name = "webmotors"
    allowed_domains = ["webmotors.com.br"]
    first_page_url = ('https://www.webmotors.com.br/carros/sp/')

    def __init__(self, force_last_page=None):
        # Paramether force_last_page
        if force_last_page:
            self.force_last_page = int(force_last_page)

        self.last_page = None

    def start_requests(self):
        ''' Create request to first page '''
        request = scrapy.Request(
            url=WebmotorsSpider.first_page_url.format(1),
            callback=self.parse_page,
        )
        yield request

    def parse_page(self, response):
        '''
        Create requests to links of all pages
        and set the last page
        '''

        print(response)


        # get anchor link on "last page" button
        last_button_anchor = response.xpath('//*[contains(@id, "boxResultado")]/div/a/@href')[-1].extract()
        # get the last page from href
        self.last_page = int(last_button_anchor.split("p=")[-1])

        if self.force_last_page:
            self.last_page = self.force_last_page

        # page 1 to last page
        for page in range(1, self.last_page):
            request = scrapy.Request(
                url=WebmotorsSpider.first_page_url.format(page),
                callback=self.parse,
            )
            yield request

    def scrapy_link(self, response, links):
        ''' Extract the link '''
        link_items = response.xpath(
            '//*[contains(@id, "boxResultado")]/a/@href').extract()

        for l in link_items:
            try:
                links.append(l)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

    def scrapy_makermodel(self, response, makers, models):
        ''' Extract model and maker '''
        model_items = response.xpath(
            '//*[contains(@class,"make-model")]'
            '/text()').extract()

        for m in model_items:
            try:
                model_maker = m.split()
                maker = model_maker[0]
                model = " ".join(model_maker[1:])
                makers.append(maker)
                models.append(model)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

    def scrapy_price(self, response, prices):
        ''' Extract price '''
        prices_items = response.xpath(
            '//*[contains(@class,"price")]/text()').extract()

        for p in prices_items:
            try:
                clean_price = p.strip()
                if clean_price == '':
                    continue
                prices.append(clean_price)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

    def scrapy_image(self, response, images):
        ''' Extract image '''
        image_tags = response.xpath(
            '//*[contains(@id, "boxResultado")]//img'
            '/@data-original').extract()

        for i in image_tags:
            try:
                images.append(i)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

    def scrapy_city(self, response, cities):
        ''' Extract city '''
        city_tags = response.xpath(
            '//*[contains(@class,"card-footer")]'
            '/span[1]/text()').extract()

        for city in city_tags:
            try:
                cities.append(city)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

    def scrapy_yearmaker(self, response, yearmakers):
        ''' Extract yearMaker '''
        yearmaker_tags = response.xpath(
            '//*[contains(@class,"features")]/div[1]/span[1]/text()').extract()

        for yearmaker in yearmaker_tags:
            try:
                yearmakers.append(yearmaker)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

    def scrapy_color(self, response, colors):
        ''' Extract color '''
        color_tags = response.xpath(
            '//*[contains(@class,"features")]/div[1]/span[2]/text()').extract()

        for color in color_tags:
            try:
                colors.append(color)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

    def scrapy_km(self, response, kms):
        ''' Extract Km '''
        km_tags = response.xpath(
            '//*[contains(@class,"features")]/div[2]/span[1]/text()').extract()

        for km in km_tags:
            try:
                kms.append(km)
            except ValueError as e:
                print("URL {}, error : {}".format(response.url, e))
                return
            except Exception as e:
                print("URL {}, generic error : {}".format(response.url, e))
                return

    def parse(self, response):
        """Parse all information to CarItem"""

        links = []
        self.scrapy_link(response, links)

        makers = []
        models = []
        self.scrapy_makermodel(response, makers, models)

        prices = []
        self.scrapy_price(response, prices)

        images = []
        self.scrapy_image(response, images)

        cities = []
        self.scrapy_city(response, cities)

        yearmakers = []
        self.scrapy_yearmaker(response, yearmakers)

        colors = []
        self.scrapy_color(response, colors)

        kms = []
        self.scrapy_km(response, kms)

        # If size of lists is not equal something wrong
        if len(prices) == len(models) == len(makers) == len(images):
            size = len(prices)
            for i in range(0, size):
                car = CarItem()
                car['link'] = links[i]
                car['maker'] = makers[i]
                car['model'] = models[i]
                car['price'] = prices[i]
                car['image'] = images[i]
                car['city'] = cities[i]
                # state
                car['yearmaker'] = yearmakers[i]
                # yearModel
                car['km'] = kms[i]
                car['color'] = colors[i]
                # version
                # search
                # searchoriginal
                # idsite
                # iduser
                # contact_name
                # contact_email
                # contact_phone
                # description
                yield car
        else:
            error_message = ("Error with size of lists: prices={}, "
                             "models={}, makers={}, images={}")
            print(error_message.format(len(prices), len(
                models), len(makers), len(images)))




class CarItem(scrapy.Item):
    link = scrapy.Field()
    model = scrapy.Field()
    maker = scrapy.Field()
    price = scrapy.Field()
    image = scrapy.Field()
    city = scrapy.Field()
    yearmaker = scrapy.Field()
    color = scrapy.Field()
    km = scrapy.Field()