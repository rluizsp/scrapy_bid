# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import psycopg2

class ScrapyBidPipeline(object):
    def open_spider(self, spider):
        hostname = 'localhost'
        username = 'postgres'
        password = 'hexenii7'  # your password
        database = 'cars'
        self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
        self.cur = self.connection.cursor()

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        self.cur.execute("insert into bid_cars(item_name,item_description) values(%s,%s)", (item['title'], item['valor']))
        self.connection.commit()
        return item




    # insert
    # into
    # bid_cars(bid_name, item_name, item_price, item_description, ttimestamp, item_model_desc, item_model_year,
    #          item_made_year, item_url, item_view_count)
    # VALUES
    # ('guariglia', 'carro', 123.32, 'motor zuado', CURRENT_TIMESTAMP, 'monza', 2018, 2017, 'www', 10)

