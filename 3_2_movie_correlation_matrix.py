'''
電影相似度矩陣

'''
import pandas as pd
df = pd.read_csv('./movie_all.csv')
# print(df.head(10))

#電影簡介斷字斷詞(含使用停用字典)
import jieba
jieba.set_dictionary('./jieba_data/dict.txt.big')

stop_words_list = []
with open(file='jieba_data/movie_stop_word.txt', mode='r', encoding="UTF-8") as file:
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

#新增欄位(關鍵字=上映日期+片長+導演+演員+電影類型+分級+電影簡介)
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
    except:
        print(i)
        continue

#求出電影跟電影間的相關矩陣
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
#BoW:詞袋模型(不考慮上下文,只考虑所有词的權重)
count = CountVectorizer()
#1.分詞:計算關鍵字出现的次数
count_matrix = count.fit_transform(df['關鍵字'])   #輸出矩陣
# feature_name = count.get_feature_names()         #查看共有哪些詞
# onehat_matrix=count_matrix.toarray()             #轉成one_hat型式

#2.做TF/IDF
# from sklearn.feature_extraction.text import TfidfTransformer
# tfidf = TfidfTransformer().fit_transform(count_matrix)

#3.使用餘弦計算相似度(各向量所夾的角度)
cosine_sim = cosine_similarity(count_matrix, count_matrix)
# print(cosine_sim)
indices = pd.Series(df['電影中文名'])

#儲存相似度矩陣
import numpy as np
import time
np.savetxt('movie_correlation_matrix2',cosine_sim)

#讀取矩陣
# cosine_sim = np.loadtxt('movie_correlation_matrix')

def recommend(title, cosine_sim,indices):
    recommended_movies = []
    idx = indices[indices == title].index[0]                                        #每部電影的index
    score_series = pd.Series(cosine_sim[idx]).sort_values(ascending = False)        #求出對應該index的電影相似度indx和相似程度%
    top_10_indices = list(score_series.iloc[1:11].index)                            #列出除了自己的另外10部相似程度最高的電影index
    for i in top_10_indices:
        recommended_movies.append(list(df['電影中文名'])[i])                         #挑出index對映的電影名稱
    print(recommended_movies)

def main():
    start = time.time()
    cosine_sim = np.loadtxt('movie_correlation_matrix')
    indices = pd.Series(df['電影中文名'])
    movie=input('輸入一個電影名:')
    recommend(movie,cosine_sim,indices)
    end=time.time()
    total=end-start
    print(total)

if __name__ == '__main__':
    main()
