# coding:utf-8

from scrapy.linkextractors import LinkExtractor 
from scrapy.spiders import Rule

from scrapy_redis.spiders import RedisCrawlSpider

class AqiRedisCrawlSpider(RedisCrawlSpider):
	name = "aqi_rediscrawlspider"
	allowed_domains = ['aqistudy.cn']
	base_url = 'https://www.aqistudy.cn/historydata/' # 静态页面

	# 第一个请求是首页的请求,返回的响应默认交给所有的 Rule提取新的链接并发送请求
	# start_urls = [base_url]
	redis_key = "aqirediscrawlspider:start_urls"

	rules = [
		# 提取所有城市的链接,并发送请求,返回的响应默认经过所有的 Rule 继续提取链接
		Rule(LinkExtractor(allow=r"monthdata\.php\?city=")),
		# 提取每个月分的链接,并发送请求,返回的响应默认交给 callback 解析提取每天的数据,不需要再提取链接
		Rule(LinkExtractor(allow=r"daydata\.php\?city="),callback="parse_day")
	]
	# 如果没有 callback, 默认 follow 为 True
	# 如果有 callback, 默认follow 为 false

	def parse_day(self,response):
		"""
			提取当前月份的所有数据,并保存在 item 中
			(按动态页面解析)
		"""

		url = response.url
		city_urlencode = url[url.find("=")+1:url.find("&")]
		city = urllib.unquote(city_urlencode).decode('utf-8')

		# 所有天的结点列表
		tr_list = response.xpath("//tbody//tr")
		tr_list.pop(0)

		city = response.meta['city']

		for tr in tr_list:
			item = AqispiderItem()
			# 日期
			item['date'] = tr.xpath("./td[1]//text()").extract_first()
			# 空气质量指数
			item['aqi'] = tr.xpath("./td[1]//text()").extract_first()
			# 空气质量等级
			item['level'] = tr.xpath("./td[1]//text()").extract_first()
			# pm2.5
			item['pm2_5'] = tr.xpath("./td[1]//text()").extract_first()
			# pm10
			item['pm10'] = tr.xpath("./td[1]//text()").extract_first()
			# 二氧化硫
			item['so2'] = tr.xpath("./td[1]//text()").extract_first()
			# 一氧化碳
			item['co'] = tr.xpath("./td[1]//text()").extract_first()
			# 二氧化氮
			item['no2'] = tr.xpath("./td[1]//text()").extract_first()
			# 臭氧
			item['o3_8h'] = tr.xpath("./td[1]//text()").extract_first()
			# 数据的抓取时间
			item['time'] = str(datetime.now())
			# 抓取数据的爬虫
			item['spider'] = self.name


			# 返回给管道
			yield item
