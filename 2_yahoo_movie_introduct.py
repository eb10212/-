'''
Step1-2:網路爬蟲

1.  yahoo 電影簡介:
2.  定期新增(重新執行)

'''
from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import os
import time

#以下用來取出電影大綱
def movie_Introduction(id):
    url = 'https://movies.yahoo.com.tw/movieinfo_main.html/id={}'.format(id)
    about_data = []
    # 方式3:與用手機版面
    useragent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'
    headers = {'User-Agent': useragent,
               'x-requested-with': 'XMLHttpRequest'}
    cookie = {'nexagesd': '4'}

    res = requests.get(url, headers=headers, data=cookie)

    soup = BeautifulSoup(res.text, 'html.parser')
    # print(soup)
    summary_soup = soup.select('div[class="plot-intro-txt limit"]')
    summary = summary_soup[0].text
    new_summary = summary.replace(",", "，").replace("\n", "").replace(r"\xa0", "")
    about_data = [id, new_summary]

    with open('./Project_movie/2_movie_about.csv', 'a', newline='', encoding='utf-8') as csvfile:
        rows = csv.writer(csvfile)
        rows.writerow(about_data)

    print(id, '完成')

def main():
    data = pd.read_csv('./Project_movie/1_movie.csv')
    id_list_1 = int(list(data['電影ID'])[-1])+1



    if not os.path.isfile('./Project_movie/2_movie_about.csv'):
        new_columns = ['電影ID', '電影簡介']
        df = pd.DataFrame(columns=new_columns)
        df.to_csv('./Project_movie/2_movie_about.csv', index=False, encoding='utf-8-sig')
        id_list_2=1

    else:
        data2=pd.read_csv('./Project_movie/2_movie_about.csv')
        id_list_2 = int(list(data2['電影ID'])[-1])+1

    for id in range(id_list_2,id_list_1):
        try:
            movie_Introduction(id)

        except IndexError:
            print(id,'未完成')
            with open('./Project_movie/2_movie_about_lose.csv', 'a', newline='', encoding='utf-8') as f:
                f.write(str(id))
            continue

        except requests.exceptions.ChunkedEncodingError as e:
            print(id,'等待中')
            time.sleep(60)
            movie_Introduction(id)

if __name__ == '__main__':
    main()
