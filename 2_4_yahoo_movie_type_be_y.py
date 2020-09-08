'''
將每個電影簡介區分成不同type的內容
選出停用字典/類別關鍵字
#依type將簡介-字詞跑count:看熱力圖-找出每個type重要的關鍵字-變成每個type的特徵值(x)
'''

##1.
# import pandas as pd
# import os
#
# if not os.path.exists('movie_type'):
#     os.mkdir('movie_type')
#
# df= pd.read_csv('./ok/movie_about.csv')
# df2 = pd.read_csv('./movie_table.csv')
# # print(df2['劇情'][0])
# # print(type(df['電影簡介'][0]))
#
type_list=['劇情', '犯罪', '歷史/傳記', '動作', '懸疑/驚悚', '戰爭', '冒險', '喜劇', '恐怖', '奇幻', '愛情', '音樂/歌舞', '科幻', '溫馨/家庭', '動畫', '紀錄片', '勵志', '武俠', '影展', '戲劇', '影集']
# for i in range(len(df2)):
#     for k in type_list:
#         if df2[k][i]==1:
#             k=k.replace('/','')
#             with open('./movie_type/{}.txt'.format(k),'a',encoding='utf-8')as t1:
#                 t1.write(df['電影簡介'][i]+'\n')

#2
import jieba
import pandas as pd
from collections import Counter

jieba.set_dictionary('./jieba_data/dict.txt.big')
stop_words_list = []
with open(file='jieba_data/movie_stop_word.txt',mode='r', encoding="UTF-8") as file:
    for line in file:
        line = line.strip()
        stop_words_list.append(line)

for i in type_list:
    all_txt=[]
    i=i.replace('/','')
    with open('./movie_type/{}.txt'.format(i),'r',encoding='utf-8') as f:
        each_txt=f.read().replace('\n','').replace('-','').replace('_','').replace('~','')
        each_txt_jieba=jieba.lcut(each_txt,cut_all=False)       #精確模式
    for word in each_txt_jieba:
        if word not in stop_words_list and len(word) > 1:
            if  word.isalpha():
                all_txt.append(word)
            else:
                continue


    txt_count=Counter(all_txt)

    df=pd.DataFrame(list(txt_count.items()),columns = ['key','value'])

    df.to_csv('./movie_type/{}_count.csv'.format(i),index=False,encoding='utf-8-sig')



# for i in type_list:
#     i=i.replace('/','')
#     df = pd.read_csv('./movie_type/{}_count.csv'.format(i))
#     print(i, len(df))