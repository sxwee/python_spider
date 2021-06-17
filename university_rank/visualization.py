from pyecharts import options as opts
from pyecharts.charts import Map,Bar
from pyecharts.faker import Faker
import pandas as pd
from statistics import groupByProvince,avgScoreOfProVince

data_path = r"datas\bcur_2021.csv"
data = pd.read_csv(data_path)

def drawCountMap():
    """
    功能：绘制各省市大学数量地图
    """
    cities,counts = groupByProvince(data)
    c = (
    Map()
    .add(
            "大学",
            [list(z) for z in zip(cities, counts)],
            "china",
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="中国2021软科排名主榜上榜高校各省市分布数量图"),
            visualmap_opts=opts.VisualMapOpts(
                is_piecewise=True,
                pieces=[
                    {"min": 0, "max": 0, "label": "0所"},
                    {"min": 1, "max": 5, "label": "1-5所"},
                    {"min": 6, "max": 9, "label": "6-9所"},
                    {"min": 10, "max": 15, "label": "10-15所"},
                    {"min": 16, "max": 19, "label": "16-19所"},
                    {"min": 20, "max": 25, "label": "20-25所"},
                    {"min": 26, "max": 29, "label": "26-39所"},
                    {"min": 30, "label": "30所以上"},
                ],
            ),
        )
        .render("map_china_cities.html")
    )

def drawAvgScoreBar():
    """
    功能：绘制各省市上榜高校的平均得分直方图
    """
    cities,avg_scores = avgScoreOfProVince(data)
    avg_scores = [round(s,1) for s in avg_scores]
    b = (
        Bar(init_opts=opts.InitOpts(height="700px"))
        .add_xaxis(cities)
        .add_yaxis('平均分数', avg_scores,category_gap="30%")
        .reversal_axis()
        .set_series_opts(label_opts=opts.LabelOpts(position='right'))
        .set_global_opts(
            title_opts=opts.TitleOpts(title='中国各省市软科上榜大学平均得分直方图'),
            yaxis_opts=opts.AxisOpts(name='省份'),
            xaxis_opts=opts.AxisOpts(name='平均得分'),
        )
        .render('bar_china_cities.html')
    )

if __name__ == "__main__":
    # drawCountMap()
    drawAvgScoreBar()
