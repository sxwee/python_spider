import pandas as pd

def groupByProvince(data):
    """
    功能：按省市分组
    """
    group = data.loc[:,['univNameCn','province']].groupby("province").count()
    cities,counts = group.index.tolist(),group.loc[:,['univNameCn']].values.flatten().tolist()
    # print(cities,counts)
    return cities,counts

def avgScoreOfProVince(data):
    """
    功能：求取各省市上榜高校的平均得分
    """
    group = data.loc[:,['score','province']].groupby("province").mean()
    group.sort_values(by=['score'],inplace=True)
    cities,avg_scores = group.index.tolist(),group.loc[:,['score']].values.flatten().tolist()
    # print(cities,avg_score)
    return cities,avg_scores


if __name__ == "__main__":
    data_path = r"datas\bcur_2021.csv"
    data = pd.read_csv(data_path)
    # groupByProvince(data)
    avgScoreOfProVince(data)