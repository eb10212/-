'''
將每部電影的type寫成onehat形式
使用Ｒ跑分群
'''

import pandas as pd
import csv
# df = pd.read_csv('./ok/movie_copy.csv')
# print(df['電影類型'][0])
# type_list=[]
# for i in range(len(df)):
#     a=(df['電影類型'][i].strip('[').strip(']').replace('\'','')).split(',')
#     for i in a:
#         b=i.strip()
#     # print(b)
#         if b not in type_list and b!='':
#             type_list.append(b)
# print(type_list)

type_list=['劇情', '犯罪', '歷史/傳記', '動作', '懸疑/驚悚', '戰爭', '冒險', '喜劇', '恐怖', '奇幻', '愛情', '音樂/歌舞', '科幻', '溫馨/家庭', '動畫', '紀錄片', '勵志', '武俠', '影展', '戲劇', '影集']

df2 = pd.read_csv('./ok/movie_copy.csv')
for i in range(len(df2)):
    id_no=df2['電影ID'][i]
    # print([id_no])
    each_type_list = df2['電影類型'][i].strip('[').strip(']').replace('\'', '').split(',')
    # print(each_type_list)
    each_type_list_new=[]
    for each_type in each_type_list:
        each_type=each_type.strip()
        each_type_list_new.append(each_type)
    # print(each_type_list_new)

    count_list=[id_no]          #索引地1個位子先放id_no,再放type
    for i in type_list:
        if i in each_type_list_new:
            count_list.append(1)
        else:
            count_list.append(0)
    # print(count_list)
    with open('./movie_table.csv', 'a', newline='', encoding='utf-8') as csvfile:
        rows = csv.writer(csvfile)
        rows.writerow(count_list)
