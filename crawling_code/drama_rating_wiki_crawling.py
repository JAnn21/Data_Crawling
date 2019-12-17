# 시청률 크롤링
import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from itertools import count
from selenium import webdriver
import os, ssl
import utils

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

def naver_drama_rating_address(result, drama, fail_list):
    
    existAGB = False
    existTNmS = False
    existSeoul = False

    row_count = 0
    broadcast_count = 0
    rating_sum = 0
    rating_list = "["
    drama_title = drama
    drama_search = drama_title.replace(' ', '_')

    drama_encode = urllib.parse.quote(drama_search)
    URL = 'https://ko.wikipedia.org/wiki/%s'%drama_encode

    drama_episode = ''
    broadcast_date = ''
        
    try:
        rcv_data = get_request_url(URL)
        soupData = BeautifulSoup(rcv_data,'html.parser')
        table = soupData.find('table', attrs={'class':'wikitable'})

        if table == None:
            drama_search = drama_search + "_(드라마)"
                
            drama_encode = urllib.parse.quote(drama_search)
            URL = 'https://ko.wikipedia.org/wiki/%s'%drama_encode

            rcv_data = get_request_url(URL)
            soupData = BeautifulSoup(rcv_data,'html.parser')


        for rating_table in soupData.findAll('table', attrs={'class':'wikitable'}):

            # 시청률 테이블 찾기
            if str(rating_table).find('회차') < 0:
                continue

            else:

                start_index = 3
                    
                if str(rating_table).find('2019년') < 0:
                    start_index = 2

                for rating in rating_table.findAll('tr'):

                    row_count = row_count+1
                    if row_count <= start_index:
                        continue

                    if row_count <= start_index:
                        if row_count == start_index-1:

                            # AGB 시청률 존재 여부
                            if str(rating).find('AGB') > -1 or str(rating).find('닐슨') > -1:
                                existAGB = True

                            # TNmS 시청률 존재 여부
                            if str(rating).find('TNmS') > -1:
                                existTNmS = True

                        elif row_count == start_index:

                            if str(rating).find('수도권') > -1:
                                existSeoul = True

                    else :
                        td_list = []
                            
                        episode = rating.find('th')

                        if episode != None:
                            drama_episode = episode.get_text()
                            
                        if drama_episode.find('평균') > -1:
                            break

                        for td in rating.findAll('td'):

                            b = td.find('b')

                            if b == None:
                                td_list.append(td.get_text())

                            else:
                                td_list.append(b.get_text())

                        print(td_list)
                        if existSeoul == False and existTNmS == False:
                            rt = td_list[-1]
                        elif existSeoul == False:
                            rt = td_list[-1]
                        elif existTNmS == False:
                            rt = td_list[-2]
                        else:
                            rt = td_list[-2]

                        rt = td_list[-2]

                        if td_list[0].find('월') > -1:
                            broadcast_date = '2019년 ' + td_list[0]

                        drama_title = drama_title.replace ( '\u200b', '').replace('\u2729','')
                        broadcast_date = broadcast_date.replace ( '\u200b', '').replace('\u2729','')
                        drama_episode = drama_episode.replace ( '\u200b', '').replace('\u2729','')
                        rt = rt.replace ( '\u200b', '').replace('\u2729','')

                        result.append([drama_title] + [broadcast_date] + [drama_episode] + [rt])
     
    except Exception as e:
        print(e)
        fail_list.append(drama_title)
        return

    return


def naver_drama_rating ():

    result = []
    fail_list = []

    filepath = 'E:/크롤링 프로젝트/drama_종합편성.csv'
    
    drama_list = utils.get_drama_list(filepath)

    for drama in drama_list:
        
        print( drama + ' RATING CRAWLING START')

        naver_drama_rating_address(result, drama, fail_list)
        drama_rating_table = pd.DataFrame(result, columns=('title', 'date', 'episode', 'rating'))
        drama_rating_table.to_csv('drama_rating_지상파_' + drama.replace(':','') + '.csv', encoding='cp949', mode='w', index=True)

        del result[:]


    print(fail_list)
    
        
    print('FINISHED')


if __name__ == '__main__':
     naver_drama_rating ()




