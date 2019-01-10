# Create time:2018-12-26 15:49
# Author:Chen
# 数据可视化

from pyecharts import Bar, Pie
import pymongo
import datetime
import xlwt


class DataSight:

    def __init__(self):
        self.mongo_cli = pymongo.MongoClient('127.0.0.1', 27017).ErShouFang.houses
        self.sub_title = "作者：Chen"

    def avg_area(self):
        """
        生成区域平均面积图片
        :return:
        """
        self.render_data("北京二手房平均面积", "平方米", "region", "avg", "$area", "柱状图")

    def avg_unit_price(self):
        """
        生成区域平均价格图片
        :return:
        """
        self.render_data("北京二手房平均价格", "元/平方米", "region", "avg", "$unit_price", "柱状图")

    def count(self):
        """
        生成区域数量图片
        :return:
        """
        self.render_data("北京二手房在售数量", "套", "region", "sum", 1, "柱状图")

    def agency_count(self):
        """
        爬虫四大中介在售房的饼状图
        :return:
        """
        self.render_data("北京二手房数据分布", "套", "agency", "sum", 1, "饼状图")

    def community_avg_price(self):
        excel = xlwt.Workbook()
        for region in ["西城", "东城", "朝阳", "海淀"]:
            arg = [
                {'$match': {"region": region}},
                {"$group": {"_id": "$community", "avg_price": {"$avg": "$unit_price"}, "count": {"$sum": 1}}},
                {"$match": {"count": {"$gt": 4}}},
                {"$sort": {"avg_price": -1}},
                {"$limit": 10}
            ]
            result = self.mongo_cli.aggregate(arg)
            sheet = excel.add_sheet(region)
            sheet.write(0, 0, "小区名称")
            sheet.write(0, 1, "平均价格")
            for i, data in enumerate(result):
                sheet.write(i + 1, 0, data['_id'])
                sheet.write(i + 1, 1, int(data['avg_price']))
        excel.save("北京最贵小区表.xls")

    def render_data(self, title_name, unit_name, group_name, accumulate_type, accumulate_name, image_type):
        """
        生成图片
        :param title_name: 标题和文件名字 字符串
        :param unit_name: 单位 字符串
        :param file_name: 生成的图片名称 字符串
        :param group_name: 数据库中的key，根据此名字对数据分组 字符串
        :param accumulate_type: 计算的类型 sum：求和 avg：求平均值等 字符串
        :param accumulate_name: 数据库中的key，被计算数据的名字 前面加$
        :param image_type: 图标类型，柱状图，饼状图
        :return:
        """
        arg = [{"$group": {"_id": f"${group_name}", "result": {f"${accumulate_type}": accumulate_name}}}]
        result = list(self.mongo_cli.aggregate(pipeline=arg))
        # 由大到小排序
        result.sort(key=lambda x: x['result'], reverse=True)
        for i in result:
            if i['_id'] == "亦庄开发区":
                i['_id'] = "亦庄"
        if image_type == "柱状图":
            bar = Bar(f"{title_name}{datetime.datetime.now().strftime('%m%d')}", self.sub_title)
        elif image_type == "饼状图":
            bar = Pie(f"{title_name}{datetime.datetime.now().strftime('%m%d')}", self.sub_title)
        else:
            raise Exception("未定义图标类型")
        bar.add(
            f"单位：{unit_name}",
            [r['_id'] for r in result],
            [int(r['result']) for r in result],
            xaxis_interval=0,
            is_label_show=True
        )
        bar.render(path=f'{title_name}.png')


if __name__ == "__main__":
    DataSight().community_avg_price()
