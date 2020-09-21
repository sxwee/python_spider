import scrapy
import re
from bs4 import BeautifulSoup
from ..items import JdcomputerItem
from fake_useragent import UserAgent


class ComputerSpiderSpider(scrapy.Spider):
    name = 'computer_spider'
    allowed_domains = ['jd.com']

    def __init__(self):
        ua = UserAgent()
        self.headers = {
            "User-Agent":ua.random,
        }

    def start_requests(self):
        s,page = 1,1
        for i in range(100):
            url = "https://search.jd.com/Search?keyword=%E7%AC%94%E8%AE%B0%E6%9C%AC%E7%94%B5%E8%84%91&spm=2.1.0&page={}&s={}&click=0".format(1 + 2*i,s + 50*i)
            yield scrapy.Request(url,callback=self.parse,headers=self.headers)

    def parse(self, response):
        soup = BeautifulSoup(response.text,'lxml')
        pcs = soup.findAll('li',attrs={'class':re.compile('^gl-item.*')})
        pctype,price,shop = [],[],[]
        for pc in pcs:
            pc_type = pc.find('div',attrs={'class':'p-name p-name-type-2'}).get_text().strip()
            pc_price = re.search('^￥(\d+.\d{2}).*',pc.find('div',attrs={'class':'p-price'}).get_text().strip()).group(1)
            pc_shop = pc.find('a',attrs={'class':'curr-shop hd-shopname'}).get_text()
            pc_type = pc_type.replace('\t','').replace('\n','')
            pctype.append(pc_type)
            price.append(pc_price)
            shop.append(pc_shop)

        item = JdcomputerItem()
        item['pctype'] = pctype
        item['price'] = price
        item['shop'] = shop

        return item

