''' 
yahoo電影相似度矩陣
因為查詢電影相似度耗時-一部約1分鐘 
嘗試寫入mongodb
     將檔案轉為json格式: 
    {'電影ID':xxxx, 
    '電影名稱':'xxxxxxx', 
    '電影相似度':{'A':0.97,
                'B':0.88,
                ......,
                'n':0.0001 
                }
    }
 '''

import pandas as pd
df = pd.read_csv('./movie_all_2.csv')

import jieba
jieba.set_dictionary('./jieba_data/dict.txt.big')

stop_words_list = []
with open(file='jieba_data/movie_stop_word_new.txt', mode='r', encoding="UTF-8") as file:
    for line in file:
        line = line.strip()
        stop_words_list.append(line)

for i in range(len(df)):
    id_no = df['電影ID'][i]
    each_list = df['電影簡介'][i]
    try:
        each_txt_jieba = jieba.lcut(each_list, cut_all=False)
        #     print(each_txt_jieba)
        each_cut = []
        for t in each_txt_jieba:
            if t not in stop_words_list:
                each_cut.append(t)
        df['電影簡介'][i] = ' '.join(each_cut)          #存成str型態
    except:
        print(id_no)
        continue

#將電影所有資訊都當成該電影的關鍵字

df['關鍵字'] = ''
columns = ['上映日期', '片長', '導演', '演員','電影類型','分級','電影簡介']
for i in range(len(df)):
    s=''
    try:
        for col in columns:
            if str(df[col][i]) =='nan':
                continue
            else:
                s+=str(' '+df[col][i])
        df['關鍵字'][i]=s
    except:
        print(i)
        continue

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
count = CountVectorizer()
count_matrix = count.fit_transform(df['關鍵字'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)


#將矩陣存入mongo
from pymongo import MongoClient
conn = MongoClient('mongodb://localhost:27017/')        #連線-27017為預設port
db = conn.Movie_project   #建立資料庫-Movie_project(如果沒有會自行創建) 

l=[]
d={}
movie_field=['_id','電影中文名','英譯']
m_id=list(df['電影ID'])
m_name=list(df['電影中文名'])
m_name_e=list(df['英譯'])
m_total=[m_id,m_name,m_name_e]
for i in range(len(m_id)):
    try :
        top_30_similar = pd.Series(cosine_sim[i], index=list(df['電影中文名'])).sort_values(ascending=False).iloc[1:31]
        for j in range(len(movie_field)):
            d[movie_field[j]]=str(m_total[j][i])
            d['其他電影相似度']=dict(top_30_similar)
        # print(d)
        result = db.movie_similarity.insert(d)  # 建立桶子movie_similarity(表格)
        print('ID={}完成'.format(df['電影ID'][i]))
    except Exception as e:
        l.append(df['電影ID'][i])
        print('ID={}失敗'.format(df['電影ID'][i]))
        print(e)
        continue
print(l)
# for i in range(5):
#     top_5_similar = pd.Series(cosine_sim[i], index=list(df['電影中文名'])).sort_values(ascending=False).iloc[1:6]
#     for j in range(len(movie_field)):
#         d[movie_field[j]]=m_total[j][i]
#         d['其他電影相似度']=dict(top_5_similar)
#     print(d)

#呼叫方式
db.movie_similarity.find({'電影中文名':'億男'})
r=db.movie_similarity.find({'電影中文名':'億男'},{'其他電影相似度':1})
# print(r)

from pymongo import MongoClient
con = MongoClient('mongodb://localhost:27017/')
db = con.Movie_project
input_movie=input('請輸入電影名稱:')
input_count=int(input('要推薦幾部:'))
r=db.movie_similarity.find({'電影中文名':'{}'.format(input_movie)},{'其他電影相似度':1})
# r=db.movie_similarity.find({'電影中文名':'億男'},{'其他電影相似度':1})
# print(r)

# for item in r:
#     s=item['其他電影相似度']
#     l=sorted(s.items(),key=lambda item:item[1],reverse=True)
#     l=l[:input_count]
#     for top_i in l:
#         print(top_i[0])