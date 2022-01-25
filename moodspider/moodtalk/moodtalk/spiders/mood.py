import logging
import scrapy
#from moodspider.moodtalk.moodtalk.items import MoodtalkItem
from moodspider import models as moodtalk_models


class MoodSpider(scrapy.Spider):
    name = 'mood'
    allowed_domains = ['mingyanjiaju.org']
    start_urls = ['https://mingyanjiaju.org/juzi/yingyumingyan/2015/0516/932.html']

    # 處理網址的部分
    def start_request(self, response):
        url = 'https://mingyanjiaju.org/juzi/yingyumingyan/2015/0516/932.html'
        yield scrapy.Request(url,callback=self.parse)

    def parse(self,response):
        #item = MoodtalkItem()
        sentence_list = response.xpath('//div[@class="text01"]/div[@class="textCont"]/p')
        for i in range(1, len(sentence_list),2):
            sentence = sentence_list[i].xpath(".//text()").get()
            moodtalk = moodtalk_models.Moodtalk(sentence = sentence)
            moodtalk.save()

#if __name__ == '__main__':