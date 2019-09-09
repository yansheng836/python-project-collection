# coding=utf-8
import threading
import MySQLdb
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from log import logger
 
 
def get_con():
    host = "127.0.0.1"
    port = 3306
    logsdb = "logsdb"
    user = "root"
    password = "never tell you"
    con = MySQLdb.connect(host=host, user=user, passwd=password, db=logsdb, port=port, charset="utf8")
    return con
 
 
def calculate_time():
 
    now = time.mktime(datetime.now().timetuple())-60*2
    result = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
    return result
 
 
def get_data():
    select_time = calculate_time()
    logger.info("select time:"+select_time)
    sql = "select file_name,message from logsdb.app_logs_record " \
          "where log_time >"+"'"+select_time+"'" \
          "and level="+"'ERROR'" \
          "order by log_time desc"
    conn = get_con()
 
    cursor = conn.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
 
    cursor.close()
    conn.close()
 
    return results
 
 
def send_email(content):
 
    sender = "sender_monitor@163.com"
    receiver = ["rec01@163.com", "rec02@163.com"]
    host = 'smtp.163.com'
    port = 465
    msg = MIMEText(content)
    msg['From'] = "sender_monitor@163.com"
    msg['To'] = "rec01@163.com,rec02@163.com"
    msg['Subject'] = "system error warning"
 
    try:
        smtp = smtplib.SMTP_SSL(host, port)
        smtp.login(sender, '123456')
        smtp.sendmail(sender, receiver, msg.as_string())
        logger.info("send email success")
    except Exception, e:
        logger.error(e)
 
 
def task():
    while True:
        logger.info("monitor running")
        results = get_data()
        if results is not None and len(results) > 5:
            content = "recharge error："
            logger.info("a lot of error,so send mail")
            for r in results:
                content += r[1]+'\n'
            send_email(content)
        time.sleep(2*60)
 
 
def run_monitor():
    monitor = threading.Thread(target=task)
    monitor.start()
 
 
if __name__ == "__main__":
    run_monitor()



[program:app-monitor]
command = python /root/monitor/app_monitor.py
directory = /root/monitor
user = root