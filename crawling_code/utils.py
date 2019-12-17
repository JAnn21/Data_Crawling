import pandas as pd
import os

def get_dir_list(dir_path):

    file_list = os.listdir(dir_path)
    file_list_csv = [file for file in file_list if file.endswith(".csv")]

    return file_list_csv

def get_drama_list(filepath):

    
    drama_df = pd.read_csv(filepath, encoding='CP949', index_col=0, header=0, engine='python')

    drama_df[drama_df['start_date'] == drama_df['end_date']]
    drama_table = drama_df[drama_df['start_date'] != drama_df['end_date']]

    drama_table[drama_table['last_rating'] == '0%']
    drama_table = drama_table[drama_table['last_rating']!='0%']

    title_list = drama_table.title.unique()

    return title_list

def get_drama_and_start_date_list(filepath):

    drama_df = pd.read_csv(filepath, encoding='CP949', index_col=0, header=0, engine='python')

    drama_df[drama_df['start_date'] == drama_df['end_date']]
    drama_table = drama_df[drama_df['start_date'] != drama_df['end_date']]

    drama_table[drama_table['last_rating'] == '0%']
    drama_table = drama_table[drama_table['last_rating']!='0%']
    drama_table = drama_table[['title', 'start_date']]

    title_and_date_list = drama_table.values

    return title_and_date_list

def get_drama_and_end_date_list(filepath):

    drama_df = pd.read_csv(filepath, encoding='CP949', index_col=0, header=0, engine='python')

    drama_df[drama_df['start_date'] == drama_df['end_date']]
    drama_table = drama_df[drama_df['start_date'] != drama_df['end_date']]

    drama_table[drama_table['last_rating'] == '0%']
    drama_table = drama_table[drama_table['last_rating']!='0%']
    drama_table = drama_table[['title', 'end_date']]

    title_and_date_list = drama_table.values

    print(title_and_date_list)

    return title_and_date_list

def get_dataframe(filepath):

    df = pd.read_csv(filepath, encoding='CP949', index_col=0, header=0, engine='python')

    return df

def save_dataframe(df, filepath):
    
    df.to_csv(filepath, encoding='cp949', mode='w', index=True)

def get_clear_string(value):

 #   unicode_list = ['\u119e','\u2757','\u9648','\u0e22','\u0e49','\u0e32','\u0e38','\u0e48','\u0e19','\u5a77','\u0308','\ufecc','\U0001f60d','\u258e','\u8bb0','\U0001f91c','\u2219','\u272e','\u7f51','\u5427','\u4f53','\u996d','\u8717','\u5bfe','\u8217','\u8aac','\u273f','\u2727','\u2601','\u032e','\u2726','\u02e2','\u02e1','\xf3','\u5b66','\u0e31','\u1555','\u1d00','\u029f','\u026a','\u1d21','\u1d07','\u554a','\u1d39','\u1d3c','\u1d30','\u1da0','\u1d40','\u1d34','\u4e57','\u2693','\u685c','\u0280','\u1d04','\u1d0f','\u1d05','\u1d1b','\u029c','\u7e01','\u56fd','\u141b','\u1557','\u263a','\u0c87','\u26ab','\u0643','\u0631','\u0627','\u0641','\u0645','\u063a','\u05e7','\u05e8','\u05d1','\u05de','\u05d2','\u05e2','\xab','\xbb','\u0e27','\u2800','\u2b07','\u263b','\u0e51','\u200b','\u604b','\u5b81','\u513f','\u6ca1','\u58f0','\u4f20','\u270b','\u515a','\u25cd','\u0348','\u9752','\u6238','\u273d','\u2508','\xe7','\u11a2','\u6765','\u99c6','\u309d','\u2579','\u301c','\u2014','\u2763','\u2f1f','\u0299','\u1d1c','\u2666','\u0dc6','\u2070','\u203c','\u203f','\u6dcc','\u65f6','\u270f','\u2024','\xa0','\ufffd','\xa9','\u035f','\u987f','\ufe4f','\u5c81','\u7955','\u10d3','\u0301','\u51ea','\u9f99','\xe0','\u90d1','\u9d8f','\xe1','\u7fbf','\u27a1','\xf6','\u2311','\u0d03','\uff65','\u0311','\u25e1','\u4e34','\u035e','\u0295','\u2022','\u032b','\u0361','\u0294','\xea','\xe8','\u2117','\ufe0e','\u2027','\u20a9','\u2764','\ufe0f','\u2b50','\u2013','\u10e6','\u2714','\u30fc','\u2600','\u02c3','\u0335','\u1d17','\u02c2','\u0648','\u30fb','\u2765','\u2728','\u2708']

 #   for unicode in unicode_list:
 #       value = value.replace(unicode, '')

    value = value.strip()
    
    return value
