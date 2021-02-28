import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent

ua = UserAgent()

headers = {
    'Cookie':'换上自己的cookie',
    'User-Agent': ua.random
}

def getMovies(url='https://maoyan.com/'):
    """
    获取当前热映电影movieid与名字
    """
    movies = {}
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content,'lxml',from_encoding='utf-8')
    # 获取热映电影所在的模块
    movie_items = soup.find('dl',attrs={'class':'movie-list'}).find_all('div',attrs={'class':'movie-item'})
    # 遍历获取每部电影名字和movieid
    for movie_item in movie_items:
        id = movie_item.find('a').get('href').replace('/films/','')
        name = movie_item.find('img',attrs={'class':'movie-poster-img'}).get('alt').replace('电影海报','')
        counts = getMovieCommentNumbers(id)
        print(id,name)
        movies[name] = [id,counts]
    return movies


def getMovieCommentNumbers(movieid):
    """
    获取当前电影的评论数
    注意该页面有时候可能需要验证一下，只需要点开url进行验证即可
    """
    url = ' https://m.maoyan.com/review/v2/comments.json?movieId={}&userId=-1&offset=0&limit=15&ts=0&type=3'.format(movieid)
    print(url)
    response = requests.get(url,headers=headers)
    js_data = json.loads(response.text)
    total = js_data['data']['total']
    return int(total)    

if __name__ == "__main__":
    getMovies()
