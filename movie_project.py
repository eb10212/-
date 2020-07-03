import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

data=[]
for id in range(10345,10346):
    try:
        #Yahoo編號(id)
        print(id)
        url='https://movies.yahoo.com.tw/movieinfo_main.html/id={:05d}'.format(id)
        res=requests.get(url)
        soup=BeautifulSoup(res.text,'html.parser')
        #電影名稱-中英文
        title_soup1=soup.select('div[class="movie_intro_info_r"] h1')
        title_soup2=soup.select('div[class="movie_intro_info_r"] h3')
        title1=title_soup1[0].text
        title2=title_soup2[0].text
        # print(title1)
        # print(title2)
        #上映日期/片長/發行公司/IMDb分數
        list_soup = soup.select('div[class="movie_intro_info_r"] span')
        date=list_soup[0].text
        time=list_soup[1].text
        company=list_soup[2].text
        IMDb=list_soup[3].text
        # print(date)
        # print(time)
        # print(company)
        if IMDb != '導演：':
            # print(IMDb)
            IMDb = list_soup[3].text
        else:
            # print('沒有評分')
            IMDb ='沒有評分'

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
        #電影類型
        type_soup = soup.select('div[class="level_name"] a')
        type=[]
        for i in range(len(type_soup)):
            if i !=len(type_soup)-1:
                # print(type_soup[i].text.strip(),end=',')
                type.append(type_soup[i].text.strip())
            else:
                # print(type_soup[i].text.strip())
                type.append(type_soup[i].text.strip())
        # 電影分級
        class_soup = soup.select('div[class="movie_intro_info_r"] div')
        class_year=class_soup[0]['class']
        if class_year ==[]:
            class_year='未分類'
            # print('未分類')
        else:
            for i in class_year:
                y=i.split('_')[1]
                if y=='0':
                    class_year ='普遍級/G'
                    # print('普遍級/G')
                if y =='6':
                    class_year ='保護級/P'
                    # print('保護級/P')
                elif y =='12':
                    class_year ='輔12級/PG12'
                    # print('輔12級/PG12')
                elif y =='15':
                    class_year ='輔15級/PG15'
                    # print('輔15級/PG15')
                elif y =='18':
                    class_year ='限制級/R'
                    # print('限制級/R')
        #電影簡介-參照movie_summary.py

        # print('========================')
        data_c=[id,title1,title2,date,time,company,IMDb,director,actor,type,class_year]
        data.append(data_c)
    except IndexError:
        print(id)
        continue

# columns=['電影ID','電影中文名','英譯','上映日期','片長','發行公司','IMDb分數','導演','演員','電影類型','分級']
# df=pd.DataFrame(columns=columns,data=data)
# df.to_csv('./movie.csv',index=False,encoding='utf-8-sig')




