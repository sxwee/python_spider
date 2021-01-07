import requests
import pandas as pd
import threading
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re
import traceback
import random
from getIPs import ExtractIP

ua = UserAgent()
IPs = ExtractIP()

headers = {
    'User-Agent':ua.random,
     'Cookie': '换上自己登录豆瓣的cookie'
}

class DoubanCommentSpider(threading.Thread):
    def __init__(self,url,threadname,csv_filename) -> None:
        threading.Thread.__init__(self, name=threadname)
        self.headers = headers
        self.url = url
        self.csv_filename = csv_filename

    def run(self):
        """
        功能：线程的run方法
        """
        try:
            while pages:
                page_num = pages.pop(0)
                visit_url = self.url.format(page_num*20)
                print('{} is clawing {}'.format(self.getName(),visit_url))
                html_content = self.get_html(visit_url)
                comment = self.parse_html(html_content)
                self.save(comment)
        except Exception:
            traceback.print_exc()
        

    def get_html(self,url):
        """
        功能：下载url对应的网页并返回
        """
        index = random.randint(0,len(IPs) - 1)
        proxies =  {"http":"{}:8080".format(IPs[index])}
        response = requests.get(url,headers=self.headers,proxies=proxies)
        #print(response.text)
        if response.status_code == 200:
            return response.content
        else:
            return None

    def parse_html(self,content):
        """
        功能：分析下载网页
        """
        if content is None:
            return []
        soup = BeautifulSoup(content,'lxml')
        comments = soup.find_all('div',attrs={'class':'comment-item'})
        outcome = []
        for c in comments:
            rh = c.find('a')
            reviewer = rh.get('title') if rh else ''
            starclass = c.find('span',attrs={'class':re.compile('allstar')})
            star = starclass.get('class')[0][-2]+'星' if starclass else '未评分'
            cp = c.find('p',attrs={'class':'comment-content'})
            comment = cp.get_text().strip() if cp else ''
            outcome.append([reviewer,star,comment])
            #print([reviewer,int(star),comment])
        
        return outcome

    def save(self,comment):
        """
        功能：将排列数据写入csv文件
        """
        df = pd.DataFrame(comment)
        df.to_csv(self.csv_filename,mode='a',index=False,header=False)      



if __name__ == "__main__":
    threadNums = 5
    pages = [i for i in range(25)]
    url = "https://movie.douban.com/subject/30444960/comments?start={}&limit=20&status=P&sort=new_score"
    for i in range(threadNums):
        spider = DoubanCommentSpider(url,'spider {}'.format(i + 1),'./datas/tenet.csv').start()
    
    
    
