# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from ErShouFang.items import ErshoufangItem


class LianjiaSpider(scrapy.Spider):
    name = 'LianJia'
    custom_settings = {
        'EXTENSIONS_DO': True
    }
    start_urls = [f'https://bj.lianjia.com/ershoufang/{region}/' for region in\
                  ["dongcheng", "xicheng", "chaoyang", "haidian", "fengtai", "shijingshan",
                   "tongzhou", "changping", "daxing", "yizhuangkaifaqu",
                   "shunyi", "fangshan", "mentougou", "pinggu", "huairou", "miyun", "yanqing"]]

    def parse(self, response):
        """
        每个地区的房屋列表页
        :param response:
        :return:
        """
        # 房子总数
        total_num = response.xpath("//h2[@class='total fl']/span/text()").extract_first().strip()
        # 最大页数
        max_page_num = int(int(total_num) / 30) + 1
        # 最多只有100页
        if max_page_num > 100:
            max_page_num = 100
        for page_num in range(1, max_page_num+1):
            # 带页数的url地址
            url = response.url + f"pg{page_num}/"
            yield scrapy.Request(url, callback=self.page_parse)

    def page_parse(self, response):
        lis = response.xpath("//li[@class='clear LOGCLICKDATA']")
        region = response.xpath("//div[@class='sub_nav section_sub_nav']/a[@class='selected']/text()").extract_first()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        for li in lis:
            room = li.xpath(".//div[@class='houseInfo']/text()[1]").extract_first()
            if "室" not in room:
                # 商住非正规房
                return
            area = li.xpath(".//div[@class='houseInfo']/text()[2]").extract_first()
            total_price = li.xpath(".//div[@class='totalPrice']/span/text()").extract_first()
            unit_price = li.xpath(".//div[@class='unitPrice']/span/text()").extract_first()
            community = li.xpath(".//div[@class='houseInfo']/a/text()").extract_first()
            yield ErshoufangItem(
               bedroom=int(re.findall("(\d)室", room)[0]),
               living_room=int(re.findall("(\d)厅", room)[0]),
               area=float(re.findall("(.+)平米", area)[0]),
               total_price=int(total_price),
               unit_price=int(re.findall('单价(.+)元/平米',unit_price)[0]),
               region=region,
               community=community,
               agency="链家",
               date=date
                )
