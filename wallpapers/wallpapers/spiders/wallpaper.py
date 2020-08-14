import scrapy
from ..items import WallpapersItem
from bs4 import BeautifulSoup

class WallpaperSpider(scrapy.Spider):
    name = 'wallpaper'
    allowed_domains = ['wallpaperscraft.com']
    
    def start_requests(self):
        page_num = 180
        for i in range(1,page_num + 1):
            url = "https://wallpaperscraft.com/catalog/art/page{}".format(i)
            yield scrapy.Request(url,callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text,'lxml')
        images = soup.findAll('img',attrs={'class':'wallpapers__image'})
        image_urls = []
        for image in images:
            link = image.get('src')
            image_urls.append(link.replace('300x168','1280x720'))
            
        item = WallpapersItem()
        item['image_urls'] = image_urls
        return item

