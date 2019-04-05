import scrapy

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


#https://doc.scrapy.org/en/latest/topics/practices.html

from agent_project.spiders import Prix
from agent_project.spiders import Communes

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(Communes.Communes)
    #yield runner.crawl(Prix.Prix)
    reactor.stop()

crawl()
reactor.run()