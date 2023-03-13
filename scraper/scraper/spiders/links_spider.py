'''Import scrapy - web scraping framework'''
import os
import scrapy
import tomli

class LinksSpider(scrapy.Spider):
    '''Spider to crawl posts links from listing website.'''
    name = 'links'

    #TODO: Create a load config function to load config file
    config_file = open(os.path.abspath("scraper/scraper.toml"), 'rb')
    config = tomli.load(config_file)
    print(config)        

    start_urls = config["start_urls"]["links"]

    def parse(self, response):
        with open("/scraper.toml", mode="r") as config_file:
            config = tomli.load(config_file)

        # link_selector is relative to the current post element (.post)
        link_selector = config["selectors"]["links"]["link"]

        for post in response.css('.post'):
            yield {
                'link': post.css(link_selector).get()
            }

        next_page_selector = config["selectors"]["links"]["next_page"]
        next_page = response.css(next_page_selector).get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)
