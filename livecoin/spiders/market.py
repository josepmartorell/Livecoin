# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class MarketSpider(scrapy.Spider):
    name = 'market'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = ['http://www.livecoin.net/en/']

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(1))
            rur_tab = assert(splash:select_all("button.button-red"))
            rur_tab[1]:mouse_click()
            assert(splash:wait(1))
            splash:set_viewport_full()
            return splash:html()
        end

    '''

    def start_requests(self):
        yield SplashRequest(url="https://www.livecoin.net/en", callback=self.parse, endpoint="execute", args={
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

            }
