# Create time:2018-12-25 17:44
# Author:Chen

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
	p = CrawlerProcess(get_project_settings())
	p.crawl("ZhongYuan")
	# p.crawl("Wiwj")
	# p.crawl("LianJia")
	# p.crawl("FangTianXia")
	p.start()
