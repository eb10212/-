'''
求出每部電影的特徵矩陣(記數)
# 1.使用np:每欄位原始記數=0
2.一電影id,將各簡介斷字段詞
3.分別計算每部電影的關鍵字出現次數
'''

import numpy as np
import jieba
import pandas as pd
import csv

#1.
movie_tag_list = []
with open(file='jieba_data/movie_tag.txt',mode='r', encoding="UTF-8") as file:
    for line in file:
        line = line.strip()
        movie_tag_list.append(line)
# print(movie_tag_list)

column=['電影ID']
column.extend(movie_tag_list)
with open('./movie_count_tag.csv', 'a', newline='', encoding='utf-8') as csvfile:
    rows = csv.writer(csvfile)
    rows.writerow(column)
# count_tag=np.zeros(len(movie_tag_list),int)


#2.
jieba.set_dictionary('./jieba_data/dict.txt.big')

stop_words_list = []
with open(file='jieba_data/movie_stop_word.txt',mode='r', encoding="UTF-8") as file:
    for line in file:
        line = line.strip()
        stop_words_list.append(line)


#3.
df1 = pd.read_csv('./ok/movie_about.csv')
# print(df1.head(10))
# for i in range(1):
for i in range(len(df1)):
    id_no=df1['電影ID'][i]
    each_list = df1['電影簡介'][i].replace('\n', '').replace('-', '').replace('_', '').replace('~', '')
    each_txt_jieba = jieba.lcut(each_list, cut_all=False)
    # print(each_txt_jieba)
    each_ID_tag_count = [id_no,]
    for each_tag in movie_tag_list:
        # print(each_tag)
        each_ID_tag_count.append(each_txt_jieba.count(each_tag))
    # print(tag_count)
    # print('===================')
    with open('./movie_count_tag.csv', 'a', newline='', encoding='utf-8') as csvfile:
        rows = csv.writer(csvfile)
        rows.writerow(each_ID_tag_count)


#想法/用法=========================================
# a=[2,4,6,8,10,12] #tag
# b=[1,2,3,4,5,2,2,6]#簡介斷字
# c=[]
# for i in a:
#     c.append(b.count(i))
# print(c)
#
# a=['a']
# a.extend(['b','b','c'])
# print(a)