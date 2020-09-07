#改善movie_add.csv的電影評論格式為yahoo_comment.csv

import pandas as pd
with open('./movie_add.csv','r',encoding='utf-8-sig')as f:
    a=f.readlines()#讀出來為一個list且每列為一個str,len(a)=總列數

for i in a:
    s=i.split('|')      #先將每列str轉成單獨的list
    tmp=s[:4]
    s='|'.join(tmp) + '|' +str(s[4:5]).replace("[",'').replace("'","").replace("]",'')  #前4欄先在轉成str,第5欄(評論)去除一些符號後也轉為str
    ts=s.split('|')     #再轉成list??????
    with open('./yahoo_comment.csv','a',encoding='utf-8')as f:
         f.write(str(s) + '\n')

#查看資料panda呈現方式
# with open('./yahoo_comment.csv','r',encoding='utf-8')as f:
#     data_view=f.readlines()
#
# data=[item.split('|') for item in data_view]
# df=pd.DataFrame(data=[item for item in data[1:]],columns=data_view[0].split('|'))
# print(df)