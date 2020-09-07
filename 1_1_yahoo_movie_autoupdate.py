'''
Step1-1:網路爬蟲

1.  yahoo 電影基本資料:
    電影ID,電影中文名,英譯,上映日期,片長,發行公司,IMDb分數,導演,演員,電影類型,分級
2.  定期新增(重新執行)

'''
import requests
from bs4 import BeautifulSoup
import csv
import os
#MAC要加下列
import ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context
import time


#舊有電影查詢
def id_search():
    id=[]
    with open('./Project_movie/1_movie.csv',encoding='utf-8') as f:
        reader = csv.reader(f)
        for i in reader:
            id.append(i[0])
    id.pop(0)
    id=list(map(int,id))
    return id[-1]

#電影基本資料
def movie_content(id_new):
    data=[]
    id=id_new
    url = 'https://movies.yahoo.com.tw/movieinfo_main.html/id={:05d}'.format(id_new)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    # 電影名稱-中英文
    title_soup1 = soup.select('div[class="movie_intro_info_r"] h1')
    title_soup2 = soup.select('div[class="movie_intro_info_r"] h3')
    title1 = title_soup1[0].text
    title2 = title_soup2[0].text
    # print(title1)
    # print(title2)
    # 上映日期/片長/發行公司/IMDb分數
    list_soup = soup.select('div[class="movie_intro_info_r"] span')
    date = list_soup[0].text
    time = list_soup[1].text
    company = list_soup[2].text
    # print(date)
    # print(time)
    # print(company)
    IMDb = list_soup[3].text
    if IMDb != '導演：':
        # print(IMDb)
        IMDb = list_soup[3].text
    else:
        # print('沒有評分')
        IMDb = '沒有評分'

    # 導演
    people_soup1 = soup.select('div[class="movie_intro_info_r"] div[class="movie_intro_list"]')
    people1 = people_soup1[0].text.strip().split('\n')
    director = []
    for i in people1:
        d = i.strip()
        if d != '、':
            director.append(d)
    # for i in director:
    #     if i != director[len(director) - 1]:
    #         print(i, end=',')
    #     else:
    #         print/(i)
    # 演員
    people2 = people_soup1[1].text.strip().split('\n')
    actor = []
    for i in people2:
        a = i.strip()
        if a != '、':
            actor.append(a)
    # for i in actor:
    #     if i != actor[len(actor) - 1]:
    #         print(i, end=',')
    #     else:
    #         print(i)
    # 電影類型
    type_soup = soup.select('div[class="level_name"] a')
    type = []
    for i in range(len(type_soup)):
        if i != len(type_soup) - 1:
            # print(type_soup[i].text.strip(),end=',')
            type.append(type_soup[i].text.strip())
        else:
            # print(type_soup[i].text.strip())
            type.append(type_soup[i].text.strip())
    # 電影分級
    class_soup = soup.select('div[class="movie_intro_info_r"] div')
    class_year = class_soup[0]['class']
    if class_year == []:
        class_year = '未分類'
        # print('未分類')
    else:
        for i in class_year:
            y = i.split('_')[1]
            if y == '0':
                class_year = '普遍級/G'
                # print('普遍級/G')
            if y == '6':
                class_year = '保護級/P'
                # print('保護級/P')
            elif y == '12':
                class_year = '輔12級/PG12'
                # print('輔12級/PG12')
            elif y == '15':
                class_year = '輔15級/PG15'
                # print('輔15級/PG15')
            elif y == '18':
                class_year = '限制級/R'
                # print('限制級/R')
    data_c = [id, title1, title2, date, time, company, IMDb, director, actor, type, class_year]
    data.append(data_c)
    return data



def main():

    if os.path.isfile('./Project_movie/1_movie.csv'):
        id_new = id_search() + 1  # 從列表中搜尋上一次最後一筆之後開始
    else :
        print('請檢查是否路徑設置錯誤或要重新抓取')
        cheack=input('若是路徑錯誤請按q,重新跑請按r:')
        if cheack=='r':
            os.mkdir('./Project_movie/movie_re.csv')
            id_new=1
        else:
            id_new=0
    if id_new !=0:
        n = 0
        m = 0
        o = 0
        while n < 20:  # 只要中間空格超過20筆,視為沒有新的電影id************************************
            try:
                renew_movie_content = movie_content(id_new)
                n = 0
                # print(renew_movie_content)#改為加入csv****************************************
                with open('./Project_movie/1_movie.csv', 'a', newline='', encoding='utf-8') as csvfile:
                    for id_content in renew_movie_content:
                        rows = csv.writer(csvfile)
                        rows.writerow(id_content)
                o += 1
                id_new += 1
                print('新增ID=',id_new)
                if id_new % 500 ==0:
                    time.sleep(60)

            except IndexError:
                n += 1
                m += 1
                id_new += 1
                continue
        print('以更新至id={}'.format(id_new - 20 - 1))
        print('此次更新{}筆'.format(o))
    else:
        print('nothing to do')





    # #1.先搜尋有無補舊的空缺id
    # for id_old in lose_id_search(id):
    #     try:
    #         old_movie_content = movie_content(id_old)
    #         print(old_movie_content)  # 改為加入csv****************************************
    #
    #     except IndexError:
    #         print(id_old)
    #         continue

    #2.找尋新增id



if __name__ == '__main__':
    main()




