import scrapy

from dota2.items import Dota2Item

class DmozSpider(scrapy.Spider):
    name = "dbuff"
    allowed_domains = ["dotabuff.com"]
    start_urls = [
        "http://www.dotabuff.com/players/105496685/heroes"
    ]

    def parse(self, response):
		for row in response.xpath('//table/tbody/tr'):
			item = Dota2Item()
			item['name'] = '' # not sure what to do with this one right now
			item['hero'] = ''
			item['played'] = ''
			item['winrate'] = ''
			item['kda'] = ''
			
			for cell in row.xpath('//td'):
				print cell.extract()
				if(cell.xpath('/div[@class="subtext minor"]').extract() != ''):
					item['hero'] = cell.xpath('a/text()').extract()	
				elif(cell.xpath('/div/div[@class="segment segment-matches"]') != ''):
					item['played'] = cell.xpath('text()').extract()
				elif(cell.xpath('/div/div[@class="segment segment-win-ratio"]') != ''):
					item['winrate'] = cell.xpath('text()').extract()
				elif(cell.xpath('/div/div[@class="segment segment-kda-ratio"]') != ''):
					item['kda'] = cell.xpath('text()').extract()
				
			print item['name'], item['hero'], item['played'], item['winrate'], item['kda']
			yield item
