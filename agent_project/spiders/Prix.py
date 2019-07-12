from bs4 import BeautifulSoup
import scrapy
import cfscrape
from fake_useragent import UserAgent
import pendulum
import json
import csv
from agent_project.items.Items import *

class Prix(scrapy.Spider):
    name = "prix"

    custom_settings = {
        'CONCURRENT_REQUESTS': '1',
        'DOWNLOAD_DELAY':'2',
        'COOKIES_ENABLED':True
    }


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


        with open('./agent_project/data/commune.csv', newline='') as csvfile:
            communereader = csv.reader(csvfile, delimiter=',', quotechar='|')
            i = 0
            for row in communereader:
                if i>0 and i < 8 and row[1]!='NA':
                    #print(', '.join(row))
                    c=row[1]
                    id=row[0]
                    json_url = self.build_api_call(c)
                    yield scrapy.Request(json_url,
                                         headers={'X-Requested-With': 'XMLHttpRequest',
                                         'Content-Type': 'application/json; charset=UTF-8'},
                                         callback=self.parse_commune,meta={'id': id})
                i+=1

    def parse_commune(self,response):
        meta = response.meta
        if response.status == 404:
            print("END OF WORLD")
            item = PRIXItem()
            item['id'] = meta['id']
            item['place'] = "NA"
            item['rent_apart_hybrid_high'] = "NA"
            item['rent_apart_hybrid_low'] = "NA"
            item['rent_apart_hybrid_value'] = "NA"
            item['rent_apart_t1_high'] = "NA"
            item['rent_apart_t1_low'] = "NA"
            item['rent_apart_t1_value'] = "NA"
            item['rent_apart_t2_high'] = "NA"
            item['rent_apart_t2_low'] = "NA"
            item['rent_apart_t2_value'] = "NA"
            item['rent_apart_t3_high'] = "NA"
            item['rent_apart_t3_low'] = "NA"
            item['rent_apart_t3_value'] = "NA"
            item['rent_apart_t4_high'] = "NA"
            item['rent_apart_t4_low'] = "NA"
            item['rent_apart_t4_value'] = "NA"
            item['sell_apart_high'] = "NA"
            item['sell_apart_low'] = "NA"
            item['sell_apart_value'] = "NA"
            item['sell_house_high'] = "NA"
            item['sell_house_low'] = "NA"
            item['sell_house_value'] = "NA"
            item['sell_hybrid_high'] = "NA"
            item['sell_hybrid_low'] = "NA"
            item['sell_hybrid_value'] = "NA"
            item['zips'] = "NA"
        else:
            item = PRIXItem()
            dataJson = json.loads(response.body_as_unicode())
            # item['id'] = dataJson['response']['place']['id']
            # item['place'] = dataJson['response']['place']['slug']
        yield item



        # print(data['market']['prices'])
