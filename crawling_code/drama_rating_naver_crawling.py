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
    
    
def naver_drama_rating_address(result, drama_list):
    
    wd = webdriver.Chrome("C:/Users/LG/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Python 3.5/chromedriver.exe")

    count = drama_list.size

    for i in range(0, count):

        broadcast_count = 0
        rating_sum = 0
        rating_list = "["
        drama_title = drama_list[i]
        drama_search = drama_title.replace(' ', '')
        
        URL = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%s' %drama_search

        wd.get(URL)
        time.sleep(1)

        wd.find_element_by_xpath("//a[text() = '시청률']").click()
        time.sleep(1)
        
        try:
            rcv_data = wd.page_source
            soupData = BeautifulSoup(rcv_data,'html.parser')
            table = soupData.find('g', attrs={'class':'bb-texts bb-texts-data'})
            print(table)

            for rating in table.findAll('text'):
                broadcast_count = broadcast_count + 1
                value = rating.get_text()
                bd_c = "제 " + str(broadcast_count) + "회"
                result.append([drama_title] + [bd_c] + [value])

            drama_table = pd.DataFrame(result, columns=('title', 'episode', 'rating'))
            drama_table.to_csv('drama_rating_케이블_' + drama_title.replace(':','') + '.csv', encoding='cp949', mode='w', index=True)

            del result[:]

        except Exception as e:
            print(e)
            continue
            

    

    return


def naver_drama_rating ():

    result = []

    filepath = 'C:/Users/LG/Desktop/drama_list/drama_케이블.csv'
    drama_list = utils.get_drama_list(filepath)

    print('DRAMA RATING CRAWLING START')

    naver_drama_rating_address(result, drama_list)

        
    print('FINISHED')


if __name__ == '__main__':
     naver_drama_rating ()




