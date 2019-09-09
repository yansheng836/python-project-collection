# -*- coding: utf-8 -*-
import sqlite3

#大家要改成自己的路径
history_db = '/Users/Marcel/Desktop/tmp/code/chrome_history/History'

# 1.连接history_db
c = sqlite3.connect(history_db)
cursor = c.cursor()


# 2.选取我们想要的网址和访问时间
try:
    select_statement = "SELECT url,datetime(last_visit_time/1000000-11644473600,'unixepoch','localtime') AS tm FROM urls WHERE julianday('now') - julianday(tm) < 1 ORDER BY tm;"
    cursor.execute(select_statement)
except sqlite3.OperationalError:
    print("[!] The database is locked! Please exit Chrome and run the script again.")
    quit()

# 3.将网址和访问时间存入result.txt文件
results = cursor.fetchall()
with open('/Users/Marcel/Desktop/tmp/code/chrome_history/result.txt','w') as f:#改成自己的路径
    for i in range(len(results)):
        f.write(results[i][1]+'\n')
        f.write(results[i][0]+'\n')