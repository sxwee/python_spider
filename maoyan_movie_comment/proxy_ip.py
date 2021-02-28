import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

ua = UserAgent()

# 抓取IP的匹配规则
IPRegular = r"(([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])"

def ExtractIP(url="https://ip.ihuan.me/"):
    """
    抓取IP，返回IP列表
    url：抓取IP的网站
    """
    IPs = []
    try:
        response = requests.get(url,headers={'User-Agent': ua.chrome})
        soup = BeautifulSoup(response.content,"lxml",from_encoding='utf-8')                                
        tds = soup.find_all("a",attrs = {'target':'_blank'})
        for td in tds:
            string = td.text
            if re.search(IPRegular,string) and string not in IPs:
                IPs.append(string)
    except requests.exceptions.RequestException as e:
        print(e)
    return IPs

if __name__ == "__main__":
    IPs = ExtractIP()
    print(IPs)