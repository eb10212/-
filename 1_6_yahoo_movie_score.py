'''
Step1-3:網路爬蟲

1.  yahoo 電影評論:
    新增 滿意度/投票人數/評論人數的爬取

'''
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time

data=pd.read_csv('./Project_movie/1_movie.csv')
id_list=list(data['電影ID'])
# id_list=[10345,10227]
if not os.path.isfile('./Project_movie/3_movie_add.csv'):
    new_columns=['電影ID','滿意度','投票人數','評論人數']
    df=pd.DataFrame(columns=new_columns)
    df.to_csv('./Project_movie/3_movie_add.csv',index=False,encoding='utf-8-sig')

for id in id_list:
    add_column_data = []
    url='https://movies.yahoo.com.tw/movieinfo_main.html/id={}'.format(id)
    res=requests.get(url)
    soup=BeautifulSoup(res.text,'html.parser')
    print(id)

    #滿意度-satisfaction
    try:
        satisfaction_soup=soup.select('div[class="score_num count"]')
        satisfaction=satisfaction_soup[0].text
        # print(satisfaction)
    except IndexError:
        satisfaction = 'none'

    #投票人數-vote
    try:
        vote_soup = soup.select('div[class="starbox2"]')
        vote = vote_soup[0].text.strip().strip(r'(共').strip(r'人投票)')
        # print(vote)
    except IndexError:
        vote ='0'

    #評論人數-people
    try:
        people_soup=soup.select('div[class="title_num"]')[-1].text
        # print(people_soup)
        people=int(people_soup.strip('共').strip('則'))
        # print(type(people))
        # print(people)
        people_page=(people//10)+1
        # print(people)
        if id % 500 ==0:
            time.sleep(60)

    # # 評論-comment_list
    #     page = 1
    #     comment_list = []
    #     while page <= people_page:
    #         try:
    #             # print(page)
    #             url = 'https://movies.yahoo.com.tw/movieinfo_review.html/id={}?page={}'.format(id, page)
    #             res = requests.get(url)
    #             soup = BeautifulSoup(res.text, 'html.parser')
    #
    #             comment_soup = soup.select('ul[class="usercom_list"] span')
    #             # print(type(comment_soup[0].text))
    #             for comment in comment_soup:
    #                 if comment.text == '':
    #                     continue
    #                 else:
    #                     comment_list.append(comment.text)
    #             page += 1
    #         except IndexError:
    #             page += 1
    #             continue

    except IndexError:
        people ='none'
        comment_list='none'
        continue
    except ValueError:
        print('檢查',id)
        continue

    add_column = [id, satisfaction, vote, people]

    with open('./Project_movie/3_movie_add.csv', 'a', newline='', encoding='utf-8') as csvfile:
        rows = csv.writer(csvfile)
        rows.writerow(add_column)




    # add_column=[id,satisfaction,vote,people,comment_list]
    # add_column_data.append(add_column)

    # with open('./movie_add.csv','a',encoding='utf-8') as f:
    #     for i in add_column:
    #         f.write(str(i)+ '|')
    #     f.write('\n')
# print(add_column_data)
#
# new_columns=['電影ID','滿意度','投票人數','評論人數','評論']
# print(add_column_data)
# # # data = pd.read_csv('m.csv')
# df=pd.DataFrame(columns=new_columns,data=add_column_data)
# df.to_csv('./movie_add2.csv',index=False,encoding='utf-8-sig')
