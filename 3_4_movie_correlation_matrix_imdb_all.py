'''
1.先將IMDB資料做整理

2.斷字(空白鍵)完,使用停用字典
3.跑IMDB-電影相似度
4.存入mongodb

5.查詢條件設立

'''

##STEP1:(只做第一次)
# #建立新的存取表格
# import pandas as pd
# new_columns=['IMDB_ID','關鍵字']
# df=pd.DataFrame(columns=new_columns)
# df.to_csv('./movie_IMDB.csv',index=False,encoding='utf-8-sig')
#
#
# #取出IMDB_ID
# import os
# txt_list=os.listdir('E:/專題-movie/reviews_summary_ALL_txt')
# # print(txt_list)
# imdb_id_list=[]
# #
# import csv
# #取出電影將電影簡介
# for i in txt_list:
#     imdb_id=i.rstrip('.txt')
#     imdb_id_list.append(imdb_id)
#     with open('E:/專題-movie/reviews_summary_ALL_txt/{}'.format(i),'r',encoding='utf-8')as f:
#         content=f.read().replace('\n','')
#         content_new=[]
#         content_new.append(content)
#         content_new=''.join(content_new)
#         # print(type(content_new))
#         # print(len(content_new))
#         # print(content_new)
#     data=[imdb_id,content_new]
#     # print(data)
#     with open('./movie_IMDB.csv','a',encoding='utf-8')as f:
#         rows=csv.writer(f)
#         rows.writerow(data)


# #取出電影名稱-合併表格movie_imdb_name.tsv
# import pandas as pd
# df = pd.read_csv('./movie_IMDB.csv')
# df2 = pd.read_csv('./movie_imdb_name.csv',delimiter="\t")
# # print(df2.head(10))
# df3=pd.merge(df,df2, on="IMDB_ID")
# #儲存為./movie_IMDB_new.csv
# df3.to_csv('./movie_IMDB_new.csv',index=False,encoding='utf-8-sig')

#===================================================================================

# #STEP2:
# #將電影將電影簡介斷字&使用停用字典
# import pandas as pd
# import nltk
# import time
# a=time.time()
#
# df = pd.read_csv('./movie_IMDB_new.csv')
#
# #電影簡介斷字斷詞(含使用停用字典)
#
# stop_words_list = []
# with open(file='jieba_data/english_stop.txt', mode='r', encoding="UTF-8") as file:
#     for line in file:
#         line = line.strip()
#         stop_words_list.append(line)
#
#
# for i in range(len(df)):
#     id_no = df['IMDB_ID'][i]
#     each_list = df['關鍵字'][i]
#     try:
#         each_txt_nltk = nltk.word_tokenize(each_list)
#         #     print(each_txt_jieba)
#         each_cut = []
#         for t in each_txt_nltk:
#             if t not in stop_words_list:
#                 each_cut.append(t)
#         df['關鍵字'][i] = ' '.join(each_cut)          #存成str型態
#         print(id_no,'成功')
#     except:
#         print(id_no)
#         continue
# df.to_csv('./movie_IMDB_result.csv',index=False,encoding='utf-8-sig')
# b=time.time()
# print(b-a)

#===================================================================================
import time
import pandas as pd
df=pd.read_csv('./movie_IMDB_result.csv')

#STEP3:相似矩陣
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
count = CountVectorizer()
count_matrix = count.fit_transform(df['關鍵字'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)


#STEP4:將矩陣存入mongo
from pymongo import MongoClient
conn = MongoClient('mongodb://localhost:27017/')        #連線-27017為預設port
db = conn.Movie_project                                 #建立資料庫-Movie_project(如果沒有會自行創建) 
#mongo除錯
def column_filter(s):
    return str(s).replace(r'.','')
for c in df['primaryTitle']:
    df['primaryTitle']=df['primaryTitle'].apply(column_filter)
l=[]
movie_field=['_id','IMDB電影名']
m_id=list(df['IMDB_ID'])
m_name=list(df['primaryTitle'])
m_total=[m_id,m_name]
for i in range(len(m_id)):
    try :
        top_30_similar = pd.Series(cosine_sim[i], index=list(df['primaryTitle'])).sort_values(ascending=False).iloc[1:31]
        d = {}
        for j in range(len(movie_field)):
            d[movie_field[j]]=str(m_total[j][i])
            d['其他電影相似度']=dict(top_30_similar)
        # print(d)
        result = db.movie_similarity_IMDB_new.insert(d)          # 建立桶子movie_similarity_IMDB(表格)
        print('ID={}完成'.format(df['IMDB_ID'][i]))
    except Exception as e:
        l.append(df['primaryTitle'][i])
        print('ID={}失敗'.format(df['IMDB_ID'][i]))
        print(e)
        continue
print(l)
d=time.time()



#===================================================================================
# #STEP5:搜尋資料
# from pymongo import MongoClient
# con = MongoClient('mongodb://localhost:27017/')
# db = con.Movie_project
# input_movie=input('請輸入電影名稱:')
# input_count=int(input('要推薦幾部:'))
# r=db.movie_similarity.find({'電影中文名':'{}'.format(input_movie)},{'其他電影相似度':1})
# # r=db.movie_similarity.find({'電影中文名':'億男'},{'其他電影相似度':1})
# # print(r)
#
# for item in r:
#     s=item['其他電影相似度']
#     l=sorted(s.items(),key=lambda item:item[1],reverse=True)
#     l=l[:input_count]
#     for top_i in l:
#         print(top_i[0])



#以下查詢IMDB資料===============================================================
# # from pymongo import MongoClient
# # con = MongoClient('mongodb://10.120.26.13:27017/') #雅婕的mongodb
# # db = con.movie_tag
# #
# # id='tt0010323'
# # r = db.tag100.find({'_id': id}, {id: 1})
# # for item in r:
# #     word=item[id]
# #     print(word)



