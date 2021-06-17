from bs4 import BeautifulSoup
import requests
import re
import json
import random
import pandas as pd
import traceback

IPRegular = r"(([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])"

headers = {
    "User-Agent": "换成自己的User-Agent",
    "cookie": "换成自己登录的淘宝cookie"
}

def ExtractIP(url="https://ip.ihuan.me/"):
    """
    功能：抓取IP，返回IP列表
    url：抓取IP的网站
    """
    IPs = []
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"lxml")                                
    tds = soup.find_all("a",attrs = {'target':'_blank'})
    for td in tds:
        string = td.text
        if re.search(IPRegular,string) and string not in IPs:
            IPs.append(string)
    print(IPs)
    return IPs
        
def Filter(mobile_infos):
    """
    功能：过滤出手机的相关信息
    mobile_infos：
    """
    mobile_list = [] #存储手机信息的列表
    for mobile_info in mobile_infos:
        title = mobile_info['raw_title']
        price = mobile_info['view_price']
        loc = mobile_info['item_loc'].replace(' ','')
        shop = mobile_info['nick']
        #print(mobile_info['view_sales'])
        sales = re.search(r'(\d+.?\d*).*人付款',mobile_info['view_sales']).group(1)
        if sales[-1] == '+':#去掉末尾的加号
            sales = sales[:-1]
        if '万' in mobile_info['view_sales']:
            sales = float(sales) * 10000
        print(title,price,loc,shop,int(sales),mobile_info['view_sales'])
        mobile_list.append([title,price,loc,shop,int(sales)])

    return mobile_list

def Saver(mobiles):
    """
    功能：保存爬取信息
    mobiles：手机信息列表
    """
    mdata = pd.DataFrame(mobiles,columns=['手机名','价格','店铺位置','店铺名','销量'])
    mdata.to_csv('mobile_info.csv',index=False)


def Spider(page_nums = 100):
    """
    功能：爬虫主程序
    page_nums：待爬取的页数
    """
    #爬取代理IP
    IPs = ExtractIP()
    length,mobiles,i = len(IPs),[],0
    while i < page_nums:
        try:
            print('--------------------正在爬取第{}页--------------------'.format(i + 1))
            url = "https://s.taobao.com/search?q=%E6%89%8B%E6%9C%BA&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=3&ntoffset=0&p4ppushleft=1%2C48&data-key=s&data-value={}".format(i*44)
            #设置代理ip
            index = random.randint(0,length - 1)
            proxies = {"http":"{}:8080".format(IPs[index])}
            #请求网页
            response = requests.get(url,headers=headers,proxies=proxies)
            #利用正则表达式获取包含手机信息json数据
            match_obj = re.search(r'g_page_config = (.*?)};',response.text)
            #将json对象加载为python字典
            mobile_infos= json.loads(match_obj.group(1) + '}')['mods']['itemlist']['data']['auctions']
            #过滤出字典中的有用信息
            mobiles += Filter(mobile_infos)
            i += 1
        except Exception:
            traceback.print_exc()
            print('手机信息第{}页爬取失败'.format(i + 1))
            i += 1
    #保存手机信息为csv文件
    Saver(mobiles)


if __name__ == "__main__":
    Spider()