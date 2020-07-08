import pymysql
import pandas as pd

#先去SQL建立好資料庫名稱(movie_test)&標格名稱(Basic_content)
#連接MySQL
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='u65p0123', db='movie_test', charset='utf8mb4')
print('Successfully connected!')
#建立游標
cursor = conn.cursor()

#將csv寫入SQl
df=pd.read_csv('m.csv')
counts = 0      #計算筆數
for each in df.values:          # 每一條資料都應該單獨新增，所以每次新增的時候都要重置一遍sql語句
        sql = 'insert into '+'Basic_content'+' values('
        for i,n in enumerate(each):             # 因為每條資料都是一個列表，所以使用for迴圈遍歷一下依次新增
            if i < (len(each) - 1):
                sql = sql + '"' + str(n) + '"' + ','            #因為不是數值需要加雙引號(""),且最後加逗號
            else:
                sql = sql + '"' + str(n) + '"'                  #最後一條的時候不能新增逗號
        sql = sql + ');'
        print(sql)
        # 當添加當前一條資料sql語句完成以後，需要執行並且提交一次
        cursor.execute(sql)
        # 提交sql語句執行操作
        conn.commit()
        # 沒提交一次就計數一次
        counts += 1
        # 使用一個輸出來提示一下當前存到第幾條了
        print('成功添加了' + str(counts) + '條資料 ')
cursor.close()
conn.close()