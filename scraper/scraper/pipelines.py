import sys

import mysql.connector
import tomli


class ScraperPipeline:
    """Scrapy Item Pipeline: https://docs.scrapy.org/en/latest/topics/item-pipeline.html"""

    def __init__(self):
        with open("scraper.toml", mode="rb") as config_file:
            self.config = tomli.load(config_file)

        self.conn = mysql.connector.connect(
            host=self.config["database"]["host"],
            user=self.config["database"]["user"],
            password=self.config["database"]["password"],
            database=self.config["database"]["name"]
        )

        try:
            self.cur = self.conn.cursor()
            self.cur.execute("""
                       CREATE TABLE IF NOT EXISTS houses(
                           house_id INT NOT NULL AUTO_INCREMENT,
                           title VARCHAR(255),
                           link VARCHAR(768),
                           description TEXT,
                           price INT,
                           tot_no_room INT,
                           area TEXT,
                           location TEXT,
                           pub_date VARCHAR(255),
                           link VARCHAR(768),
                           website TEXT,
                           created_at DATE,
                           updated_at DATE,
                           PRIMARY KEY (house_id),
                           UNIQUE INDEX unique_link USING HASH (link)
                       );
                       """)
        except mysql.connector.Error as e:
            print("Error while connecting to MySQL", e)
            sys.exit(1)

    def process_item(self, item, spider):
        """
        Load items into database.
        This method is called for every item pipeline component.
        """
        if spider.name == "links":
            self.cur.execute("""INSERT IGNORE INTO houses (link) VALUES (%s)""", (item["link"],))
            self.conn.commit()
        elif spider.name == "posts":
            self.cur.execute(
                """UPDATE houses
                SET title = %s, description = %s, price = %s, tot_no_room = %s, area = %s, location = %s, pub_date = %s
                WHERE link = %s
                """,
                (
                    item["title"],
                    item["description"],
                    item["price"],
                    item["tot_no_room"],
                    item["area"],
                    item["location"],
                    item["pub_date"],
                    item["link"],
                )
            )
            self.conn.commit()
        else:
            raise ValueError("Invalid spider name!")

    def close_spider(self, _):
        """
        Close cursor and database's connection.
        This method is called when the spider is closed.
        """
        self.cur.close()
        self.conn.close()
