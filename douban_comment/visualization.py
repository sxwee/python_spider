import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from chineseProcess import Cutter
import PIL.Image as image
import numpy as np

def loadDataset(filepath='tenet.csv'):
    """
    功能：加载评论数据
    """
    return pd.read_csv(filepath,names=['reviewer','star','comment'])

def rankBar(df):
    """
    功能：绘制评分直方图
    """
    group = df[['star','reviewer']].groupby('star').count()
    x,y = group.index.tolist(),group.values.flatten().tolist()
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.bar(x,y)
    plt.xlabel('评分')
    plt.ylabel('人数')
    plt.savefig('./images/rankBar.png')
    plt.show()

def wordcloudImage(string):
    """
    功能：绘制词云图
    """
    mask = np.array(image.open('./images/tenet.jpg'))
    wc = WordCloud(font_path='C:/Users/wl/OldPC/WordCloud_Font/simhei.ttf',mask=mask,background_color='white',collocations=False)
    wc.generate(string)
    wc.to_file('./images/wordcloudImage.png')
    plt.imshow(wc)
    plt.show()

if __name__ == "__main__":
    df = loadDataset()
    rankBar(df)
    comment_list = df[['comment']].values.flatten().tolist()
    string = Cutter(comment_list)
    wordcloudImage(string)