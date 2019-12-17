import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
from itertools import count
from selenium import webdriver
import os, ssl

if (not os.environ.get('PYTHONHTTPSVERIFY', '') and

    getattr(ssl, '_create_unverified_context', None)):

    ssl._create_default_https_context = ssl._create_unverified_context
    
def naver_drama_address(crawling_type, result):
    
    wd = webdriver.Chrome("C:/Program Files (x86)/Microsoft Visual Studio/Shared/Python37_64/WebDriver/chromedriver.exe")
    URL = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&query=%EB%B0%A9%EC%98%81%EC%A2%85%EB%A3%8C%EB%93%9C%EB%9D%BC%EB%A7%88'
    wd.get(URL)
    time.sleep(10)
    wd.find_element_by_xpath("//div[@class='sort_data _root_method']").click()
    time.sleep(1)
    wd.find_element_by_xpath("//li[@data-value='" + crawling_type + "']").click()
    #wd.find_element_by_xpath("//li[@class='_item']/option[data-value='u4=KR&u8=&u9=100']").click()
    time.sleep(1)

    #wd.find_element_by_xpath("//li[@class='_item']/option[text()='지상파']").click()
    # 지상파 버튼 클릭
    # > (다음) 버튼 클릭
    for page in count():
      try:

        rcv_data = wd.page_source
        soupData = BeautifulSoup(rcv_data,'html.parser')

        div_tag = soupData.find('div', attrs={'class':'content_box _content'})
        for drama_data in div_tag.findAll('div', attrs={'class':'item'}):
          drama_info = drama_data.find('dl') # list(store_tr.strings)
          drama_title = drama_info.find('dt', attrs={'class':'bd_title'})
          drama_title = drama_title.find('a').get_text().replace ( '\u200b', '')
          
          drama_broadcaster = drama_info.find('dd', attrs={'class':'bd_info'})
          drama_broadcaster = drama_broadcaster.find('a').get_text().replace ( '\u200b', '')

          drama_date = drama_info.find('dd', attrs={'class':'start_day'})
          drama_date = drama_date.find('span').get_text().replace ( '\u200b', '')
          drama_period = drama_date.split('~')
          start_date = drama_period[0].replace ( '\u200b', '')
          end_date = drama_period[1].replace ( '\u200b', '')
          drama_rating = drama_info.find('dd', attrs={'class':'rating_data'})

          if drama_rating==None:
              print("no")
          else:
              drama_rating = drama_rating.find('em')

          if drama_rating==None:
              drama_rating = '0%'
              drama_rating = drama_rating.replace ( '\u200b', '')
          else:
              drama_rating = drama_rating.get_text().replace ( '\u200b', '')
          
          print(drama_title)
          print(drama_broadcaster)
          print(drama_date)
          print(start_date)
          print(end_date)
          print(drama_rating)

          result.append([drama_title] + [drama_broadcaster] + [start_date] + [end_date] + [drama_rating])

        next_btn = wd.find_element_by_xpath("//a[@class='btn_page on _btn_next']").click()
        time.sleep(1)
        
      except Exception as e:
        print(e)
        break

    return

#@data-value
#지상파 : u4=KR&u8=&u9=100
#종합편성 : u4=KR&u8=&u9=500
#케이블 : u4=KR&u8=&u9=200

def naver_drama ():

    channel_type = ['지상파', '종합편성', '케이블']
    channel_code = ['u4=KR&u8=&u9=100', 'u4=KR&u8=&u9=500', 'u4=KR&u8=&u9=200']
    
    result = []
    
    print('DRAMA CRAWLING START')
    for i in range(0,3):

        crawling_type = channel_type[i]
        
        naver_drama_address(channel_code[i], result)

        drama_table = pd.DataFrame(result, columns=('title', 'broadcaster', 'start_date', 'end_date', 'last_rating'))
        drama_table.to_csv('drama_' + crawling_type + '.csv', encoding='cp949', mode='w', index=True)

        print(crawling_type + ' CRAWLING FINISHED')

        del result[:]
        
    print('FINISHED')
    
if __name__ == '__main__':
     naver_drama ()

