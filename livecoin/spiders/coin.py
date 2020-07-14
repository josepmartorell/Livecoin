# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class CoinSpider(scrapy.Spider):
    name = 'coin'
    allowed_domains = ['www.livecoin.net']

    base_category_url = "https://www.livecoin.net"

    start_url_dict = {
        u"market": "/en",
        u"news": "/en/news/list",
        u"fees_and_limits": "/en/fees",
        u"exchange_services": "/en/partners"

    }

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
        for k, v in self.start_url_dict.items():
            for i in range(4):
                url = self.base_category_url + v
                yield SplashRequest(url, callback=self.parse, meta={'category': k}, endpoint="execute", args={
                    'lua_source': self.script

                })

    def parse(self, response):
        for currency in response.xpath("//div[contains(@class, 'ReactVirtualized__Table__row tableRow___3EtiS ')]"):
            yield {
                'currency_pair': currency.xpath(".//div[1]/div/text()").get(),
                'volume_24h': currency.xpath(".//div[2]/span/text()").get(),
                'Last_price': currency.xpath(".//div[3]/span/text()").get(),
                'Change_24h': currency.xpath(".//div[4]/span/span/text()").get(),
                'High_24h': currency.xpath(".//div[5]/span/text()").get(),
                'Low_24h': currency.xpath(".//div[6]/span/text()").get(),
                'partners_name': currency.xpath(".//div/h1/a/text()").get(),
                'partner_info': currency.xpath(".//div/text()")[1].get().split()

            }

        for currency in response.xpath("//div[contains(@class, 'partner cfix')]"):
            yield {
                'partners_name': currency.xpath(".//div/h1/a/text()").get(),
                'partner_info': currency.xpath(".//div/text()")[1].get().split()

            }
