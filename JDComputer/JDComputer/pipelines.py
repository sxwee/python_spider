# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd


class JdcomputerPipeline:
    def process_item(self, item, spider):
        return item

class ComputerItemTOCSV:

    def process_item(self,item,spider):
        data = pd.DataFrame({'pctype':item['pctype'],'price':item['price'],'shop':item['shop']})
        data.to_csv('ComputerInfo.csv',mode='a',header=False,index=False)
        
        return item
