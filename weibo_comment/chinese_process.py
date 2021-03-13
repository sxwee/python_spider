import re
import jieba
from jieba.finalseg import cut
import pandas as pd

chinese = '[\u4e00-\u9fa5]+' #提取中文汉字的pattern


def LoadStopWords(file_path = '../中文停用词词表.txt'):
    """
    加载中文停用词列表
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
    删除中文停词
    g_lst：分词结果
    stop_words：分词结果
    """
    stop_words.append('博主') # 电影多次出现且意义不大
    outcome = []
    for term in g_list:
        if term not in stop_words:
            outcome.append(term)
    return outcome

def Cutter(comments,stop_words):
    """
    功能：中文分词主函数
    comment_list：评论列表
    stop_words：中文停用词表
    """
    cut_string = "" #分词结果字符串
    for comment in comments:
        comment = "".join(re.findall(chinese,str(comment)))
        if comment != "":
            seg_list = jieba.cut(comment)
            comment = " ".join(DeleteStopWrods(seg_list,stop_words))
            cut_string += comment + ' '
    
    return cut_string

if __name__ == '__main__':
    pass