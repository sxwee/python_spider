import os
import matplotlib.pyplot as plt
import pandas as pd
from chinese_process import LoadStopWords,Cutter
from wordcloud import WordCloud

def loadData(fn):
    """
    加载某个电影数据
    fn：文件名
    """
    return pd.read_csv('datas/{}'.format(fn))

def WordCloudImage(fn,content):
    """
    功能：生成词云图
    file_path：评论文件路径
    """
    wc = WordCloud(font_path="../simhei.ttf",background_color='white',collocations=False)
    wc.generate(content)
    wc.to_file('images/{}.png'.format(fn))



if __name__ == '__main__':
    data = loadData('comments.csv')
    stop_words = LoadStopWords()
    comments = data['user_c'].values.tolist()
    cut_string = Cutter(comments,stop_words)
    WordCloudImage('评论词云图',cut_string)