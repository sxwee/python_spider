import os
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib import cm
from chinese_process import LoadStopWords,Cutter
from wordcloud import WordCloud

def loadData(fn):
    """
    加载某个电影数据
    fn：文件名
    """
    return pd.read_csv('datas/{}'.format(fn))

def scoreDistribution(df):
    """
    获取评分及评分人数
    df：dataframe形式数据
    """
    mdata = df[['score','id']].groupby('score').count()
    score_nums = mdata['id'].tolist()[6:]
    labels = mdata.index.tolist()[6:]
    # 合并5分以下的
    score_nums.insert(0,mdata.loc[0:5,:].sum().values.item())
    labels.insert(0,'0~5')
    return score_nums,labels

# def autolable(rects):
#     """
#     绘制柱形图的值
#     """
#     for rect in rects:
#         height = rect.get_height()
#         if height>=0:
#             plt.text(rect.get_x()+rect.get_width()/2.0 - 0.3,height + 10,'{}'.format(height))
#         else:
#             plt.text(rect.get_x()+rect.get_width()/2.0 - 0.3,height - 10,'{}'.format(height))
#             # 如果存在小于0的数值，则画0刻度横向直线
#             plt.axhline(y=0,color='black')

# def drawBar(fn,x,height):
#     """
#     绘制条形图
#     """
#     map_vir = cm.get_cmap(name='inferno')
#     colors = map_vir(height)
#     fig = plt.figure()
#     ax = plt.bar(x,height,color=colors,edgecolor='black')
#     autolable(ax)
#     plt.savefig('images/{}直方图.png'.format(fn))

def drawPie(fn,x,labels):
    """
    绘制圆环图
    """
    plt.figure()
    plt.pie(score_nums,labels=labels,wedgeprops=dict(width=0.3, edgecolor='w'),autopct='%1.1f%%',pctdistance=0.85)
    plt.savefig('images/{}圆环图.png'.format(fn))

def WordCloudImage(fn,content):
    """
    功能：生成词云图
    file_path：评论文件路径
    """
    wc = WordCloud(font_path="../simhei.ttf",background_color='white',collocations=False,
    width=600,height=300,max_words=100)
    wc.generate(content)
    wc.to_file('images/{}词云图.png'.format(fn))



if __name__ == '__main__':
    for fn in os.listdir('datas/'):
        fn = fn.replace('.csv','')
        data = loadData('{}.csv'.format(fn))
        score_nums,labels = scoreDistribution(data)
        # drawBar(fn,labels,score_nums)
        drawPie(fn,score_nums,labels)
        stop_words = LoadStopWords()
        comments = data['content'].values.tolist()
        cut_string = Cutter(comments,stop_words)
        WordCloudImage(fn,cut_string)