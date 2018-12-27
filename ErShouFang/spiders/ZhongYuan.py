# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from ErShouFang.items import ErshoufangItem


class ZhongyuanSpider(scrapy.Spider):
    name = 'ZhongYuan'
    start_urls = [f'https://bj.centanet.com/ershoufang/{region}/' for region in\
                  ["dongchengqu", "haidianqu", "xichengqu", "shijingshanqu", "fengtaiqu", "shunyiqu",
                   "mentougouqu", "tongzhouqu", "daxingqu", "yizhuangkaifaqu"]]

    def parse(self, response):
        max_page = response.xpath("//a[text()='>>']/@href").extract_first()
        # 判断是否有第二页，如果没有直接分析网页
        if max_page:
            max_page_num = re.findall(r'g(\d+)\/', max_page)[0]
            for page in range(1, int(max_page_num) + 1):
                yield scrapy.Request(response.url + f"g{page}/", callback=self.page_parse)
        else:
            self.page_parse(response)

    def page_parse(self, response):
        region = response.xpath("//p[@class='termcon fl ']/span[@class='curr']/text()").extract_first()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        divs = response.xpath("//div[@class='house-item clearfix']")
        for div in divs:
            room = div.xpath(".//p[@class='house-name']/span[2]/text()").extract_first()
            area = div.xpath(".//p[@class='house-name']/span[4]/text()").extract_first()
            total_price = div.xpath(".//p[@class='price-nub cRed tc']/span/text()").extract_first()
            unit_price = div.xpath(".//p[@class='price-txt tc']/text()").extract_first()
            community = div.xpath(".//p[@class='house-name']/a/text()").extract_first()
            yield ErshoufangItem(
                bedroom=int(re.findall("(\d)室", room)[0]),
                living_room=int(re.findall("(\d)厅", room)[0] if '厅' in room else '0'),
                area=float(re.findall("(.+)平", area)[0]),
                total_price=int(float(total_price)),
                unit_price=int(float(re.findall('(\d+)元/平', unit_price)[0])),
                region=region,
                community=community,
                agency="中原地产",
                date=date
            )