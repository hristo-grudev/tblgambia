import scrapy

from scrapy.loader import ItemLoader

from ..items import TblgambiaItem
from itemloaders.processors import TakeFirst


class TblgambiaSpider(scrapy.Spider):
	name = 'tblgambia'
	start_urls = ['https://tblgambia.com/news/']

	def parse(self, response):
		post_links = response.xpath('//a[@class="post-details details-type-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="entry-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//a[@class="data-link"]/time/text()').get()

		item = ItemLoader(item=TblgambiaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
