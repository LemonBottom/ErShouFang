# Create time:2018-12-24 22:05
# Author:Chen
from scrapy import signals
from scrapy.exceptions import NotConfigured
import requests
import time
import threading
import json
import logging
import redis


class QingtingProxy:

	def __init__(self, proxy_key, redis_setting):
		self.url = "https://proxy.horocn.com/api/proxies?order_id=U7G61620840936700598&num=10&format=json&line_separator=win"
		self.spider_running = True
		self.proxy_key = proxy_key
		self.server = redis.Redis(*redis_setting)

	@classmethod
	def from_crawler(cls, crawler):
		if crawler.settings.get("EXTENSIONS_DO"):
			spider = cls(crawler.settings.get("PROXY_KEY"), crawler.settings.getlist("REDIS"))
			crawler.signals.connect(spider.engine_started, signal=signals.engine_started)
			crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
			return spider
		else:
			raise NotConfigured

	def proxy(self, server):
		while self.spider_running:
			r = requests.get(self.url)
			logging.debug(r.text)
			if "不足" in r.text:
				raise Exception("代理余额不足")
			# 代理ip和端口号组合后的列表
			ip_list = [i['host'] + ":" + str(i["port"]) for i in json.loads(r.text)]
			for ip in ip_list:
				server.sadd(self.proxy_key + "_pr", ip)
			server.rename(self.proxy_key + "_pr", self.proxy_key)
			# 代理ip调用最小间隔10s
			time.sleep(10)

	def engine_started(self):
		# 当engine开始运行时开始维护代理池
		threading.Thread(target=self.proxy, args=(self.server,)).start()

	def spider_closed(self, spider):
		# 当爬虫关闭时关闭代理池维护
		self.spider_running = False
