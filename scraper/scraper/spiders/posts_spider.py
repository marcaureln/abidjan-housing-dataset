import re
import scrapy
import tomli
import mysql.connector


class PostsSpider(scrapy.Spider):
    """Spider to crawl post details from listing website."""
    name = 'posts'
    start_urls = []

    def __init__(self):
        super().__init__()
        with open("scraper.toml", mode="rb") as config_file:
            self.config = tomli.load(config_file)

        connection = mysql.connector.connect(
            host=self.config["database"]["host"],
            user=self.config["database"]["user"],
            password=self.config["database"]["password"],
            database=self.config["database"]["name"]
        )

        cursor = connection.cursor()
        cursor.execute("SELECT link FROM houses")
        links = cursor.fetchall()

        self.start_urls = [link[0] for link in links]

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
        }

    def remove_html(self, string):
        """Remove HTML tags from a given string"""
        pattern = re.compile('<.*?>')
        try:
            return re.sub(pattern, ' ', string).strip()
        except Exception:  # Catch TypeError
            return None

    def get_tot_no_room(self, tot_no_room_string):
        """Parse and return the total number of rooms"""
        try:
            return int(tot_no_room_string)
        except Exception:  # Catch TypeError and ValueError
            return None

    def get_area(self, area_string):
        """Remove the unit (e.g.: m2) from the scraped area"""
        try:
            return float(re.search(r'\d+', area_string).group())
        except Exception:  # Catch TypeError and ValueError
            return None
