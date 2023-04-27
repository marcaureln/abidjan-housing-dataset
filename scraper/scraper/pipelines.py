# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector
import tomli


class ScraperPipeline:
    '''Scrapy Item Pipeline: https://docs.scrapy.org/en/latest/topics/item-pipeline.html'''

    def __init__(self):
        with open("scraper.toml", mode="rb") as config_file:
            self.config = tomli.load(config_file)

        self.conn = mysql.connector.connect(
            host=self.config["database"]["host"],
            user=self.config["database"]["user"],
            password=self.config["database"]["password"],
            database=self.config["database"]["name"]
        )

        # Create cursor, used to execute commands
        self.cur = self.conn.cursor()

        # Create houses table if none exists
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
            link text unique,
            from text,
            created_at DATE,
            updated_at DATE,
            PRIMARY KEY (house_id)
        )
        """)

    def process_item(self, item, spider):
        '''Load items into database.
        This method is called for every item pipeline component.'''
        ## Check to see if text is already in database 
        self.cur.execute("select * from houses where link = %s", (item['link'],))
        result = self.cur.fetchone()

        ## If it is in DB, create log message
        if result:
            spider.logger.warn("Item already in database: %s" % item['link'])
            
        else:
            if spider.name == "links":
                
                # TODO: Insert links and website name into database (prevent items from inserting twice)
                # self.cur.execute("""INSERT INTO houses (title, description, price, tot_no_room, area, location, pub_date, link) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", (
                # item["title"],
                # ))
                
                self.cur.execute("""INSERT INTO houses (link, from) VALUES (%s,%s)""", (
                item["title"],
                item["from"],
                ))
            elif spider.name == "posts":
                # TODO: Update houses table with new data
                # self.cur.execute("""INSERT INTO houses (title, description, price, tot_no_room, area, location, pub_date, link) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", (
                #     item["title"],
                #     item["description"],
                #     item["price"],
                #     item["tot_no_room"],
                #     item["area"],
                #     item["location"],
                #     item["pub_date"],
                #     item["link"],
                # ))
    
                self.cur.execute("""
                                    UPDATE houses
                                    SET title = %s, 
                                        description = %s,
                                        price = %s,
                                        tot_no_room = %s,
                                        area = %s,
                                        location = %s,
                                        pub_date = %s,
                                    WHERE link = %s
                                    """
                                ,(
                    item["title"],
                    item["description"],
                    item["price"],
                    item["tot_no_room"],
                    item["area"],
                    item["location"],
                    item["pub_date"],
                    item["link"],
                ))
                self.conn.commit()
            else:
                raise ValueError("Invalid spider name!")

    def close_spider(self, spider):
        '''Close cursor and database's connection. 
        This method is called when the spider is closed.'''
        self.cur.close()
        self.conn.close()
