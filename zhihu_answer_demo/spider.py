import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import traceback

chinese = '[\u4e00-\u9fa5]+' #提取中文汉字的pattern

headers = {
    'user-agent': '换上自己的User-Agent',
    'cookie': '换上自己的知乎登录cookie'
}

def getHots(url='https://www.zhihu.com/hot'):
    """
    功能：获取知乎热榜所有话题的id
    """
    topics = []
    response = requests.get(url=url,headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content,'lxml',from_encoding='utf-8')
        hots = soup.findAll('section',attrs={'class':'HotItem'})
        for hot in hots:
            hot_url = hot.find('a').get('href')
            hot_c = hot.find('a').get('title')
            print(hot_c,hot_url)
            topics.append([hot_c,hot_url])
    Saver(topics,0,['title','url'])
    return topics

def getNumber(topic_url):
    """
    功能：获取某个问题的回答数
    """
    response = requests.get(topic_url,headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content,'lxml',from_encoding='utf-8')
        string = soup.find('h4',attrs={'class':'List-headerText'}).get_text()
        number = ''.join([s for s in string if s.isdigit()])
        return int(number)
    
    return 0

def getAnswers(question_id,number):
    """
    功能：获取某个问题各个回答
    question_id：话题id
    number：回答数量
    """
    outcome = []
    i = 0
    while i * 5 < number:
        try:
            url = 'https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset={}&platform=desktop&sort_by=default'.format(question_id,i*5)
            response = requests.get(url,headers=headers)
            if response.status_code == 200:
                js = json.loads(response.text)
                for answer in js['data']:
                    author = answer['author']['name']
                    content = ''.join(re.findall(chinese,answer['content']))
                    print(author,content)
                    outcome.append([author,content])
            i += 1
        except Exception:
            i += 1
            print(traceback.print_exc())
            print('web spider fails')
    return outcome


def Saver(datas,idx,columns):
    """
    功能：保存数据为csv格式
    index：话题索引
    """
    df = pd.DataFrame(datas,columns=columns)
    df.to_csv('./datas/hot_{}.csv'.format(idx),index=False)



def Spider():
    """
    功能：爬虫主函数
    """
    topics = getHots()
    for idx,topic in enumerate(topics):
        print('clawling: {} numbers: {}'.format(topic[0],topic[1]))
        question_id = topic[1].split('/')[-1]
        number = getNumber(topic[1])
        datas = getAnswers(question_id,number)
        Saver(datas,idx + 1,['author','content'])

if __name__ == "__main__":
    Spider()
