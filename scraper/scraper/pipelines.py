# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import tomli

class ScraperPipeline:
    def __init__(self):
        with open("../scraper.toml", mode="r") as config_file:
            self.config = tomli.load(config_file)
            print(self.config)

        self.conn = mysql.connector.connect(
            host = self.config["database"]["host"],
            user = self.config["database"]["user"],
            password = self.config["database"]["password"],
            database = self.config["database"]["name"]
        )
        
        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create houses table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS houses(
            house_id int NOT NULL auto_increment,
            title VARCHAR(255),
            description text,
            price float,
            tot_no_room int,
            area text,
            location text,
            pub_date VARCHAR(255),
            link text,
            PRIMARY KEY (house_id)
        )
        """)
    
    def process_item(self, item, spider):
        ## Define insert statement
        self.cur.execute("""insert into houses (title, description, price, tot_no_room, area, location, pub_date, link) values (%s,%s,%s,%s,%s,%s,%s,%s)""", (
            item["title"],
            item["description"],
            item["price"],
            item["tot_no_room"],
            item["area"],
            item["location"],
            item["pub_date"],
            item["link"],
        ))

        ## Execute insert of data into database
        self.conn.commit()

    
    def close_spider(self, spider):
        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()