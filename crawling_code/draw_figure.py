import pandas as pd
import matplotlib.pyplot as plt
import utils

# 드라마 리스트
# 드라마 시청률 리스트
# 드라마 기사 갯수 리스트

root_dir = 'C:/Users/LG/Desktop/'

rating_path = 'drama_rating/'
rating_name = 'drama_average_rating_'

post_path = 'blog_post/blog_post_count_'

post_name = ['before_2주_', 'after_2주_']

channels= ['지상파', '종합편성', '케이블']
channel_english = ['terrestrial','comprehensive', 'cable' ]
colors = ['salmon', 'orange', 'steelblue']
markers = ['o', 'x', '^']

pearson = []
c = 0
f = plt.figure(figsize=(10, 5))
f.subplots_adjust(left=0.090, bottom=0.001, right=0.950, top=0.80, wspace=0.50, hspace=0.99)

for channel in channels:
    
    c = c+1
    p=0
 
    for post in post_name:
        drama_rating = []
        drama_blog_count = []

        drama_rating_file_path = root_dir + rating_path + rating_name + channel + '.csv'
        #print(drama_rating_file_path)

        drama_blog_count_file_path = root_dir + post_path + post + channel + '.csv'
        #print(drama_blog_count_file_path)
        
        drama_rating_df = utils.get_dataframe(drama_rating_file_path)
        drama_blog_count_df = utils.get_dataframe(drama_blog_count_file_path)

        drama_file_path = root_dir + 'drama_list/drama_' + channel + '.csv'
        #print(drama_file_path)
        drama_list = utils.get_drama_list(drama_file_path)

        for drama in drama_list:
            rating_data = drama_rating_df[drama_rating_df['title'] == drama]
            rating_data_count = len(rating_data.index)

            if rating_data_count == 1:
                drama_rating.append(rating_data['average_rating'].values[0])
            else :
                print(drama)
        
            article_counting_data = drama_blog_count_df[drama_rating_df['title'] == drama]
            article_counting_data_count = len(article_counting_data.index)

            if article_counting_data_count == 1:
                drama_blog_count.append(article_counting_data['after'].values[0])
            else :
                print(drama)

        
       # print(drama_rating)
       # print(drama_blog_count)

       # print("drama_rating : " + str(len(drama_rating)) + "  drama_article_counting : " + str(len(drama_blog_count)))

       
        row = 3
        col = 3
        graph = f.add_subplot(row,col,c+(p*3))

        graph.set_xlabel('blog count')
        graph.set_ylabel(' rating')
        graph.set_title(post.replace("주_", "week_")+channel_english[c-1])
        graph.scatter(drama_blog_count, drama_rating, marker=markers[c-1], color=colors[c-1])
        ls = []
        ls.append(drama_rating)
        ls.append(drama_blog_count)
        dd=pd.DataFrame(ls).T

        corr=dd.corr(method='pearson')
        print(drama_rating_file_path)
        print(drama_blog_count_file_path)
        print(round(corr[0][1],6))
        p = p+1

plt.show()

'''
    

drama_file_path = root_dir + 'drama_list/drama_지상파.csv'
drama_rating_file_path = root_dir + 'drama_rating_average/drama_average_rating_지상파.csv'
drama_article_counting_fil_path = root_dir + 'drama_blog_post_count/drama_blog_count_deduplication_지상파_2주.csv'

drama_rating = []
drama_article_counting = []

drama_list = utils.get_drama_list(drama_file_path)
drama_list.sort()

drama_rating_df = utils.get_dataframe(drama_rating_file_path)
drama_article_counting_df = utils.get_dataframe(drama_article_counting_fil_path)

#print(drama_rating_df.sort_values(by=['title'], axis=0))
#print(drama_article_counting_df.sort_values(by=['title'], axis=0))

for drama in drama_list:

    rating_data = drama_rating_df[drama_rating_df['title'] == drama]
    rating_data_count = len(rating_data.index)

    if rating_data_count == 1:
        drama_rating.append(rating_data['average_rating'].values[0])
        #print(rating_data['average_rating'].values[0])
    else :
        print(drama)
        
    article_counting_data = drama_article_counting_df[drama_rating_df['title'] == drama]
    article_counting_data_count = len(article_counting_data.index)

    if article_counting_data_count == 1:
        drama_article_counting.append(article_counting_data['after'].values[0])
        #print(article_counting_data['article_counting'].values[0])
    else :
        print(drama)


ls = []
ls.append(drama_rating)
ls.append(drama_article_counting)
dd=pd.DataFrame(ls).T

corr=dd.corr(method='pearson')
print(corr)
'''
