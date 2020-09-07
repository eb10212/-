'''
yahoo電影資料清洗&合併
    重複的電影名稱/特別符號/冗字
基本資料+簡介
'''
import pandas as pd
df1=pd.read_csv('./ok/movie_copy.csv',encoding='utf-8')
df2=pd.read_csv('./ok/movie_about.csv')
data = pd.merge(df1, df2, on=['電影ID', '電影ID'], how='left') # pandas csv表左連線
# print(data.head())

all_columns=data.columns
# print(all_columns)
# data.to_csv('./movie_all.csv', encoding='utf-8',index=False)
#
# df=pd.read_csv('./movie_all.csv')
# print(df.columns)

def tmpfilter(s):
    try:
        return s.replace('上映日期：','').replace('片　　長：','').replace('發行公司：','').replace('[','').replace(']','').replace(' ','')
    except AttributeError:
        s=str(s)
        return s.replace('上映日期：', '').replace('片　　長：', '').replace('發行公司：', '').replace('[', '').replace(']','').replace(' ', '')
def tmpfilters2(s):
    a=s.replace(r'.','_初版')

    return a


for i in data.columns:
    for c in data[i]:
        data[i]=data[i].apply(tmpfilter)
for i in data['電影中文名']:
    data['電影中文名']=data['電影中文名'].apply(tmpfilters2)

c=[]
for i in range(len(data['電影中文名'])):
    if data['電影中文名'][i] not in c:
        c.append(data['電影中文名'][i])
    else:
        data['電影中文名'][i]=data['電影中文名'][i]+'_改版'
        c.append(data['電影中文名'][i])

data.to_csv('./movie_all_2.csv', encoding='utf-8',index=False)


# s='上映日期：2001-10-19'
# print(tmpfilter(s))
#
# def tmpfilter(s):
#     if not s:
#         return '無'
#     else:
#         return s
# for c in columns:
#     df[c] = df[c].apply(tmpfilter)