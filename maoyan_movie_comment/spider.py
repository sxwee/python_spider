import json
import time
import random
import requests
import traceback
import pandas as pd
from fake_useragent import UserAgent
from get_hit_movieid import getMovies,headers
from proxy_ip import ExtractIP
import threading

ua = UserAgent()

class MaoYanSpider(threading.Thread):
    def __init__(self,movie_name,movieId,nums,threadname,IPs=None,append=False) -> None:
        threading.Thread.__init__(self, name=threadname)
        self.movieId = movieId
        self.nums = nums
        self.movie_name = movie_name
        self.IPs = IPs
        self.append = append
    
    def run(self):
        """
        爬虫主程序
        self.movieId：待爬取电影的id
        self.nums：待爬取的页数
        self.IPs：代理IP列表
        """
        clist = []
        t = self.nums // 15
        for i in range(nums):
            try:
                print('{} is clawling the {}st page'.format(self.getName(),i + 1))
                ts = time.time()
                url = 'https://m.maoyan.com/review/v2/comments.json?movieId={}&userId=-1&offset={}&limit=15&ts={}&type=3&optimus_uuid=CDD8C6B0775A11EB869539E04D007BD066D8CA91D8354B5C9BE678701804B84C&optimus_risk_level=71&optimus_code=10'\
                        .format(self.movieId,i*15,int(ts*1000))
                # print(url)
                # 设置代理IP
                if self.IPs is not None:
                    index = random.randint(0,len(self.IPs) - 1)
                    proxies =  {"http":"{}:8080".format(self.self.IPs[index])}
                    response = requests.get(url=url,headers=headers,proxies=proxies)
                else:
                    proxies =  {"http":"{}:8080".format('41.207.251.198')}
                    response = requests.get(url=url,headers=headers,proxies=proxies)
                # with open('temp.html','w',encoding='utf-8') as fp:
                #     fp.write(response.text)
                outcome = self.phrase(response.text)
                # 爬取空列表则停止（猫眼爬虫有条数限制）
                if outcome == []:break
                clist += outcome
                time.sleep(1.5)
            except Exception:
                traceback.print_exc()
                pass
        
        self.Saver(clist,self.append)


    def phrase(self,data):
        """
        解析获取的影评数据(json格式)
        data：文本数据
        """
        outcome = []
        js_data = json.loads(data)
        comments = js_data.get('data').get('comments')
        if comments != None:
            for comment in comments:
                id = comment.get('id') # 电影ID
                content = comment.get('content')  # 评论的内容
                nick = comment.get('nick') # 评论人的昵称
                score = comment.get('score') # 评论的分数
                startTime = comment.get('startTime')  # 开始时间
                print(id,content,nick,score,startTime)
                outcome.append([id,content,nick,score,startTime])
        return outcome


    def Saver(self,clist,append=False):
        """
        功能：保存评论为csv文件
        clist：获取的数据
        append：是否为追加文件到原有的文件中去
        """
        datas = pd.DataFrame(clist,columns=['id','content','nick','score','startTime'])
        if append:
            datas.to_csv('datas/{}.csv'.format(self.movie_name),index=False,header=False,mode='a')
        else:
            datas.to_csv('datas/{}.csv'.format(self.movie_name),index=False)

if __name__ == "__main__":
    movies = getMovies()
    IPs = ExtractIP()
    IPs = None if IPs == [] else IPs
    i = 1
    for k,v in movies.items():
        movie_name = k
        movieId,nums = v[0],v[1]
        print(movie_name,'\t',movieId,'\t',nums)
        threadname = 'spider{}'.format(i)
        spider = MaoYanSpider(movie_name,movieId,nums,threadname,IPs,append=True).start()
        i += 1
