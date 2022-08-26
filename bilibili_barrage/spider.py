import requests
from bs4 import BeautifulSoup
import re
import traceback
import pandas as pd

headers = {
    "User-Agent": "换上自己的user-agent或用fake-useragent",
    "cookie": "换上自己的cookie"
}

def GainVideoLink(pagenums = 3):
    """
    功能：获取某页的视频链接
    pagenums：视频总页数
    返回值：一个链接列表
    """
    i,vlink = 1,[]
    while i <= pagenums:
        try:
            url = "https://search.bilibili.com/all?keyword=%E7%89%B9%E6%9C%97%E6%99%AE%E7%AD%BE%E7%BD%B2%E8%A1%8C%E6%94%BF%E4%BB%A4&page={}".format(i)
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                i += 1
                soup = BeautifulSoup(response.content,'lxml')
                videos = soup.findAll('li',attrs={"class":"video-item matrix"})

                for video in videos:
                    href = video.find('a').get('href')#获取视频的链接
                    print("http:" + href)
                    vlink.append("http:" + href)
        except Exception:
            print("第{}页视频链接爬取失败".format(i))
            traceback.print_exc()
        
    return vlink

def GainCid(url):
    """
    功能：获取视频的cid
    url：视频的链接
    proxies：代理IP
    返回值：视频的cid
    """
    cid = 0
    try:
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            match_obj = re.search('cid=(\d+)&aid',response.text)
            #print(response.text)
            cid = match_obj.group(1)
            return cid   
    except Exception:
        print("cid获取失败,url:{}".format(url))
        traceback.print_exc()

def GainComment(cid):
    """
    功能：获取对应cid的视频的弹幕
    cid：视频的cid
    返回值：弹幕列表
    """
    clist = [] #弹幕列表
    try:
        url = "http://comment.bilibili.com/{}.xml".format(cid)
        response = requests.get(url,headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content,"lxml",from_encoding="UTF-8")
            comments = soup.findAll('d')
            for c in comments:
                comment = c.get_text()
                clist.append([cid,comment])
        return clist
    except Exception:
        print("弹幕爬取失败,cid:{}".format(cid))
        traceback.print_exc()

def Saver(clist):
    """
    功能：将视频数据保存为csv文件
    clist：弹幕列表
    """  
    datas = pd.DataFrame(clist,columns=['视频cid','弹幕内容'])  
    datas.to_csv('bilibili_comments.csv',index = False)

def Spider():
    """
    功能：爬虫主程序
    IPs：代理IP列表
    """
    comments = []
    vlink = GainVideoLink()
    for i,url in enumerate(vlink):
        print("Crawing Video {},url:{}".format(i + 1,url))
        cid = GainCid(url)
        clist = GainComment(cid)
        if clist != []:
            comments += clist
    Saver(comments)

if __name__ == "__main__":
    Spider()