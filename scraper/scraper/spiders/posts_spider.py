'''Import scrapy - web scraping framework'''
from os import path
import re
import csv
import scrapy


class PostsSpider(scrapy.Spider):
    '''Spider to craw posts links from listing website.'''
    name = 'posts'
    start_urls = []

    def __init__(self, links, base_url='https://deals.jumia.ci'):
        super().__init__()
        spyder_script_dir = path.dirname(__file__)
        abs_file_path = path.normpath(
            path.join(spyder_script_dir, f"../../{links}"))
        with open(abs_file_path, mode='r', encoding='utf-8') as file:
            csv_file = csv.reader(file)
            self.start_urls = [base_url + line[0].strip() for line in csv_file]

    def parse(self, response):
        title_xpath = '//*[@id="main-holder"]/article/header/h1/span/text()'
        price_selector = '#priceSection > span > span:nth-child(1)::attr("content")'
        description_xpath = '//*[@id="main-holder"]/article/div[1]/div/div[3]/p/text()'
        tot_no_room_xpath = '//*[@id="main-holder"]/article/div[1]/div/div[2]/div/h3[1]/span/text()'
        area_xpath = '//*[@id="main-holder"]/article/div[1]/div/div[2]/div/h3[2]/span/text()'

        yield {
            'title': response.xpath(title_xpath).get().strip(),
            'description': self.escape_html(response.xpath(description_xpath).get()).strip(),
            'price': float(response.css(price_selector).get()),
            'tot_no_room': int(response.xpath(tot_no_room_xpath).get()),
            'area': self.get_area(response.xpath(area_xpath).get()),
        }

    def escape_html(self, string):
        '''Remove HTML tags from a given string'''
        pattern = re.compile('<.*?>')
        return re.sub(pattern, ' ', string)

    def get_area(self, area_string):
        '''Remove the unit (e.g.: m2) from the scraped area'''
        return float(re.search(r'\d+', area_string).group())
