# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PensItem(scrapy.Item):
    product_title = scrapy.Field()
    product_id = scrapy.Field()
    product_price = scrapy.Field()
    product_rating = scrapy.Field()
    product_colors = scrapy.Field()
    product_site = scrapy.Field()

