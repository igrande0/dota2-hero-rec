import scrapy
from dota2.items import Dota2Item

class DmozSpider(scrapy.Spider):
  name = "dbuff"
  allowed_domains = ["www.dotabuff.com"]
  max_range = 1000000
  
  def iterate_req(self):
	for i in range(1, self.max_range):
		yield Request('http://www.dotabuff.com/players/%d' % i, callback=self.parse)
		
  def parse(self, response):
	item = Dota2Item()
	item['name'] = response.url
	
	cut_string = item['name'].split('/')
	new_string = cut_string[4]
	print new_string
	
	filename = ("profileId.txt")
	idfile = open(filename, "w")
	idfile.write(new_string + '\n')
	
	return item
	