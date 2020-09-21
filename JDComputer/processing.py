import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('./JDComputer/ComputerInfo.csv',names=['pctype','price','shop'],
    dtype={'pctype':str,'price':float,'shop':str})

def DropDuplicates(data):
    """
    功能：清除重复行
    data：DataFrame
    """
    #print(data.duplicated().sum())
    data.drop_duplicates(inplace=True)

def PriceSeg(price):
    """
    功能：对价格范围分段
    price：1-D array
    """
    bins=[0,3000,6000,10000,60000]
    return pd.cut(price,bins)

def GroupAndVisualize(data):
    """
    功能：分组统计各个价格段的电脑类型并进行可视化
    data：DataFrame
    """
    plt.rcParams['font.sans-serif']=['SimHei']
    group = data[['price','segs']].groupby('segs').count()
    plt.title('笔记本电脑价格区间档')
    plt.pie(x = group['price'],labels=group.index,autopct=r"%1.2f%%")
    plt.savefig('cp_pie.png')
    plt.show()

if __name__ == "__main__":
    #清除重复数据
    DropDuplicates(data)
    #对价格分段
    segs = PriceSeg(data['price'])
    #添加价格区间列
    data['segs'] = segs
    #可视化
    GroupAndVisualize(data)