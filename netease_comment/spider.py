from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

#开启万花筒模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=options)
WAIT = WebDriverWait(driver,10)


def ParseComment(element_list):
    """
    功能：提取网页中的评论
    element_list：包含评论的div元素块集合
    """
    clist = []
    for c in element_list:
        text = c.text
        idx = text.find('：')
        print(text[idx + 1:])
        clist.append(text[idx + 1:])
    
    return clist

def NextPage():
    """
    功能：获取下一页评论
    page_num：当前评论页
    """
    try:
        next_button = WAIT.until(EC.element_to_be_clickable((By.XPATH,'//a[starts-with(@class,"zbtn znxt js-n-")]')))
        driver.execute_script('arguments[0].click();', next_button)
        element_list = WAIT.until(EC.presence_of_all_elements_located((By.XPATH,'//div[@class="cnt f-brk"]')))
        
        return element_list
    except TimeoutException:
        # traceback.print_exc()
        driver.refresh()
        NextPage()


def Spider(page_nums = 623,url="https://music.163.com/#/song?id=1466053895"):
    """
    功能：爬虫主程序
    page_nums：评论总页数
    url：爬取歌曲链接
    """
    i,comments = 2,[]
    driver.get(url)
    driver.switch_to.frame('g_iframe')
    element_list  = driver.find_elements_by_xpath('//div[@class="cnt f-brk"]')
    comments += ParseComment(element_list )
    try:
        while i <= page_nums:
            print('-------------Crawing page {}---------------'.format(i))
            element_list = NextPage()
            comments += ParseComment(element_list)
            i += 1
    finally:
        driver.close()
    
    return comments      

def Saver(comments,file_path = '无滤镜评论.csv'):
    """
    功能：保存评论为csv文件
    comments：评论列表
    """
    datas = pd.DataFrame(comments,columns=['评论内容'])
    datas.to_csv(file_path,index=False)

if __name__ == "__main__":
    comments = Spider()
    Saver(comments)