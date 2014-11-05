import scrapy

from dota2.items import Dota2Item

class DmozSpider(scrapy.Spider):
    name = "dbuff"
    allowed_domains = ["dotabuff.com"]
    start_urls = [
        "http://www.dotabuff.com/players/105496685/heroes/"
    ]

    def parse(self, response):
        #filename = response.url.split("/")[-2]
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
		for sel in response.xpath('//ul/li'):
			item = Dota2Item()
			item['name'] = sel.xpath('a/text()').extract()
			item['hero'] = sel.xpath('text()').extract()		    
			item['success'] = sel.xpath('a/@href').extract()
			item['played'] = sel.xpath('text()').extract()
			item['winrate'] = sel.xpath('text()').extract()
			item['kda'] = sel.xpath('text()').extract()
			print name, hero, success, played, winrate, kda
			#yield item