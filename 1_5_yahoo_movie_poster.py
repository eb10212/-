'''
yahoo電影海報
'''
import pandas as pd
import requests
from bs4 import BeautifulSoup
import os
import time
import csv
if not os.path.exists('Project_movie/images'):
    os.mkdir('Project_movie/images')

new_columns=['電影ID','電影海報連結']
df=pd.DataFrame(columns=new_columns)
df.to_csv('./5_movie_images.csv',index=False,encoding='utf-8-sig')

data=pd.read_csv('Project_movie/1_movie.csv')
id_list=list(data['電影ID'])
l=[]
for n,id in enumerate(id_list):
    try:
        url='https://movies.yahoo.com.tw/movieinfo_main.html/id={}'.format(id)
        headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}
        res=requests.get(url,headers=headers)
        soup=BeautifulSoup(res.text,'html.parser')
        #電影海報
        p_soup=soup.select('div[class="movie_intro_foto"] img')
        p_url=p_soup[0]['src']
        print(id , p_url)
        data = [id, p_url]
        with open('Project_movie/5_movie_images.csv', 'a', newline='', encoding='utf-8') as csvfile:
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