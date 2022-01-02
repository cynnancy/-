from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *


#導入套件
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time as t
import datetime
import os
from urllib.parse import urljoin
from selenium.webdriver.chrome.options import Options


# 先定義能判別日期的函數(先抓取近當天的新聞)
def distinguish_date(time):    
    time = time.replace('/','-')
    yest = datetime.datetime.now()+ datetime.timedelta(days=-1)
    yest  = yest.strftime("%Y-%m-%d")
    #two_days_before = datetime.datetime.now()+ datetime.timedelta(days=-2)
    #three_days_before = datetime.datetime.now()+ datetime.timedelta(days=-3)
    
    if ( time == datetime.datetime.now().strftime("%Y-%m-%d") ) or ( time == yest  ):
        return True
    else:
        return False

# 開始爬蟲的時間，為了區別每次爬蟲
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# stock = '長榮'
#stock = input()

#中時新聞網
# 定義 更多新聞 按鈕之連結
def get_uri_chinatimes(stock): 
    uri_chinatimes = "https://wantrich.chinatimes.com/" + 'search/' + stock
    return uri_chinatimes
    

# 定義成函數
def get_news_chinatimes(stock):
    title_lis = []
    time_lis = []
    source_lis = []
    author_lis = []
    article_url_lis = []

    # 跑每頁的內容
    page = 1
    while 1:    
        url = "https://wantrich.chinatimes.com/"
        url = url + 'search/' + stock + '/' + str(page)
        re = requests.get(url)
        soup = BeautifulSoup(re.text, "html.parser")
        news = soup.find('ul',{'class':'vertical-list'})
        news = news.findAll('div', {'class':'articlebox-compact'})

        for new in news:  
            new_time = new.find('div', {'class':'meta-info'})
            time = new_time.find('span', {'class':'date'}).text

            if distinguish_date(time) == True :
                new_title = new.find("h3",{'class':'title'})
                title = new_title.text       

                article_url = new.find('a')['href']
                article_url = urljoin(url,article_url)

                #隔頁爬蟲
                re = requests.get(article_url)
                soup = BeautifulSoup(re.text, "html.parser")
                soup = soup.find('div', {'class':'align-items-center'})
                source = soup.find('div',{'class':'source'}).text
                author = soup.find('div',{'class':'author'}).text
                if author == '':
                    author = '(無特定作者)'

                # 確切新聞發布時間
                time = time + '   ' + soup.find('span',{'class':'hour'}).text  

                #
                title_lis.append(title)
                time_lis.append(time)
                source_lis.append(source)
                author_lis.append(author)
                article_url_lis.append(article_url)
                t.sleep(1)
            elif distinguish_date(time) == False :
                break

        if distinguish_date(time) == False :
            break
        page = page + 1

    df = pd.DataFrame({"title":title_lis,"time": time_lis ,"author":author_lis ,"link":article_url_lis})
    return df

# 先定義能判別日期的函數(只抓取近兩天的新聞)
def distinguish_date(time):    
    time = time.replace('/','-')
    yest = datetime.datetime.now()+ datetime.timedelta(days=-1)
    yest  = yest .strftime("%Y-%m-%d")
    if ( time == datetime.datetime.now().strftime("%Y-%m-%d")) or ( time == yest):
        return True
    else:
        return False

# 開始爬蟲的時間，為了區別每次爬蟲
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")

# stock = '長榮'
#stock = input()

#經濟日報
# 定義 更多新聞 按鈕之連結
def get_uri_economy(stock): 
    uri_economy = "https://money.udn.com/search/result/1001/" + stock
    return uri_economy

