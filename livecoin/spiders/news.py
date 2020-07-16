# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['www.livecoin.net/en/news/list']

    script = '''
        function main(splash, args)
          splash.private_mode_enabled = false
          splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0")
          url = args.url
          assert(splash:go(url))
          assert(splash:wait(1))
          splash:set_viewport_full()
          return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='http://www.livecoin.net/en/news/list/', callback=self.parse, endpoint="execute", args={
            'lua_source': self.script
        })

    def parse(self, response):
        for currency in response.xpath("//div[contains(@class, 'news_item')]"):
            yield {
                'date_news': currency.xpath("normalize-space(.//div/text())").get(),
                'headline_news': currency.xpath(".//h2/a/text()").get(),
                'entry_news': currency.xpath("normalize-space(string(string(.//div[@class='short_text'])))").get()

            }
