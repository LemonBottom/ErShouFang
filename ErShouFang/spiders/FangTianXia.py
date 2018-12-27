# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from ErShouFang.items import ErshoufangItem


class FangtianxiaSpider(scrapy.Spider):
    name = 'FangTianXia'
    start_urls = [f'https://esf.fang.com{region}' for region in\
                  ["/house-a01/", "/house-a00/", "/house-a06/", "/house-a03/", "/house-a02/",
                  "/house-a012/", "/house-a0585/", "/house-a010/", "/house-a08/", "/house-a011/",
                   "/house-a07/", "/house-a013/", "/house-a09/", "/house-a014/", "/house-a015/", "/house-a016/"]]

    def parse(self, response):
        max_page = response.xpath("//div[@class='page_al']/p[last()]/text()").extract_first()
        max_page_num = re.findall('共(\d+)页', max_page)[0]
        for page in range(1, int(max_page_num) + 1):
            yield scrapy.Request(response.url + f"i3{page}/", callback=self.page_parse)

    def page_parse(self, response):
        region = response.xpath("//div[@class='term_screen2 clearfix']/ul/li[1]/a/text()").extract_first()
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        dls = response.xpath("//div[@class='shop_list shop_list_4']/dl")
        for dl in dls:
            room = dl.xpath(".//p[@class='tel_shop']/text()[1]").extract_first()
            if room:
                area = dl.xpath(".//p[@class='tel_shop']/text()[2]").extract_first()
                total_price = dl.xpath(".//dd[@class='price_right']/span/b/text()").extract_first()
                unit_price = dl.xpath(".//dd[@class='price_right']/span[2]/text()").extract_first()
                community = dl.xpath(".//p[@class='add_shop']/a/@title").extract_first()
                yield ErshoufangItem(
                    bedroom=int(re.findall("(\d)室", room)[0]),
                    living_room=int(re.findall("(\d)厅", room)[0]),
                    area=float(re.findall("(.+)㎡", area)[0]),
                    total_price=int(total_price),
                    unit_price=int(re.findall('(\d+)元/㎡', unit_price)[0]),
                    region=region,
                    community=community,
                    agency="房天下",
                    date=date
                )