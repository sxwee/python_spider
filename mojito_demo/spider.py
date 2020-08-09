from wordcloud import WordCloud
import requests
import json
import regex
import jieba
import traceback

chinese = '[\u4e00-\u9fa5]+' #提取中文汉字的pattern
root_url = "https://c.y.qq.com/base/fcgi-bin/fcg_global_comment_h5.fcg"

querystring = {
    "g_tk_new_20200303": "5381",
    "g_tk": "5381",
    "loginUin": "0",
    "hostUin": "0",
    "format": "json",
    "inCharset": "utf8",
    "outCharset": "GB2312",
    "notice": "0",
    "platform": "yqq.json",
    "needNewCode": "0",
    "cid": "205360772",
    "reqtype": "2",
    "biztype": "1",
    "topid": "268352018",
    "cmd": "8",
    "needmusiccrit": "0",
    "pagenum": "0",
    "pagesize": "25",
    "lasthotcommentid": "song_268352018_1663008688_1596070398_1335842063_1596080731",
    "domain": "qq.com",
    "ct": "24",
    "cv": "10101010"
}

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
        Chrome/84.0.4147.105 Safari/537.36"
}

proxies = {
    'http':'116.12.74.81:8080', 
    'http':'176.101.89.226:8080', 
    'http':'207.182.135.52:8080', 
    'http':'27.72.29.159:8080', 
    'http':'27.72.29.159:8080', 
    'htpp':'95.78.174.219:8080'
}

def LoadStopWords(file_path = '中文停用词词表.txt'):
    """
    功能：加载中文停用词列表
    file_path：停用词表所在路径
    """
    stopwords = []
    with open(file_path,'r') as f:
        text = f.readlines()
        for line in text:
            stopwords.append(line[:-2])#去换行符
    return stopwords

def DeleteStopWrods(g_list,stop_words):
    """
    功能：删除中文停词
    g_lst：分词结果
    stop_words：分词结果
    """
    outcome = []
    for term in g_list:
        if term not in stop_words:
            outcome.append(term)
    return outcome

def Spider(stop_words,nums = 5118):
    """
    功能：爬虫主程序
    stop_words：中文停用词表
    nums：评论占用的页数
    返回值：clist，即评论列表
    """
    pagenum,lasthotcommentid = 0,"song_268352018_1663008688_1596070398_1335842063_1596080731" #初始化参数
    clist = [] #保存评论的列表
    while pagenum < nums:
        try:
            print("正在爬取第{}页".format(pagenum + 1))

            querystring["pagenum"] = str(pagenum)
            querystring["lasthotcommentid"] = lasthotcommentid
            response = requests.get(url=root_url,headers=headers,params=querystring,proxies=proxies)
            commentlist = json.loads(response.text)["comment"]["commentlist"] 
            
            if response.status_code == 200:#成功响应
                pagenum += 1
                lasthotcommentid = commentlist[-1]["commentid"]
                for item in commentlist:
                    c_org = item.get("rootcommentcontent")
                    if c_org == "该评论已经被删除":
                        continue
                    #只提取中文
                    comment = "".join(regex.findall(chinese,c_org)) if c_org != None else ""
                    seg_list = jieba.cut(comment) #jieba分词
                    comment = " ".join(DeleteStopWrods(seg_list,stop_words))
                    #print(comment)
                    clist.append(comment + " ")

        except Exception:
            print("第{}页爬取失败!!!".format(pagenum))
            traceback.print_exc()
        
    return clist
        
        

def Saver(clist,save_path = "mojito.txt"):
    """
    功能：评论为txt文件
    clist：评论列表
    save_path：保存文件路径
    """
    with open(save_path,'w',encoding="UTF-8") as f:
        f.writelines(clist)

def WordCloudImage(file_path='mojito.txt'):
    """
    功能：生成词云图
    file_path：评论文件路径
    """
    wc = WordCloud(font_path="E:\WordCloud_Font\simhei.ttf",background_color='white',collocations=False,
    width=600,height=300,max_words=100)
    with open(file_path,'r',encoding='UTF-8') as f:
        string = f.read()
        wc.generate(string)
        wc.to_file('wc_mojito.png')

if __name__ == "__main__":
    #stop_words = LoadStopWords()
    #clist = Spider(stop_words)
    #Saver(clist)
    WordCloudImage()

