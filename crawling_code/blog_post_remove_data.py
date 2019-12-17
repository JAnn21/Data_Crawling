# 관련없는 데이터 제거하기
import pandas as pd
import utils

dir_path = "C:/Users/LG/Desktop/blog_post/blog_post_before_30일_지상파/"

file_list = utils.get_dir_list(dir_path)

before_count = []
after_count = []

count = []

cnt = 1
for file in file_list:
    file_path = dir_path + file
    print(file_path)

    df = utils.get_dataframe(file_path)

    words = input('입력 : ')
    word_list = words.split(';')

    #total_df = pd.DataFrame(columns = ['idx','drama_title', 'date', 'blog_title', 'writer', 'contents'])
    total_df = df
    
    for word in word_list:
        print(word)

        contain_df = df[df.contents.str.contains(word)]
        print(contain_df)
        total_df.append(contain_df)
        print(total_df)
       # pd.concat([total_df,contain_df], ignore_index=True)

    print(total_df)
    total_df = total_df.drop_duplicates(["blog_title","writer"], keep="first")

    print(total_df)
    

    
