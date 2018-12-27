# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from ErShouFang.items import ErshoufangItem


class WiwjSpider(scrapy.Spider):
    name = 'Wiwj'
    start_urls = [f'https://bj.5i5j.com/ershoufang/{region}/' for region in\
                  ["haidianqu", "dongchengqu", "xichengqu", "fengtaiqu", "shijingshanqu", "tongzhouqu",
                   "changpingqu", "daxingqu", "yizhuang", "shunyiqu", "fangshanqu", "mentougou",
                   "pinggu", "huairou", "miyun", "yanqing", "chaoyangqu"]]

    def parse(self, response):
        redirect = self.rediection(response, self.parse)
        if not redirect:
            total_num = response.xpath("//div[@class='total-box noBor']/span/text()").extract_first()
            max_page_num = int(int(total_num)/30) + 1
            for page in range(1, max_page_num + 1):
                yield scrapy.Request(response.url + f"n{page}/", callback=self.page_parse)
        else:
            return redirect

    def page_parse(self, response):
        redirect = self.rediection(response, self.parse)
        if not redirect:
            region = response.xpath("//li[@class='new_di_tab_cur']/text()").extract_first()
            date = datetime.datetime.now().strftime("%Y-%m-%d")
            lis = response.xpath("//ul[@class='pList']/li")
            for li in lis:
                room = li.xpath(".//div[@class='listCon']/div[@class='listX']/p[1]/text()").extract_first()
                # 商用非正规房
                if '多' in room:
                    return
                total_price = li.xpath(".//div[@class='listCon']/div[@class='listX']/div[@class='jia']/p[1]/strong/text()").extract_first()
                unit_price = li.xpath("//div[@class='listCon']/div[@class='listX']/div[@class='jia']/p[2]/text()").extract_first()
                community = li.xpath(".//div[@class='listCon']/div[@class='listX']/p[2]/a/text()").extract_first()
                yield ErshoufangItem(
                   bedroom=int(re.findall("(\d)室", room)[0]),
                   living_room=int(re.findall("(\d)厅", room)[0]),
                   area=float(re.findall(r"\·(.+)\s\s平米", room)[0]),
                   total_price=int(total_price),
                   unit_price=int(re.findall('单价(.+)元/', unit_price)[0]),
                   region=region,
                   community=community.split(' ')[1],
                   agency="我爱我家",
                   date=date
                    )
        else:
            return redirect

    def rediection(self, response, func):
        body = response.body.decode("utf-8")
        # 如果重定向那么重新发送request
        if "window.location.href" in body:
            return scrapy.Request(re.findall(r"window.location.href='(.+?)';", body)[0], callback=func)