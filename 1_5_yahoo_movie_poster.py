'''
yahoo電影海報
'''
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
import csv
if not os.path.exists('./Project_movie/images'):
    os.mkdir('./Project_movie/images')

new_columns=['電影ID','電影海報連結']
df=pd.DataFrame(columns=new_columns)
df.to_csv('./movie_images.csv',index=False,encoding='utf-8-sig')

data=pd.read_csv('./ok/movie_copy.csv')
id_list=list(data['電影ID'])
l=[]
for n,id in enumerate(id_list):
    try:
        url='https://movies.yahoo.com.tw/movieinfo_main.html/id={}'.format(id)
        headers={'...'}#帶自己的
        res=requests.get(url,headers=headers)
        soup=BeautifulSoup(res.text,'html.parser')
        #電影海報
        p_soup=soup.select('div[class="movie_intro_foto"] img')
        p_url=p_soup[0]['src']
        print(id , p_url)
        data = [id, p_url]
        with open('./movie_images.csv', 'a', newline='', encoding='utf-8') as csvfile:
            rows = csv.writer(csvfile)
            rows.writerow(data)

        r = requests.get(p_url,headers=headers)
        with open('./images/{}.jpg'.format(id), 'wb') as f:
            f.write(r.content)
            #.content:圖片下載
        if id % 100 ==0:
            time.sleep(30)
    except IndexError:
        print(id)
        print(n)
        l.append(n)
        continue
print(l)
