'''
使用python連結mongodb,查詢相似電影
含yahoo,IMDB
'''
from pymongo import MongoClient
con = MongoClient('mongodb://localhost:27017/')
db = con.Movie_project

def movie_recommend(input_movie,input_count):
    r = db.movie_similarity.find({'電影中文名': '{}'.format(input_movie)}, {'其他電影相似度': 1})
    for item in r:
        s=item['其他電影相似度']
        l=sorted(s.items(),key=lambda item:item[1],reverse=True)
        l=l[:input_count]
        for top_i in l:
            print(top_i[0])

def movie_recommend_imdb(input_movie,input_count):
    r = db.movie_similarity_IMDB_new.find({'IMDB電影名': '{}'.format(input_movie)}, {'其他電影相似度': 1})
    for item in r:
        s=item['其他電影相似度']
        l=sorted(s.items(),key=lambda item:item[1],reverse=True)
        l=l[:input_count]
        for top_i in l:
            print(top_i[0])

# print(movie_recommend_imdb('The Avengers',2))

# def movie_exist(m):
#     return db.movie_similarity.count({'電影中文名': m})

# def movie_exist2(m):
#     if db.movie_similarity_IMDB_new.count({'IMDB電影名': m})>0:
#         return 2
#     else:
#         return 0
#
# print(movie_exist2('The Avengers'))
# print(type(movie_exist2('The Avengers')))

def movie_exist_all(m):
    if db.movie_similarity.count({'電影中文名': m})>0:
        return 1
    elif db.movie_similarity_IMDB_new.count({'IMDB電影名': m})>0:
        return 2
    else:
        return 0
# print(movie_exist_all('億男'))
# print(movie_exist_all('The Avengers'))


def main():
    c=0
    while c==0 :
        input_movie = input('請輸入電影名稱:').replace(r'.','')
        # c=movie_exist(input_movie)
        c = movie_exist_all(input_movie)
        if c== 1 and input_movie!='q':
            input_count = int(input('要推薦幾部:'))
            movie_recommend(input_movie, input_count)
            c=0
        elif c== 2 and input_movie!='q':
            input_count = int(input('要推薦幾部:'))
            movie_recommend_imdb(input_movie, input_count)
            c=0
        elif c==0 and input_movie == 'q':
            print('再會~')
            break
        else:
            print('名稱輸入有誤,請重新輸入或輸入q離開')
            c=0

if __name__ == '__main__':
    main()