# 定義成函數
def get_news_economy(stock):
    title_lis = []
    time_lis = []
    author_lis = []
    article_url_lis = []
    
    # 開始爬蟲
    url = "https://money.udn.com/search/result/1001/"
    url = url + stock
    re = requests.get(url)
    soup = BeautifulSoup(re.text, "html.parser")
    news = soup.find('ul',{'class':'story-list-holder'})
    news = news.findAll('div', {'class':'story__content'})

    for new in news:  
        article_url = new.find('a')['href']
        # 隔頁爬蟲
        re = requests.get(article_url)
        soup = BeautifulSoup(re.text, "html.parser")
        time = soup.find('time',{'class':'article-body__time'}).text 
        # time 格式  '%Y/%m/%d %H:%M:%S' 
        time_spli = time.split(" ")
        if distinguish_date(time_spli[0]) == True :
            title = soup.find('h1',{'id':'story_art_title'}).text
            article__url = article_url
            
            # refine author 資訊 
            author = soup.find('div',{'class':'article-body__info'}).find('span').text
            author_spli = author.split("／")
            author_spli =  author_spli[0]
            author_spli = author_spli.split("/")
            author_spli =  author_spli[0].split(" ")
            #source = author_spli[0]
            author = author_spli[1]
            author = author.replace("記者",'')
            author = author.replace("文",'')
            author = author.split("台北")
            author = author[0]
            if author == '':
                author = '(無特定作者)'
            
            
            title_lis.append(title)
            time_lis.append(time)
            author_lis.append(author)
            article_url_lis.append(article__url)
            t.sleep(1)
        elif distinguish_date(time_spli[0]) == False :
            break
        
    df = pd.DataFrame({"title":title_lis,"time": time_lis ,"author":author_lis ,"link":article_url_lis})
    return df

#處理標題過長問題
def title_shorten(words):
    sentence = list(words)
    ans_lst = []
    if len(sentence)>11:
        for i in range(0,11):
            ans_lst.append(sentence[i])
        title = "".join(ans_lst) + "......"
    else:
        title = words
    return title

def news_carousel(stock):
    #經濟
    data_economy = get_news_economy(stock)
    if data_economy.empty == True:
        title_data_economy = ['無近兩天新聞','無近兩天新聞']  # 請參考更多新聞
        link_data_economy = [get_uri_economy(stock), get_uri_economy(stock)]
    elif data_economy.empty != True:
        title_data_economy = []
        link_data_economy = []

        title_data_eco = data_economy.loc[:,'title']
        link_data_eco = data_economy.loc[:,'link']
        for i in title_data_eco:
            title_data_economy.append(i)
        for j in link_data_eco:
            link_data_economy.append(j)
        if len(title_data_economy) <2 :
            string_1 = '近兩天無額外新聞'
            title_data_economy.append(string_1)
            link_data_economy.append(get_uri_economy(stock))

    #中時
    data_chinatimes = get_news_chinatimes(stock)
    if data_chinatimes.empty == True:
        title_data_chinatimes = ['近兩天無額外新聞','近兩天無額外新聞']  # 請參考更多新聞
        link_data_chinatimes = [get_uri_chinatimes(stock), get_uri_chinatimes(stock)]
    elif data_chinatimes.empty != True:
        title_data_chinatimes = []
        link_data_chinatimes = []

        title_data_ = data_chinatimes.loc[:,'title']
        link_data_ = data_chinatimes.loc[:,'link']
        for i in title_data_:
            title_data_chinatimes.append(i)
        for j in link_data_:
            link_data_chinatimes.append(j)
        if len(title_data_chinatimes) <2 :
            string_1 = '近兩天無額外新聞'
            title_data_chinatimes.append(string_1)
            link_data_chinatimes.append(get_uri_chinatimes(stock))

    eco1 = title_shorten(title_data_economy[0])
    eco1_link = link_data_economy[0]
    eco2 = title_shorten(title_data_economy[1])
    eco2_link = link_data_economy[1]
    eco_uri = get_uri_economy(stock)

    china1 = title_shorten(title_data_chinatimes[0])
    china1_link = link_data_chinatimes[0]
    china2 = title_shorten(title_data_chinatimes[1])
    china2_link = link_data_chinatimes[1]
    china_link = get_uri_chinatimes(stock)

    columns = [CarouselColumn(
                    thumbnail_image_url='https://money.udn.com/static/img/logo.png?1',
                    title='經濟日報',
                    text= stock,
                    actions=[
                        URITemplateAction(
                            label= eco1,
                            uri = eco1_link
                        ),
                        URITemplateAction(
                            label= eco2,
                            uri = eco2_link
                        ),
                        URITemplateAction(
                            label='更多新聞',
                            uri= eco_uri
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://static.chinatimes.com/images/2020/logo-chinatimes2020.svg',
                    title='中國時報',
                    text = stock,
                    actions=[
                        URITemplateAction(
                            label= china1,
                            uri = china1_link
                        ),
                        URITemplateAction(
                            label= china2,
                            uri = china2_link
                        ),
                        URITemplateAction(
                            label='更多新聞',
                            uri= china_link
                        )
                    ]
                )    
            ]
    return columns

