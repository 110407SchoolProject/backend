# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymysql.converters import encoders
from itemadapter import ItemAdapter
import pymysql
from moodtalk import settings

class MoodtalkPipeline:
    def __init__(self) -> None:
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DATABASE,
            user=settings.MYSQL_USERNAME,
            passwd=settings.MYSQL_PASSWORD,
            charset='utf-8-sig',
        )

        self.cursor = self.connect.cursor()
    

    def process_item(self, item, spider):
        sql = 'INSERT (sentence)VALUES(%s) INTO moodspider_moodtalk'
        data = (item['sentence'])
        self.cursor.execute(sql, data)
        return item
    
    def close_spider(self, spider):
        self.connect.commit()
        self.connect.close()

