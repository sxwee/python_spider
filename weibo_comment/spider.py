import json
import time
import requests
from fake_useragent import UserAgent
import pandas as pd
import random
from proxy_ip import extractIP
import traceback
import re
import os

requests.packages.urllib3.disable_warnings()

ua = UserAgent()

headers = {
    "Host": "m.weibo.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "MWeibo-Pwa": "1",
    "X-XSRF-TOKEN": "da898d",
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": ua.chrome,
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://m.weibo.cn/detail/4614060694573362",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Cookie": "换上自己登陆微博的cookie"
}


def parse(text):
    """
    功能：解析json数据
    text：待解析的文本内容
    """
    comments,max_id = [],None
    js_data = json.loads(text)
    datas = js_data.get('data')
    if datas:
        contents = datas.get('data')
        # 获取json末尾的max_id
        max_id = datas.get('max_id')
        for content in contents:
            # 获取用户名
            user_na = content.get('user').get('screen_name')
            # 获取评论内容
            user_c = content.get('text')
            # 筛选掉评论内容中的部分html代码
            if '<span' in user_c:
                user_c = re.search('(.?)<span .*',user_c).group(1)
            # 去掉评论中的空格
            user_c = user_c.replace('　','')
            # 获取评论时间
            t = content.get('created_at')
            print(user_na,user_c,t)
            comments.append([user_na,user_c,t])
    return comments,max_id

def Spider(comment_counts,weibo_id,IPs=None):
    """
    爬虫主程序
    wb_id待爬取的微博的id
    comment_counts：评论数
    IPs：代理IP列表
    """
    clist,max_id = [],None
    # 获取需要爬取的页数
    lengh = comment_counts // 20
    session = requests.Session()
    # max_id_type的值
    flag = 0
    fail_nums = 0
    for i in range(1,lengh + 1):
        # 10次获取json数据失败则退出爬虫程序
        if fail_nums >= 10:break
        try:
            if i == 1:
                # 首个json评论数据没有max_id字段
                url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id_type=0".format(weibo_id,weibo_id)
            else:
                url = "https://m.weibo.cn/comments/hotflow?id={}&mid={}&max_id={}&max_id_type={}".format(weibo_id,weibo_id,max_id,flag)
            time.sleep(3.5)
            print("clawing {}st pages：{}".format(i,url))
            if IPs is not None:
                index = random.randint(0,len(IPs) - 1)
                proxies =  {"http":"{}:8080".format(IPs[index])}
                response = session.get(url=url,headers=headers,proxies=proxies,verify=False)
            else:
                response = session.get(url=url,headers=headers,verify=False)
            comments,cur_id = parse(response.text)
            if cur_id == None:
                flag = 1
                fail_nums += 1
            else:
                flag = 0
                max_id = cur_id 
            clist += comments
        except Exception:
            print("clawing {}st page failed".format(i))
            traceback.print_exc()
    session.close()
    Saver(clist,'comments.csv')

def Saver(clist,file_name):
    """
    功能：保存评论为csv文件
    clist：获取的数据
    append：是否为追加文件到原有的文件中去
    """
    datas = pd.DataFrame(clist,columns=["user_na","user_c","t"])
    file_path = "datas/{}".format(file_name)
    if os.path.exists(file_path):
        datas.to_csv(file_path,index=False,header=False,mode="a")
    else:
        datas.to_csv(file_path,index=False)

if __name__ == "__main__":
    # 微博列表，内容为id:评论条数
    weibo_list = {
        '4614060694573362':900,
        '4614186683074288':700,
        '4614208131958609':1500
    }
    # 抓取代理IP
    IPs = extractIP()
    print(IPs)
    if IPs == []:IPs = None
    # 爬取微博列表中的微博所对应的评论
    for weibo_id,comment_counts in weibo_list.items():
        Spider(comment_counts,weibo_id,IPs=IPs)