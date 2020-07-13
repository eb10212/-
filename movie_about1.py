#存成json
#放入mongodb
#加快速度

from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import os
import time

#以下用來取出電影大綱

data=pd.read_csv('./movie_copy.csv')
id_list=list(data['電影ID'][6607:])
# id_list=[10345,10227]

# new_columns=['電影ID','電影簡介']
# df=pd.DataFrame(columns=new_columns)
# df.to_csv('./movie_about.csv',index=False,encoding='utf-8-sig')


for id in id_list:
    try:
        url ='https://movies.yahoo.com.tw/movieinfo_main.html/id={}'.format(id)
        about_data = []
        #方式3:與用手機版面
        useragent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'
        headers = {'User-Agent': useragent,
                   'x-requested-with': 'XMLHttpRequest'}
        cookie = {'nexagesd': '4'}

        res = requests.get(url,headers=headers,data=cookie)

        soup = BeautifulSoup(res.text, 'html.parser')
        # print(soup)
        summary_soup=soup.select('div[class="plot-intro-txt limit"]')
        summary=summary_soup[0].text
        new_summary = summary.replace(",","，").replace("\n","").replace(r"\xa0","")
        about_data=[id,new_summary]

        with open('./movie_about.csv', 'a', newline='', encoding='utf-8') as csvfile:
            rows = csv.writer(csvfile)
            rows.writerow(about_data)

        print(id,'完成')
    except IndexError:
        print(id,'未完成')
        with open('./movie_about_lose.csv', 'a', newline='', encoding='utf-8') as f:
            f.write(id)
        continue

    except requests.exceptions.ChunkedEncodingError as e:
        print(id,'等待中')
        time.sleep(60)


        # with open('./movie_about.csv','a',encoding='utf-8') as f:
        #     for i in about_data:
        #         f.write(str(i)+ '|')
        #     f.write('\n')
        # print(add_column_data)