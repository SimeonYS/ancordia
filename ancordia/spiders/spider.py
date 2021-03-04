import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import AncdordiaItem
from itemloaders.processors import TakeFirst
pattern = r'(\xa0)?'

class AncdordiaSpider(scrapy.Spider):
	name = 'ancordia'
	start_urls = ['https://www.ancoriabank.com/news']
	number = 1
	def parse(self, response):
		post_links = response.xpath('//h2/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)


		next_page = f'https://www.ancoriabank.com/news?page={str(self.number)}'
		if response.xpath('//div[@class="pagination"]//i[@class="fa fa-angle-right"]').get():
			self.number +=1
			yield response.follow(next_page, self.parse)


	def parse_post(self, response):

		date = response.xpath('//div[@class="blog-item-data"]//text()').getall()
		date = ''.join([p.strip() for p in date if p.strip()])
		title = response.xpath('//h2[@class="blog-item-title font-alt"]//text()').get()
		content = response.xpath('//div[@class="field field-name-body field-type-text-with-summary field-label-hidden"]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=AncdordiaItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
