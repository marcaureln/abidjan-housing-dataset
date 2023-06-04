"""Import scrapy - web scraping framework"""
from pathlib import Path
import scrapy
import tomli


class LinksSpider(scrapy.Spider):
    """Spider to crawl posts links from listing website."""
    name = 'links'
    base_url = ''
    start_urls = []

    # TODO: Move base_url to config file
    # TODO: Write a function to get config

    def __init__(self, base_url='https://deals.jumia.ci'):
        super().__init__()
        config_file_path = Path("scraper.toml").resolve()
        with open(config_file_path, mode="rb") as config_file:
            config = tomli.load(config_file)

        self.start_urls = config["start_urls"]["links"]
        self.base_url = base_url

    def parse(self, response):
        config_file_path = Path("scraper.toml").resolve()
        with open(config_file_path, mode="rb") as config_file:
            config = tomli.load(config_file)

        # link_selector is relative to the current post element (.post)
        # TODO: Loop through ["selectors"]["links"]
        link_selector = config["selectors"]["links"][0]["link"]

        for post in response.css('.post'):
            yield {
                'name': config["selectors"]["links"][0]["name"],
                'link': self.base_url + post.css(link_selector).get()
            }

        next_page_selector = config["selectors"]["links"][0]["next_page"]
        next_page = response.css(next_page_selector).get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)
