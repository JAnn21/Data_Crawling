# 드라마 블로그 크롤링
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from itertools import count
from selenium import webdriver
import os, ssl
import utils
import re

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and

    getattr(ssl, '_create_unverified_context', None)):

    ssl._create_default_https_context = ssl._create_unverified_context


def get_request_url(url, enc='utf-8'):

    
    req = urllib.request.Request(url)

    try: 
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            try:
                rcv = response.read()
                ret = rcv.decode(enc)
            except UnicodeDecodeError:
                ret = rcv.decode(enc, 'replace')                
            return ret
            
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

def naver_drama_blog_address(result, all_result, article_number, drama):

        
    drama_title = drama[0] + " 드라마"
    print(drama_title)
    drama_encode = urllib.parse.quote(drama_title)
    
    # 방영 시작일
    drama_date = drama[1]
    print(drama_date)
    search_date = drama_date[:-1]
    
    search_date_list = drama_date.split('.')
    year = int(search_date_list[0])
    month = int(search_date_list[1])
    day = int(search_date_list[2])

    date = datetime.datetime(year,month,day)

    after_1_day = str(date+datetime.timedelta(days=-14))
    start_date = after_1_day.split(' ')[0].replace('-', '')
    
    after_14_day = date+datetime.timedelta(days=-1)

    today = datetime.datetime.now()
    if after_14_day > today:
        after_14_day = today

    after_14_day = str(after_14_day)
    end_date = after_14_day.split(' ')[0].replace('-', '')

    URL ="https://search.naver.com/search.naver?where=post&query=" + drama_encode + "&sort=0" + "&ds=" + start_date + "&de=" + end_date + "&nso=so%3Ar%2Cp%3Afrom" + start_date + "to" + end_date + "%2Ca%3A&start=1"

    print(URL)
    
    try:
        rcv_data = get_request_url(URL)
        soupData = BeautifulSoup(rcv_data,'html.parser')

        article_count = soupData.find('span', attrs={'class':'title_num'}).get_text().split('/')[1].replace('건','').strip()
        article_number.append([drama_title] + [article_count])
 
        article_count = article_count.replace(',','')
        article_count = int(article_count)
        if article_count%10 == 0:
            article_count = int(article_count/10) - 1
        else :
            article_count = int(article_count/10)
  
        article_container = soupData.find('ul', attrs={'class':'type01'})
        for drama_article in article_container.findAll('dl'):

            article_title = utils.get_clear_string(drama_article.find('dt').a['title'])
            article_date = drama_article.find('dd',attrs={'class':'txt_inline'}).get_text()

            article_date = utils.get_clear_string(article_date)

            article_contents = utils.get_clear_string(drama_article.find('dd',attrs={'class':'sh_blog_passage'}).get_text())

            article_writer = utils.get_clear_string(drama_article.find('span', attrs={'class':'inline'}).find('a').get_text())

            print(article_title)
            print(article_date)
            print(article_writer)
                
            result.append([drama_title] + [article_date] + [article_title] + [article_writer] + [article_contents])


        for page in range(0,article_count):

            page = ((page+1)*10)+1

            URL ="https://search.naver.com/search.naver?where=post&query=" + drama_encode + "&sort=0" + "&ds=" + start_date + "&de=" + end_date + "&nso=so%3Ar%2Cp%3Afrom" + start_date + "to" + end_date + "%2Ca%3A&start=" + str(page)

            try:
                rcv_data = get_request_url(URL)
                soupData = BeautifulSoup(rcv_data,'html.parser')

                article_container = soupData.find('ul', attrs={'class':'type01'})
                for drama_article in article_container.findAll('dl'):
                    article_title = utils.get_clear_string(drama_article.find('dt').a['title'])
                    if article_title.strip() == '':
                        article_title = utils.get_clear_string(drama_article.find('dt').a.get_text())
                                                               
                    article_date = drama_article.find('dd',attrs={'class':'txt_inline'}).get_text()

                    article_date = utils.get_clear_string(article_date)

                    article_contents = utils.get_clear_string(drama_article.find('dd',attrs={'class':'sh_blog_passage'}).get_text())

                    article_writer = utils.get_clear_string(drama_article.find('span', attrs={'class':'inline'}).find('a').get_text())
                    
                    print(article_title)
                    print(article_date)
                    print(article_writer)
                
                    result.append([drama_title] + [article_date] + [article_title] + [article_writer] + [article_contents])

            
            except Exception as e:
                print(drama_title)
                print(e)
                break

    except Exception as e:
        print(drama_title)
        print(e)
        

    return


def naver_drama_article ():

    result = []
    all_result = []
    article_count = []

    filepath = 'E:/크롤링 프로젝트/제출/drama_list/drama_케이블.csv'

    drama_list = utils.get_drama_and_end_date_list(filepath)

    print(drama_list)

    cnt = 1
    for drama in drama_list:
        
        
        print('DRAMA ARTICLE CRAWLING START')

        naver_drama_blog_address(result, all_result, article_count, drama)

        print(drama)
        print(drama_list)
        print(article_count)

        drama_article_table = pd.DataFrame(result, columns=('drama_title', 'date', 'blog_title', 'writer', 'contents'))
        drama_article_table.to_csv('drama_blog_지상파_2주_' + drama[0].replace(":", "") + '.csv', encoding='utf-8', mode='w', index=True)
        del result[:]

        print(drama + ' CRAWLING FINISHED')

    drama_blog_count_table= pd.DataFrame(article_count, columns=('title', 'number'))
    drama_blog_count_table.to_csv('drama_blog_케이블_방영종료_2주.csv', encoding='cp949', mode='w', index=True)
    
    del all_result[:]
        
    print('FINISHED')


if __name__ == '__main__':
     naver_drama_article ()




