'''
使用python連結mongodb,查詢相似電影
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

def movie_exist(m):
    return db.movie_similarity.count({'電影中文名': m})


def main():
    c=0
    while c==0 :
        input_movie = input('請輸入電影名稱:')
        c=movie_exist(input_movie)
        if c!=0 and input_movie!='q':
            input_count = int(input('要推薦幾部:'))
            movie_recommend(input_movie, input_count)
            c=0
        elif c==0 and input_movie == 'q':
            print('再會~')
            break
        else:
            print('名稱輸入有誤,請重新輸入或輸入q離開')
            c=0

if __name__ == '__main__':
    main()







