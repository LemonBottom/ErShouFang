# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request
import random
import time
import logging
import redis


class ErshoufangSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ErshoufangDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self, ua):
        self.ua = ua

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls(crawler.settings.getlist("USER_AGENT"))
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        # 我爱我家反爬，需要cookie
        if "5i5j" in request.url:
            request.cookies = {
                'PHPSESSID': '1p63h7he47e4jb21uf3qpqa31h',
                 ' domain': 'bj',
                 ' yfx_c_g_u_id_10000001': '_ck18122702385612291856717911557',
                 ' yfx_f_l_v_t_10000001': 'f_t_1545849536214__r_t_1545849536214__v_t_1545849536214__r_c_0',
                 ' yfx_mr_n_10000001': 'baidu::market_type_ppzq::::::::::%E6%A0%87%E9%A2%98::bj.5i5j.com::::::%E5%B7%A6%E4%BE%A7%E6%A0%87%E9%A2%98::%E6%A0%87%E9%A2%98::160::pmf_from_adv::bj.5i5j.com/',
                 ' yfx_mr_f_n_10000001': 'baidu::market_type_ppzq::::::::::%E6%A0%87%E9%A2%98::bj.5i5j.com::::::%E5%B7%A6%E4%BE%A7%E6%A0%87%E9%A2%98::%E6%A0%87%E9%A2%98::160::pmf_from_adv::bj.5i5j.com/',
                 ' _ga': 'GA1.2.1709742213.1545849536',
                 ' _gid': 'GA1.2.1682278583.1545849536',
                 ' _gat': '1',
                 ' Hm_lvt_94ed3d23572054a86ed341d64b267ec6': '1545849537',
                 ' Hm_lpvt_94ed3d23572054a86ed341d64b267ec6': '1545849539',
                 ' _Jo0OQK': '50ADB2E7DEF3A95BCBAA04D52F5414775A30C0C5815693EB62460770A7531C510DCEFD1A42F959FF2E12A16D4BFD17D9C7D374A1376BEE8ED0AACA8F800B32B3CE3C57212F12283777C840763663251ADEB840763663251ADEBC6107B635DA7B8669547054735CB82A9GJ1Z1XA=='}
        request.headers["User-Agent"] = random.choice(self.ua)
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomProxy:
    """
    将每次请求加上代理ip
    """
    def __init__(self, proxy_key, redis_setting):
        self.proxy_key = proxy_key
        self.server = redis.Redis(*redis_setting)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get("PROXY_KEY"), crawler.settings.getlist("REDIS"))

    def set_proxy(self, server):
        if server.scard(self.proxy_key) == 0:
            # 等待代理池初始化
            time.sleep(10)
        return server.srandmember(self.proxy_key, 1)[0].decode("utf-8")

    def process_request(self, request, spider):
        request.meta["proxy"] = "https://" + self.set_proxy(self.server)

    def process_exception(self, request, exception, spider):
        if exception:
            logging.error("连接异常，返回消息队列")
            return Request(request.url, callback=request.callback, dont_filter=True)

    def process_response(self, request, response, spider):
        if response.status != 200:
            logging.error("状态码异常，返回消息队列")
            return Request(request.url, callback=request.callback, dont_filter=True)
        return response