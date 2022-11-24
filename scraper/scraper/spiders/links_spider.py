'''Import scrapy - web scraping framework'''
import scrapy


class LinksSpider(scrapy.Spider):
    '''Spider to crawl posts links from listing website.'''
    name = 'links'
    start_urls = [
        'https://deals.jumia.ci/abidjan/appartements-a-vendre',
        'https://deals.jumia.ci/abidjan/maisons-a-vendre'
    ]

    def parse(self, response):
        # link_selector is relative to the current post element (.post)
        link_selector = 'div.text-area > div > div.announcement-infos > a::attr("href")'

        for post in response.css('.post'):
            yield {
                'link': post.css(link_selector).get()
            }

        next_page_selector = '#tab1 > nav > ul > li.next > a::attr("href")'
        next_page = response.css(next_page_selector).get()

        if next_page is not None:
            yield response.follow(next_page, self.parse)
