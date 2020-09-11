from bs4 import BeautifulSoup
import requests
import re
import json
import random
import pandas as pd
import traceback

IPRegular = r"(([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
    "cookie": "thw=cn; cna=7W44FT/BQ3UCAXyhCANsjkrB; tracknick=%5Cu4E00%5Cu84D1%5Cu70DF%5Cu96E8%5Cu4EFB%5Cu5E73%5Cu751F678; tg=0; hng=CN%7Czh-CN%7CCNY%7C156; miid=452598852068526430; sgcookie=Erop1RJclTWUlHu6njl9r; uc3=vt3=F8dCufTP%2F1zP09zomvw%3D&lg2=V32FPkk%2Fw0dUvg%3D%3D&id2=UNX4HdDc7DfpNw%3D%3D&nk2=saDShX4nCyjW1n1YqyTdKU4%3D; lgc=%5Cu4E00%5Cu84D1%5Cu70DF%5Cu96E8%5Cu4EFB%5Cu5E73%5Cu751F678; uc4=id4=0%40UgJ9%2F0%2FW7CwgGrfAVFRiZZHHtRL7&nk4=0%40s8WS70y7cDeuHXfNGrC%2Fb9UKyx1%2F6TyFOYipUg%3D%3D; _cc_=WqG3DMC9EA%3D%3D; enc=Liv1XLNGVc%2BwJRzw%2FAW0LTuvAhCB0M9flhhelKsSAqmUy3jF2Y4yw6u6TYo%2BOKsKLM4x6IS7hN1tlZxfL%2BHuvA%3D%3D; UM_distinctid=17473196d42f7-0caca7877e514f-f7b1332-100200-17473196d437aa; mt=ci=-1_0; xlly_s=1; lLtC1_=1; v=0; _m_h5_tk=0d1d7b142c58bf91a3ad82ddfd37169d_1599723236031; _m_h5_tk_enc=a80117ec7f3cb50505f45377d01e60b4; t=2ae93078faab98d27c06beb0609a6f0a; _tb_token_=ee6539f5d7635; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; cookie2=1d4dda7ef6c8999b65003ad9455ce33b; JSESSIONID=77B58A9CB1EDB5BED7330917074DDB58; uc1=cookie14=UoTV5YvD0UgsXw%3D%3D; isg=BFBQDI86O4q9ceX3ddHQbuXcIZ6iGTRji3WGpkojjqt-hfAv8i3v86f8WU1lUew7; l=eBQ2dBUlqEOpXI5pBO5BFurza7793QRb4oVzaNbMiInca6adtFTqjNQ4CnkXSdtjgtCFVetPDcnX3RLHR3fd9xDDB3h2q_PjFxvO.; tfstk=cYHFBs1vYppFk2eWMJwPF__SPzVda9kohBE8tb2saFfO86r3usfOylx1y23zkdVh."
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
