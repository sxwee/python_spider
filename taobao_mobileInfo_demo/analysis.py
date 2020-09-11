import pandas as pd
import matplotlib.pyplot as plt


def Countmobsales(mdata):
    """
    功能：统计各种类型手机售卖窗口数
    mdata：手机数据列表，数据格式为[手机名(手机型号),价格,店铺地址,店铺名]
    """
    #用来统计手机型号和售卖店铺数
    mobsales = {
        '华为':0,
        'VIVO':0,
        'OPPO':0,
        '小米':0,
        '苹果':0,
        '三星':0,
        '中兴':0,
        '魅族':0,
        '一加':0,
        '其他':0
    }
    for mtype in mdata:
        mobname,sales = mtype[0].lower(),int(mtype[-1]) #将手机名中的英文转为小写
        if '华为' in mobname or '荣耀' in mobname:
            mobsales['华为'] += sales
        elif 'vivo' in mobname or 'iqoo' in mobname:
            mobsales['VIVO'] += sales
        elif 'oppo' in mobname:
            mobsales['OPPO'] += sales
        elif '小米' in mobname or '红米' in mobname:
            mobsales['小米'] += sales
        elif '苹果' in mobname or 'apple' in mobname:
            mobsales['苹果'] += sales
        elif '三星' in mobname:
            mobsales['三星'] += sales
        elif '中兴' in mobname:
            mobsales['中兴'] += sales
        elif '魅族' in mobname:
            mobsales['魅族'] += sales
        elif '一加' in mobname:
            mobsales['一加'] += sales
        else:
            print(mtype)
            mobsales['其他'] += sales
    print(mobsales)
    return mobsales

def DataVisVisualization(mobsales):
    """
    功能：对各厂家手机及其售卖窗口数绘制直方图进行展示
    mobsales：[厂家,售卖窗口数]
    """
    mobsales = sorted(mobsales.items(),reverse = True,key = lambda x:x[1])
    mobx,moby = [],[]
    for mobsale in mobsales:
        mobx.append(mobsale[0])
        moby.append(mobsale[1])
    plt.rcParams['font.sans-serif']=['SimHei']#正确显示中文l   
    plt.bar(x=mobx,height=moby)
    plt.title('淘宝手机厂家售卖数')
    plt.xlabel('厂家')
    plt.ylabel('售卖数')
    plt.savefig('mobsales.png')
    plt.show()

if __name__ == "__main__":
    mdata = pd.read_csv('mobile_info.csv').values.tolist()
    mobsales = Countmobsales(mdata)
    DataVisVisualization(mobsales)