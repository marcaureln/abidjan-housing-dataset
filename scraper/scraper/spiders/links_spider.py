'''Import scrapy - web scraping framework'''
import scrapy


class LinksSpider(scrapy.Spider):
    '''Spider to craw posts links from listing website.'''
    name = 'links'
    start_urls = [
        'https://deals.jumia.ci/abidjan/appartements-a-vendre',
        'https://deals.jumia.ci/abidjan/maisons-a-vendre'
    ]

    def parse(self, response):
        for post in response.css('.post'):
            yield {
                'link': post.css(
                    'div.text-area > div > div.announcement-infos > a::attr("href")'
                ).get()
            }

        next_page = response.css(
            '#tab1 > nav > ul > li.next > a::attr("href")'
        ).get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)
