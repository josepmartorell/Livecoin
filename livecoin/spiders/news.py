# -*- coding: utf-8 -*-
import scrapy


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.livecoin.net']

    def start_requests(self):
        yield scrapy.Request(url='http://www.livecoin.net/en/news/list/', callback=self.parse, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/76.0.3809.100 Safari/537.36 '
        })

    def parse(self, response):
        for currency in response.xpath("//div[contains(@class, 'news_item')]"):
            yield {
                'date_news': currency.xpath("normalize-space(.//div/text())").get(),
                'headline_news': currency.xpath(".//h2/a/text()").get(),
                'entry_news': currency.xpath("normalize-space(string(string(.//div[@class='short_text'])))").get()

            }

        next_page = response.xpath(
            './/li[@class=" active"]/following-sibling::li[1]/a/@href').extract_first()

        if next_page is not None:
            yield response.follow(url=next_page,
                                  callback=self.parse)
