from chessspider.spiders.chessdataspider import  ChessDataSpider,Settings,CrawlerRunner,reactor

if __name__ == '__main__':
    print("******************* \n\n")
    settings = Settings()
    runner = CrawlerRunner(settings)
    d = runner.crawl(ChessDataSpider)
    reactor.run()  # the script will block here until the crawling is finished

