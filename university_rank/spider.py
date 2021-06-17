import requests
import traceback
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)

headers = {
    "user-agent":ua.chrome
}

def getJSON(url):
    """
    功能：获取JSON数据
    url：待爬取的url
    """
    response = requests.get(url,headers=headers)
    if response.status_code == 200:
        return response
    return None

def saveJSONFile(response,year):
    """
    功能：保存JSON格式的大学排名数据
    resposne：请求响应的数据
    year：爬取的年份
    """
    with open('datas/bcur_{}.json'.format(year),'wb') as fp:
        fp.write(response.content)


def main(start_year=2015,end_year=2021):
    """
    功能：爬虫主函数
    start_year,end_year：爬取的开始年份和结束年份
    """
    try:
        for year in range(start_year,end_year + 1):
            print("clawing {} year university rank datas".format(year))
            url = "https://www.shanghairanking.cn/api/pub/v1/bcur?bcur_type=11&year={}".format(year)
            response = getJSON(url)
            if response:
                saveJSONFile(response,year)
    except Exception:
        traceback.print_exc()

if __name__ == "__main__":
    main()