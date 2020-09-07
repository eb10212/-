'''
Step1-4:網路爬蟲

1.  yahoo 電影評論內容:
    新增 滿意度/投票人數/評論人數的爬取
2.  並依評分的星數放置不同資料夾
    後續做正負評訓練的資料

'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

#新增檔案資料夾
for s in range(1,6):
    if not os.path.exists('./Project_movie/positive_negative/moviestar{}'.format(s)):
        os.mkdir('./Project_movie/positive_negative/moviestar{}'.format(s))

data=pd.read_csv('./Project_movie/1_movie.csv')
id_list=list(data['電影ID'])

for id in id_list:

    count_people = pd.read_csv('./Project_movie/3_movie_add.csv', index_col='電影ID')
    people=count_people['評論人數'][id]
    people_page=(people//10)+1
    # 評論-comment_list
    page = 1
    while page <= people_page:
        try:
            url = 'https://movies.yahoo.com.tw/movieinfo_review.html/id={}?page={}'.format(id, page)
            res = requests.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')

            each_comment_soup = soup.select('ul[class="usercom_list"] li')
            for n,i in enumerate(each_comment_soup):
                # print(id)
                each_comment = str(i.select('span')[2]).strip('<span>').strip('</span>').replace(' ','').replace(',', '，')
                # print(each_comment)
                each_star = int(
                    str(i.select('input')[1]).strip('<input name="score" type="hidden" value="').strip('"/>'))
                # print(each_star)
                # print('=================================')
                for s in range(1, 6):
                    if each_star == s:
                        with open('./Project_movie/positive_negative/moviestar{}/{}_{}{}.txt'.format(s, id, page-1 ,n), 'w', encoding='utf-8')as f:
                            f.write(each_comment)
            page += 1
        except IndexError:
            print(id,'網頁已消失'.format(page))
            page += 1
            continue

    print(id,'已完成')