import os
import json
import pandas as pd

def getJSONFiles(data_dir):
    """
    """
    for root,_,files in os.walk(data_dir):
        for fn in files:
            if not fn.endswith(".json"):continue
            with open(os.path.join(root,fn),'r',encoding='utf-8') as fp:
                js_data = json.load(fp)
                yield fn,js_data

def parseJSON(data_dir):
    """
    功能：解析JSON数据并提取内容
    提取内容包括[univNameCn,univNameEn,univTags,univCategory,province,score,ranking]
    """
    for fn,js_datas in getJSONFiles(data_dir):
        print("==========parse {}==========".format(fn))
        data = []
        for js_data in js_datas['data']['rankings']:
            univNameCn = js_data.get('univNameCn') # 中文名
            univNameEn = js_data.get('univNameEn') # 英文名
            univTags = js_data.get('univTags') # 标签
            univTags = " ".join(univTags) if univTags else ""
            univCategory = js_data.get('univCategory') # 类型
            province = js_data.get('province') # 省市
            score = js_data.get('score') # 总分
            ranking = int(js_data.get('ranking')) # 排名
            # print(univNameCn,univNameEn,univTags,univCategory,province,score,ranking)
            data.append([univNameCn,univNameEn,univTags,univCategory,province,score,ranking])
        saveToCSV(data,fn.replace(".json",".csv"))
            
def saveToCSV(data,filename):
    """
    功能：保存提取的内容到CSV文件
    data：提取的内容
    filename：保存的文件名
    """
    df = pd.DataFrame(data,columns=['univNameCn','univNameEn','univTags','univCategory','province','score','ranking'])
    df.to_csv("datas/{}".format(filename),index=False)

if __name__ == "__main__":
    parseJSON('datas/')