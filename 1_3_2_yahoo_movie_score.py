'''
Step1-3-2:網路爬蟲

1.  yahoo 電影評論:(多一欄評論內容)
    新增 滿意度/投票人數/評論人數的爬取

'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import time
import random

data=pd.read_csv('./Project_movie/1_movie.csv')
id_list=list(data['電影ID'])
# id_list=[10345,10227]

# new_columns=['電影ID','滿意度','投票人數','評論人數','評論']
# df=pd.DataFrame(columns=new_columns)
# df.to_csv('./movie_add2.csv',index=False,encoding='utf-8-sig')

for id in id_list:
    if int(id)%1000==0:
        time.sleep(random.randint(0, 300))

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
        people=int(people_soup.strip('共').strip('則').strip('張').strip('人'))
        # print(type(people))
        # print(people)
        people_page=(people//10)+1
        # print(people)
    # 評論-comment_list
        page = 1
        comment_list = []
        while page <= people_page:
            try:
                # print(page)
                url = 'https://movies.yahoo.com.tw/movieinfo_review.html/id={}?page={}'.format(id, page)
                res = requests.get(url)
                soup = BeautifulSoup(res.text, 'html.parser')

                comment_soup = soup.select('ul[class="usercom_list"] span')
                # print(type(comment_soup[0].text))
                for comment in comment_soup:
                    if comment.text == '':
                        continue
                    else:
                        comment_list.append(comment.text)
                page += 1
            except IndexError:
                page += 1
                continue

    except IndexError:
        people ='none'
        comment_list='none'

    add_column = [id, satisfaction, vote, people, comment_list]

    with open('./Project_movie/3_movie_comment.csv', 'a', newline='', encoding='utf-8') as csvfile:
        rows = csv.writer(csvfile)
        rows.writerow(add_column)



#=======================以下為其他方式=====================================
    # with open('./movie_add.csv','a',encoding='utf-8') as f:
    #     for i in add_column:
    #         f.write(str(i)+ '|')
    #     f.write('\n')
# print(add_column_data)
#

