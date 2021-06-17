import jieba
import re

chinese = '[\u4e00-\u9fa5]+' #提取中文汉字的pattern


def LoadStopWords(file_path ='./datas中文停用词词表.txt'):
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

def Cutter(comment_list):
    """
    功能：中文分词主函数
    comment_list：评论列表
    stop_words：中文停用词表
    """
    stop_words = LoadStopWords()
    cut_string = "" #分词结果字符串
    for comment in comment_list:
        comment = "".join(re.findall(chinese,comment))
        if comment != "":
            seg_list = jieba.cut(comment)
            comment = " ".join(DeleteStopWrods(seg_list,stop_words))
            cut_string += comment + ' '
    
    return cut_string



if __name__ == "__main__":
    pass