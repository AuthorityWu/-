import scrapy


class ChessDataItem(scrapy.Item):
    url = scrapy.Field()
    init = scrapy.Field()
    name_black = scrapy.Field()
    name_red = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    move_list = scrapy.Field()
    desc = scrapy.Field()
    result = scrapy.Field()
    pass