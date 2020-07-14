# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3


class SQLitePipeline(object):
    def open_spider(self, spider):
        # todo -1/CONNECTION: create connection ('A new file called “livecoin.db” will be created where our database
        #  will be stored').
        self.connection = sqlite3.connect("livecoin.db")
        # todo -2/CURSOR: To execute SQLite statements in Python, you need a cursor object.
        #  You can create it using the cursor () method.
        self.cursor = self.connection.cursor()
        # todo -3/EXECUTE: Using the cursor object, execute method is executed with CREATE TABLE query as parameter
        try:
            self.cursor.execute('''
                CREATE TABLE coin_rates(
                    currency_pair TEXT,
                    volume_24h TEXT,
                    Last_price TEXT,
                    Change_24h TEXT,
                    High_24h TEXT,
                    Low_24h TEXT
                )

            ''')
            # todo -4/COMMIT: The commit () method saves all the changes we make.
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        # todo -5/CLOSE: Finally the close () method closes the connection.
        self.connection.close()

    def process_item(self, item, spider):
        # todo -1/EXECUTE: Using the cursor object, execute method is executed with INSERT INTO query as parameter
        self.cursor.execute('''
            INSERT INTO coin_rates (currency_pair, volume_24h, Last_price, Change_24h, High_24h, Low_24h) VALUES(?,?,?,?,?,?)
        ''', (
            item.get('currency_pair'),
            item.get('volume_24h'),
            item.get('Last_price'),
            item.get('Change_24h'),
            item.get('High_24h'),
            item.get('Low_24h')
        ))
        # todo -2/COMMIT: The commit () method saves all the changes we make.
        self.connection.commit()
        return item
