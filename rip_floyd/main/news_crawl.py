from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.common.exceptions import NoSuchElementException, TimeoutException,StaleElementReferenceException
import urllib.request
import requests
from datetime import datetime 



class Result_node():

    def __init__(self,title,article_url, img_url, time_stamp):
        self.title = title
        self.img_url = img_url
        self.article_url = article_url
        self.time_stamp = time_stamp

def croller():

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')


    driver = webdriver.Chrome('C:/Users/acepi/Desktop/chromedriver.exe', chrome_options = chrome_options) # 로컬에서 돌릴때

    driver.get("https://news.google.com/search?q=george%20floyd%20when%3A1h&hl=en-US&gl=US&ceid=US%3Aen")
    
    i = 1
    result_node_list = []
    while True:
        try:
            title = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[2]/div/main/c-wiz/div[1]/div['+str(i)+']/div/article/h3/a')
                                                  
            title_text = title.text
            article_url = title.get_attribute('href')
            
            try:
                img = driver.find_element_by_xpath('//*[@id="i'+str(i*2+2)+'"]')
                img_url = img.get_attribute('src')
            except NoSuchElementException:
                img_url = 'https://lh3.googleusercontent.com/proxy/qUWcPEtEgcLr9DPHg2uBiDZAckW0rXY_ItHyi9gchZ6NYm0FZORlJu_o-1cbpHQ4jL5f8oSgwMCAO-pJwN-6Quj9'
            now = datetime.now()
            time_stamp = now.strftime("%Y-%m-%d-%H")
            news_obj = Result_node(title_text,article_url,img_url,time_stamp)
            result_node_list.append(news_obj)
            i = i+1
        except NoSuchElementException:
            break
        
    return result_node_list


