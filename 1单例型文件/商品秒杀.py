import os
from selenium import webdriver
import datetime
import time
print('python学习群：516107834')
#需要下载deckodreiver
firefox = os.path.abspath(r"E:\Program Files\Mozilla Firefox\firefox.exe")
os.environ["webdriver.firefox.bin"] = firefox
driver = webdriver.Firefox()
driver.maximize_window()
 
def login(uname, pwd):
 driver.get("https://www.taobao.com")
 if driver.find_element_by_link_text("亲，请登录"):
  driver.find_element_by_link_text("亲，请登录").click()
 input(uname, pwd)
 
 #点击购物车里全选按钮
 if driver.find_element_by_id("J_SelectAll1"):
  driver.find_element_by_id("J_SelectAll1").click()
 # time.sleep(3)
 now = datetime.datetime.now()
 print('login success:', now.strftime('%Y-%m-%d %H:%M:%S'))
 
def input(uname,pwd):
 time.sleep(3)
 #选择密码登录
 if driver.find_element_by_id("J_Quick2Static"):
  driver.find_element_by_id("J_Quick2Static").click()
 time.sleep(3)
 
 #用户名输入
 if driver.find_element_by_name("TPL_username"):
  for i in uname:
   driver.find_element_by_name("TPL_username").send_keys(i)
   time.sleep(0.5)
 time.sleep(3)
 
 #密码输入
 if driver.find_element_by_name("TPL_password"):
  for j in pwd:
   driver.find_element_by_name("TPL_password").send_keys(j)
   time.sleep(0.5)
 time.sleep(3)
 
 #点击登录按钮
 if driver.find_element_by_id("J_SubmitStatic"):
  driver.find_element_by_id("J_SubmitStatic").click()
 time.sleep(3)
 driver.get("https://cart.taobao.com/cart.htm")
 time.sleep(2)
 
def buy(buytime):
 while True:
  now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  if now == buytime:
    try:
     #点击结算按钮
     if driver.find_element_by_id("J_Go"):
      driver.find_element_by_id("J_Go").click()
     driver.find_element_by_link_text('提交订单').click()
    except:
     time.sleep(1)
  print(now)
  time.sleep(1)
if __name__=="__main__":
 #中文账号记得decode编码
 login("账号",'密码')
 buy('2018-11-11 00:00:00')
