# deduplication 중복된 데이터 제거하기

import pandas as pd
import utils


dir_path = "C:/Users/LG/Desktop/blog_post/blog_post_before_2주_케이블/"

file_list = utils.get_dir_list(dir_path)

deduplication_before_count = []
deduplication_after_count = []

deduplication_count = []

for file in file_list:

    file_path = dir_path + file
    print(file_path)

    df = utils.get_dataframe(file_path)

    deduplication_before_count.append(len(df))
    
    deduplication_df = df.drop_duplicates(["blog_title","writer"], keep="first")

    save_path = dir_path +  file
    utils.save_dataframe(deduplication_df, save_path)

    deduplication_after_count.append(len(deduplication_df))

    drama_title = file.split("_")
    drama_title = drama_title[5].split(".")
    drama_title = drama_title[0]
    deduplication_count.append([drama_title] + [len(df)] + [len(deduplication_df)])


print(deduplication_before_count)
print(deduplication_after_count)

drama_blog_count_table= pd.DataFrame(deduplication_count, columns=('title', 'before', 'after'))
drama_blog_count_table.to_csv('blog_post_count_before_2주_케이블.csv', encoding='cp949', mode='w', index=True)

    
    
    
