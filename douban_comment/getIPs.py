from bs4 import BeautifulSoup
import requests
import re

IPRegular = r"(([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5]).){3}([1-9]?\d|1\d{2}|2[0-4]\d|25[0-5])"


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


if __name__ == "__main__":
    ExtractIP()