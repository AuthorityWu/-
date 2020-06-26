
import logging
import scrapy
from scrapy.selector import Selector
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy.settings import Settings
from scrapy.http import Request
import sys

sys.path.append("../..")
from chessspider.items import ChessDataItem


class ChessDataSpider(scrapy.Spider):
    name = "chessdataspider"
    count = 0
    # 设置下载延时
    download_delay = 0
    allowed_domains = ["game.onegreen.net"]
    start_urls = [
        "http://game.onegreen.net/chess/Index.html"
    ]

    def parse(self, response):
        hxs = Selector(response)
        title = hxs.xpath("//title/text()")[0].extract()
        iframes = hxs.xpath("//iframe/@name").extract()

        is_item = False
        for iframe in iframes:
            item = self.parse_item(title, iframe)
            if len(item["move_list"]) >0 and len(item["result"]) > 0:
                is_item = True
                item["url"] = response.url
                yield item

        if not is_item and response.url.find("/chess/HTML/") < 0:
            for url in hxs.xpath("//a/@href").extract():
                if url.find("chess") >= 0:
                    print("ok url:", url)
                    if url.find("http://game.onegreen.net/") >= 0:
                        yield Request(url, callback=self.parse)
                    else:
                        yield Request("http://game.onegreen.net" + url, callback=self.parse)
                else:
                    print("error url:", url)


    def get_Data(self, data, pattern):
        #print("data",data)
        result = []
        start_index = 0
        for i in range(10):
            start = data.find("[{}]".format(pattern), start_index, len(data))

            if start < 0:
                break
            start += len("[{}]".format(pattern))
            end = data.find("[/{}]".format(pattern), start_index, len(data))
            if start < end:
                result.append(data[start:end])
            start_index = end + len("[/{}]".format(pattern))
        if len(result) == 0:
            return ""
        #print("XXXXXXXXXXXXXXX",result,"XXXXXXXXXXXXXX")
        #print("MAXMAXMAX",max(result, key=lambda k: len(result)))
        return max(result, key=lambda k: len(result))
        #return result

    """
    def get_Data(self, data, pattern):
        result = []
        start_index = 0
        start = data.find("[{}]".format(pattern), start_index, len(data))
        start +=  len("[{}]".format(pattern))

        end  = data.find("[/{}]".format(pattern), start_index, len(data))
        if start < end:
            result.append(data[start:end])
        if len(result) == 0:
            return ""
        return result
    """

    def parse_item(self, title, data):

        item = ChessDataItem()
        item["move_list"] = self.get_Data(data, "DhtmlXQ_movelist")
        item["title"] = self.get_Data(data, "DhtmlXQ_title")
        item["name_black"] = self.get_Data(data, "DhtmlXQ_black")
        item["name_red"] = self.get_Data(data, "DhtmlXQ_red")
        item["desc"] = self.get_Data(data, "DhtmlXQ_event")
        item["result"] = self.get_Data(data, "DhtmlXQ_result")
        item["init"] = self.get_Data(data, "DhtmlXQ_binit")
        if len(item["title"]) == 0:
            item["title"] = title

        return item





