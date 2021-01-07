from wordcloud import WordCloud
import pandas as pd
import jieba

def LoadStopWords(file_path = '中文停用词词表.txt'):
    """
    功能：加载中文停用词列表
    file_path：停用词表所在路径
    """
    stopwords = []
    with open(file_path,'r',encoding='utf-8') as f:
        text = f.readlines()
        for line in text:
            stopwords.append(line[:-1])#去换行符
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


def WordCloudImage(string,sava_path):
    """
    功能：生成词云图
    string：分词并删除停用词后的回答
    """
    wc = WordCloud(font_path="E:\WordCloud_Font\simhei.ttf",background_color='white',collocations=False,
    width=800,height=400,max_words=150)
    wc.generate(string)
    wc.to_file(sava_path)

def Processing(file_path='./datas/hot_'):
    """
    功能：处理主程序
    file_path：回答路径
    """
    stop_words = LoadStopWords()
    string = ''
    for i in range(1,51):
        df = pd.read_csv('./datas/hot_{}.csv'.format(i))
        df.dropna(inplace=True)
        string = ''
        for answer in df['content']:
            seg_list = jieba.cut(answer)
            answer = " ".join(DeleteStopWrods(seg_list,stop_words))
            string += answer + ' '
        WordCloudImage(string,'./wordCloudImage/hot_{}.png'.format(i))


if __name__ == "__main__":
    Processing()