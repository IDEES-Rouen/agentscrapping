from bs4 import BeautifulSoup
import scrapy
import cfscrape
from fake_useragent import UserAgent
import pendulum
import json

class Prix(scrapy.Spider):
    name = "prix"
    start_urls = ['https://www.meilleursagents.com/prix-immobilier/']
    allowed_domains = ['meilleursagents.com']
    ua = UserAgent()

    def __init__(self, aDate = pendulum.today()):
        super(Prix, self).__init__()
        self.aDate = aDate
        self.timestamp = self.aDate.timestamp()
        print("PENDULUM UTC TODAY", self.aDate.today())
        print("PENDULUM UTC TIMESTAMP TODAY ", self.timestamp)
    def clean_html(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()

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


    def build_api_call(self,commune):
        query = 'https://www.meilleursagents.com/prix-immobilier/{commune}/?partial=1'.format(commune=commune)
        print("Query = ", query)
        return query

    ###################################
    # MAIN PARSE
    ####################################

    def parse(self, response):
        json_url = self.build_api_call("lanta-31570")
        yield scrapy.Request(json_url,
                             headers={'X-Requested-With': 'XMLHttpRequest',
                                      'Content-Type': 'application/json; charset=UTF-8'},
                             callback=self.parse_commune)

    def parse_commune(self,response):
        data = json.loads(response.body_as_unicode())
        print(data['market'])
