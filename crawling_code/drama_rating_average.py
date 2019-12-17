# 시청률 평균구하기
import pandas as pd
import utils

dir_path = "C:/Users/LG/Desktop/drama_rating/drama_rating_케이블/"

file_list = utils.get_dir_list(dir_path)

result = []
for file in file_list:

    file_path = dir_path + file
    print(file_path)

    cnt = 0
    rating_sum = 0.0
    
    df = utils.get_dataframe(file_path)

    rating_list = df['rating'].values

    for rating in rating_list:
        rating_sum = rating_sum + float(rating)
        cnt = cnt+1

    rating_average = round(rating_sum / cnt,2)

    drama_title = file.split('_')[-1]
    drama_title = drama_title.split('.')[0]

    cnt = str(cnt) + '부작'
    result.append([drama_title] + [cnt] + [rating_average])
    print(drama_title)
    print(rating_sum)
    print(cnt)
    print(rating_average)

drama_blog_count_table= pd.DataFrame(result, columns=('title', 'broadcating_count', 'average_rating'))
drama_blog_count_table.to_csv('drama_rating_average_케이블.csv', encoding='cp949', mode='w', index=True)


