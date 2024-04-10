import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


# First page of fountain pens
class PensSpider(CrawlSpider):
    name = 'pens'
    allowed_domains = ['gouletpens.com']
    start_urls = ['https://www.gouletpens.com/collections/all-fountain-pens']

    rules = (
        Rule(LinkExtractor(allow=(r"product",)), callback="parse_product"),
    )

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'pens_first_page.csv',
        'DOWNLOAD_DELAY': 0.2   
    }

    def parse_product(self, response):
        yield {
            "product_title": response.css('h1.product-info__title > span::text')[1].get(),
            "product_id": response.css('div.product-meta__sku > p > span::text').get(),
            "product_price": response.css('div.product-price > span::text').get().replace('$', ''),
            "product_rating": response.css('span.stamped-badge::attr(data-rating)').get(),
            "product_colors": response.css('div.sw-list a::attr(aria-label)').getall(),
            "product_site": 'gouletpens.com'
        }


# All pages of fountain pens
class SecondPensSpider(scrapy.Spider):
    name = 'more_pens'
    allowed_domains = ['gouletpens.com']
    start_urls = ['https://www.gouletpens.com/collections/all-fountain-pens']

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'pens_all_pages.csv',
        'DOWNLOAD_DELAY': 0.5
    }

    def parse(self, response):
        # Extract links to each product card on the current page
        product_card_links = response.css('a.boost-pfs-filter-product-item-image-link.boost-pfs-filter-crop-image-position-none::attr(href)').getall()
        for product_link in product_card_links:
            yield scrapy.Request(response.urljoin(product_link), callback=self.parse_product)

        # Handle pagination
        next_page_partial_url = response.css('link[rel="next"]::attr(href)').get()
        if next_page_partial_url:
            next_page_url = response.urljoin(next_page_partial_url)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_product(self, response):
        # Extract detailed product information
        yield {
            "product_title": response.css('title::text').get(),
            "product_id": response.css('div.product-meta__sku > p > span::text').get(),
            "product_price": response.css('div.product-price > span::text').get().replace('$', ''),
            "product_rating": response.css('span.stamped-badge::attr(data-rating)').get(),
            "product_colors": response.css('div.sw-list a::attr(aria-label)').getall(),
            "product_site": 'gouletpens.com'
        }