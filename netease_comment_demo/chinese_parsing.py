import pandas as pd
import matplotlib.pyplot as plt
import jieba
import re
from sklearn.feature_extraction.text import CountVectorizer

chinese = '[\u4e00-\u9fa5]+' #提取中文汉字的pattern

def LoadComments(file_path="无滤镜评论.csv"):
    """
    功能：加载csv文件中的评论为评论列表
    file_path：csv文件路径
    """
    datas = pd.read_csv(file_path)
    comment_list = datas['评论内容'].values.tolist()
    
    return comment_list


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

def Cutter(comment_list,stop_words):
    """
    功能：中文分词主函数
    comment_list：评论列表
    stop_words：中文停用词表
    """
    cut_string = "" #分词结果字符串
    for comment in comment_list:
        comment = "".join(re.findall(chinese,comment))
        if comment != "":
            seg_list = jieba.cut(comment)
            comment = " ".join(DeleteStopWrods(seg_list,stop_words))
            cut_string += comment + ' '
    
    return cut_string

def WordFrequence(cut_string):
    """
    功能：获取词频
    cut_string：分词后的字符串
    """
    vc = CountVectorizer()
    X = vc.fit_transform([cut_string])
    word = vc.get_feature_names()
    freq = X.toarray().tolist()
    word_freq = [item for item in zip(word,freq[0])] #获取单词对应的词频
    word_freq.sort(reverse=True,key=lambda x:x[1]) #按词频降序排序
    
    return word_freq

def WordFrequenceBar(word_freq):
    """
    功能：生成词频直方图
    word_freq：词及频率
    """
    top = word_freq[:10]
    data = pd.DataFrame(top,columns=['word','freq'])
    x,y = data['word'].values.tolist(),data['freq'].values.tolist()
    plt.rcParams['font.sans-serif']=['SimHei']#正确显示中文l
    color = [(1 - 0.03 * l, 0, 0) for l in range(10)] #设置不同柱形不同颜色
    plt.barh(x[::-1],y[::-1],color=color[::-1])
    plt.title('无滤镜热词top10')
    plt.xlabel('word')
    plt.ylabel('freq')
    plt.savefig('热词直方图.png')
    plt.show()

def main():
    """
    功能：完成中文分词，词频直方图的绘制
    """
    #加载评论数据
    comment_list = LoadComments()
    #加载停用词表
    stop_words = LoadStopWords()
    #分词
    cut_string = Cutter(comment_list,stop_words)
    #获取词频
    word_freq = WordFrequence(cut_string)
    #生成词频直方图
    WordFrequenceBar(word_freq)


if __name__ == "__main__":
    main()