import scrapy


class HfzwSpider(scrapy.Spider):
    name = "hfzw"
    allowed_domains = ["zwykb.cq.gov.cn"]
    start_urls = ["https://zwykb.cq.gov.cn/qxzz/yyxxx/bszn/?id=956cd2bf-92e0-44b3-a7ab-646ec50380d9&parentPage=8"]

    def parse(self, response):
        print(response.text)
