'''Import scrapy, os.path, re (regex) and csv'''
from os import path
import re
import csv
import scrapy


class PostsSpider(scrapy.Spider):
    '''Spider to crawl post details from listing website.'''
    name = 'posts'
    # TODO: Load start_urls from database
    start_urls = []

    # TODO: Move base_url to config file
    def __init__(self, links, base_url='https://deals.jumia.ci'):
        super().__init__()
        spider_dir = path.dirname(__file__)
        file_path = path.normpath(path.join(spider_dir, f"../../{links}"))
        with open(file_path, mode='r', encoding='utf-8') as file:
            csv_file = csv.reader(file)
            self.start_urls = [base_url + line[0].strip() for line in csv_file]

    def parse(self, response):
    # TODO: Move selectors to config file
        title_xpath = '//*[@id="main-holder"]/article/header/h1/span/text()'
        price_selector = '#priceSection > span > span:nth-child(1)::attr("content")'
        location_xpath = '//*[@id="priceSection"]/div/dl/dd[2]/span/text()'
        pub_date_selector = '#priceSection > div > dl > dd:nth-child(6) > time::attr("datetime")'
        description_xpath = '//*[@id="main-holder"]/article/div[1]/div/div[3]/p'
        tot_no_room_xpath = '//*[@id="main-holder"]/article/div[1]/div/div[2]/div/h3[1]/span/text()'
        area_xpath = '//*[@id="main-holder"]/article/div[1]/div/div[2]/div/h3[2]/span/text()'

        yield {
            'title': response.xpath(title_xpath).get(),
            'description': self.remove_html(response.xpath(description_xpath).get()),
            'price': float(response.css(price_selector).get()),
            'tot_no_room': self.get_tot_no_room(response.xpath(tot_no_room_xpath).get()),
            'area': self.get_area(response.xpath(area_xpath).get()),
            'location': response.xpath(location_xpath).get(),
            'pub_date': response.css(pub_date_selector).get(),
            'link': response.url,
            'from': response.css('title').get()
        }

    def remove_html(self, string):
        '''Remove HTML tags from a given string'''
        pattern = re.compile('<.*?>')
        try:
            return re.sub(pattern, ' ', string).strip()
        except Exception:  # Catch TypeError
            return None

    def get_tot_no_room(self, tot_no_room_string):
        '''Parse and return the total number of rooms'''
        try:
            return int(tot_no_room_string)
        except Exception:  # Catch TypeError and ValueError
            return None

    def get_area(self, area_string):
        '''Remove the unit (e.g.: m2) from the scraped area'''
        try:
            return float(re.search(r'\d+', area_string).group())
        except Exception:  # Catch TypeError and ValueError
            return None
