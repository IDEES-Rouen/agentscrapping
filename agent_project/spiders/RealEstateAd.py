from bs4 import BeautifulSoup
import scrapy
import cfscrape
from fake_useragent import UserAgent
import pendulum
import json

class RealEstateAd(scrapy.Spider):
    name = "realEstateAd"

    custom_settings = {
        'CONCURRENT_REQUESTS': '1',
        'DOWNLOAD_DELAY':'2',
        'COOKIES_ENABLED':True
    }

    start_urls = ['https://www.meilleursagents.com/achat/']
    allowed_domains = ['meilleursagents.com']
    ua = UserAgent()

    def __init__(self, aDate = pendulum.today()):
        super(RealEstateAd, self).__init__()
        self.aDate = aDate
        self.timestamp = self.aDate.timestamp()
        print("PENDULUM UTC TODAY", self.aDate.today())
        print("PENDULUM UTC TIMESTAMP TODAY ", self.timestamp)

    def start_requests(self):
        cf_requests = []
        user_agent = self.ua.random
        self.logger.info("RANDOM user_agent = %s", user_agent)
        for url in self.start_urls:
            token , agent = cfscrape.get_tokens(url,user_agent)
            self.logger.info("token = %s", token)
            self.logger.info("agent = %s", agent)

            cf_requests.append(scrapy.Request(url=url,
                                              cookies= token,
                                              headers={'User-Agent': agent}))
        return cf_requests

    def parse(self,response):

        query = 'https://www.meilleursagents.com/annonces/achat/{commune}'.format(commune='mont-saint-aignan-76130')

        yield scrapy.Request(query, callback=self.parse_commune)

    def parse_commune(self,response):
        for href in response.xpath("//a[@class='listing-item__picture-container']/@href"):
            print(href.extract())
