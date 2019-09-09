########################################################
# Python学习交流群：548377875
#源码+微信：mmp9972
# 火车票抢票系统V1.0
########################################################
import requests
import Station_Parse
import threading
import os
from datetime import datetime
from splinter.browser import Browser
from time import sleep
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
from requests.packages.urllib3.exceptions import InsecureRequestWarning
# 忽视该警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)



# 车票查询部分
#-------------------------------------------------------------------------------------------------------------------------------------------
# 数据处理+显示
class Trains_Demo():
	# 初始化
	def __init__(self, txt_show_ticket, raw_trains, option):
		self.headers = '车次： 车站： 时间： 历时： 商务/特等座： 一等座： 二等座： 高级软卧： 软卧： 动卧： 硬卧： 软座： 硬座： 无座：'.split()
		self.raw_trains = raw_trains
		self.option = option
		txt_show_ticket.delete(1.0, END)
	# 获取出发和到达站
	def get_from_to_station_name(self, data_list):
		self.from_station_name = data_list[6]
		self.to_station_name = data_list[7]
		self.from_to_station_name = Station_Parse.parse_station().disparse(self.from_station_name) + '-->' + Station_Parse.parse_station().disparse(self.to_station_name)
		return self.from_to_station_name
	# 获得出发和到达时间
	def get_start_arrive_time(self, data_list):
		self.start_arrive_time = data_list[8] + '-->' + data_list[9]
		return self.start_arrive_time
	# 解析trains数据(与headers依次对应)
	def parse_trains_data(self, data_list):
		return {
			'trips': data_list[3],
			'from_to_station_name': self.get_from_to_station_name(data_list),
			'start_arrive_time': self.get_start_arrive_time(data_list),
			'duration': data_list[10],
			'business_premier_seat': data_list[32] or '--',
			'first_class_seat': data_list[31] or '--',
			'second_class_seat': data_list[30] or '--',
			'senior_soft_sleep': data_list[21] or '--',
			'soft_sleep': data_list[23] or '--',
			'move_sleep': data_list[33] or '--',
			'hard_sleep': data_list[28] or '--',
			'soft_seat': data_list[24] or '--',
			'hard_seat': data_list[29] or '--',
			'no_seat': data_list[26] or '--',
			}
	# 判断是否需要显示
	def need_show(self, data_list):
		self.trips = data_list[3]
		initial = self.trips[0].lower()
		if 'a' in self.option:
			return self.trips
		else:
			return(initial in self.option)
	# 数据显示
	def show_trian_data(self):
		self.t_num = 0
		for self.train in self.raw_trains:
			self.data_list = self.train.split('|')
			if self.need_show(self.data_list):
				self.values_row = []
				self.parsed_train_data = self.parse_trains_data(self.data_list)
				self.values_row.append(self.headers[0] + self.parsed_train_data['trips'])
				self.values_row.append(self.headers[1] + self.parsed_train_data['from_to_station_name'])
				self.values_row.append(self.headers[2] + self.parsed_train_data['start_arrive_time'])
				self.values_row.append(self.headers[3] + self.parsed_train_data['duration'])
				self.values_row.append(self.headers[4] + self.parsed_train_data['business_premier_seat'])
				self.values_row.append(self.headers[5] + self.parsed_train_data['first_class_seat'])
				self.values_row.append(self.headers[6] + self.parsed_train_data['second_class_seat'])
				self.values_row.append(self.headers[7] + self.parsed_train_data['senior_soft_sleep'])
				self.values_row.append(self.headers[8] + self.parsed_train_data['soft_sleep'])
				self.values_row.append(self.headers[9] + self.parsed_train_data['move_sleep'])
				self.values_row.append(self.headers[10] + self.parsed_train_data['hard_sleep'])
				self.values_row.append(self.headers[11] + self.parsed_train_data['soft_seat'])
				self.values_row.append(self.headers[12] + self.parsed_train_data['hard_seat'])
				self.values_row.append(self.headers[13] + self.parsed_train_data['no_seat'])
				self.t_num += 1
				txt_show_ticket.insert(END, '第%d班：' % self.t_num + '*'*80)
				txt_show_ticket.insert(END, '\n')
				txt_show_ticket.insert(END, self.values_row)
				txt_show_ticket.insert(END, '\n')
				
# 车票查询
class Query_Ticket():
	# 初始化
	def __init__(self, txt_show_ticket, ticket_option, from_station, to_station, date):
		# 请求地址的模板
		self.url_template = (
		'https://kyfw.12306.cn/otn/leftTicket/query{}?leftTicketDTO.'
		'train_date={}&'
		'leftTicketDTO.from_station={}&'
		'leftTicketDTO.to_station={}&'
		'purpose_codes=ADULT'
		)
		self.ticket_option = ticket_option
		self.from_station = from_station
		self.to_station = to_station
		self.date = date
	# 获得请求地址
	def request_url1(self):
		return(self.url_template.format('A', self.date, self.from_station, self.to_station))
	def request_url2(self):
		return(self.url_template.format('Z', self.date, self.from_station, self.to_station))
	# 查询车票
	def query(self):
		self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3294.6 Safari/537.36'}
		self.res = requests.get(self.request_url1(), headers=self.headers, verify=False)
		try:
			try:
				self.trains = self.res.json()['data']['result']
			except:
				self.res = requests.get(self.request_url2(), headers=self.headers, verify=False)
				self.trains = self.res.json()['data']['result']
			Trains_Demo(txt_show_ticket, self.trains, self.ticket_option).show_trian_data()
		except:
			title = '提示'
			message = '出了点小问题，请重新点击按钮！'
			messagebox.showinfo(title, message)
#-------------------------------------------------------------------------------------------------------------------------------------------



# 抢票部分
#-------------------------------------------------------------------------------------------------------------------------------------------
# 抢票
class Buy_Tickets(object):
	# 初始化
	def __init__(self, username, passwd, order, passengers, dtime, starts, ends):
		self.url_template = (
		'https://kyfw.12306.cn/otn/leftTicket/query{}?leftTicketDTO.'
		'train_date={}&'
		'leftTicketDTO.from_station={}&'
		'leftTicketDTO.to_station={}&'
		'purpose_codes=ADULT'
		)
		self.username = username
		self.passwd = passwd
		# 日期
		self.dtime = dtime
		# 乘客名
		self.passengers = passengers.split('，')
		# 起始地和终点
		self.starts = Station_Parse.parse_station().parse(starts)
		self.ends = Station_Parse.parse_station().parse(ends)
		if self.starts is None or self.ends is None:
			self.title = '提示'
			self.message = '请输入有效的车站名'
			messagebox.showinfo(self.title, self.message)
		# 车次
		self.order = order
		if self.order != '0':
			self.order = self.order_transfer()
			while(not self.order):
				sleep(1)
				self.order = self.order_transfer()
		# 起始地和终点转为cookie值
		self.starts = self.Get_Cookies()[0] + '%2C' + self.starts
		self.ends = self.Get_Cookies()[1] + '%2C' + self.ends
		self.login_url = 'https://kyfw.12306.cn/otn/login/init'
		self.initMy_url = 'https://kyfw.12306.cn/otn/index/initMy12306'
		self.ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
		self.driver_name = 'chrome'
		self.executable_path = 'D:\\Python35\\Scripts\\chromedriver.exe'
	# 登录
	def login(self):
		self.driver.visit(self.login_url)
		self.driver.fill('loginUserDTO.user_name', self.username)
		self.driver.fill('userDTO.password', self.passwd)
		self.title = '提示'
		self.message = '请在自动打开的浏览器中输入验证码！'
		messagebox.showinfo(self.title, self.message)
		while True:
			if self.driver.url != self.initMy_url:
				sleep(1)
			else:
				break
	# 车次转换
	def order_transfer(self):
		self.headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3294.6 Safari/537.36'}
		self.res = requests.get(self.url_template.format('A', self.dtime, self.starts, self.ends), headers=self.headers, verify=False)
		try:
			try:
				self.trains = self.res.json()['data']['result']
			except:
				self.res = requests.get(self.url_template.format('Z', self.dtime, self.starts, self.ends), headers=self.headers, verify=False)
				self.trains = self.res.json()['data']['result']
			self.num = 0
			for self.train in self.trains:
				self.data_list = self.train.split('|')
				if self.data_list[3] == self.order:
					break
				self.num += 1
			if self.num == len(self.trains):
				self.title = '提示'
				self.message = '您输入的车次不存在，系统将自动选择任意车次！'
				messagebox.showinfo(self.title, self.message)
				self.num = '0'
			return self.num
		except:
			title = '提示'
			message = '因为网络原因正在重新尝试！'
			messagebox.showinfo(title, message)
			return None
	# 中文转Unicode
	def to_unicode(self, string):
		self.uni = ''
		for s in string:
			self.uni += hex(ord(s)).upper().replace('0X', '%u')
		return self.uni
	# 将起始地和终点转化为相应的Cookies
	def Get_Cookies(self):
		return [self.to_unicode(self.starts), self.to_unicode(self.ends)]
	# 买票
	def start_buy(self):
		self.driver = Browser(driver_name=self.driver_name, executable_path=self.executable_path)
		self.driver.driver.set_window_size(700, 500)
		self.login()
		self.driver.visit(self.ticket_url)
		try:
			self.title = '提示'
			self.message = '开始购票！'
			messagebox.showinfo(self.title, self.message)
			# 加载查询信息
			self.driver.cookies.add({"_jc_save_fromStation": self.starts})
			self.driver.cookies.add({"_jc_save_toStation": self.ends})
			self.driver.cookies.add({"_jc_save_fromDate": self.dtime})
			self.driver.reload()
			if self.order != '0':
				while self.driver.url == self.ticket_url:
					self.driver.find_by_text('查询').click()
					# self.title = '提示'
					# self.message = '开始尝试预订...'
					# messagebox.showinfo(self.title, self.message)
					try:
						self.driver.find_by_text('预订')[self.order].click()
						sleep(1.5)
					except:
						# self.title = '提示'
						# self.message = '预订失败...'
						# messagebox.showinfo(self.title, self.message)
						continue
			else:
				while self.driver.url == self.ticket_url:
					self.driver.find_by_text('查询').click()
					# self.title = '提示'
					# self.message = '开始尝试预订...'
					# messagebox.showinfo(self.title, self.message)
					try:
						for i in self.driver.find_by_text('预订'):
							i.click()
							sleep(1)
					except:
						# self.title = '提示'
						# self.message = '预订失败...'
						# messagebox.showinfo(self.title, self.message)
						continue
			self.title = '提示'
			self.message = '开始选择用户~~~'
			messagebox.showinfo(self.title, self.message)
			sleep(1)
			for p in self.passengers:
				self.driver.find_by_text(p).last.click()
				sleep(0.5)
				if p[-1] == ')':
					self.driver.find_by_id('dialog_xsertcj_ok').click()
			self.title = '提示'
			self.message = '提交订单中...'
			messagebox.showinfo(self.title, self.message)
			sleep(1)
			self.driver.find_by_id('submitOrder_id').click()
			sleep(2)
			self.title = '提示'
			self.message = '确认选座中...'
			messagebox.showinfo(self.title, self.message)
			self.driver.find_by_id('qr_submit_id').click()
			self.title = '提示'
			self.message = '预订成功...'
			messagebox.showinfo(self.title, self.message)
			self.content = '恭喜您抢票成功，请在半小时内完成支付！！！'
			_ = os.system('mshta vbscript:createobject("sapi.spvoice").speak("%s")(window.close)' % self.content)
		except:
			self.title = '提示'
			self.message = '出现了一点小错误,可能是输入信息有误导致的...'
			messagebox.showinfo(self.title, self.message)
#-------------------------------------------------------------------------------------------------------------------------------------------



# 界面部分
#-------------------------------------------------------------------------------------------------------------------------------------------
# 界面初始化
root = Tk()
root.title('火车票抢票系统V1.0')
root.resizable(False, False)
root.geometry('650x500+400+120')


# 设置背景图片
image_path = r'bg2_demo.png'
bg = Image.open(image_path)
bgimg = ImageTk.PhotoImage(bg)
lb_bgimg = Label(root, image=bgimg)
lb_bgimg.grid()


# 布局
# 查询功能
class Query_Thread(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(Query_Thread, self).__init__(*args, **kwargs)
		self.__running = threading.Event()
		self.__running.set()
	def run(self):
		while self.__running.isSet():
			global txt_show_ticket
			self.ticket_option = str(en_option_var.get()).replace(' ', '')
			self.from_station = str(en_starts_var.get()).replace(' ', '')
			self.to_station = str(en_ends_var.get()).replace(' ', '')
			self.date = str(en_date_var.get()).replace(' ', '')
			self.from_station = Station_Parse.parse_station().parse(self.from_station)
			self.to_station = Station_Parse.parse_station().parse(self.to_station)
			if not self.ticket_option:
				self.title = '提示'
				self.message = '请输入有效的类型'
				messagebox.showinfo(self.title, self.message)
				self.__running.clear()
				break
			if self.from_station is None or self.to_station is None:
				self.title = '提示'
				self.message = '请输入有效的车站名'
				messagebox.showinfo(self.title, self.message)
				self.__running.clear()
				break
			if self.date:
				if datetime.strptime(self.date, '%Y-%m-%d') < datetime.now():
					self.title = '提示'
					self.message = '请输入有效日期'
					messagebox.showinfo(self.title, self.message)
					self.__running.clear()
					break
			else:
				title = '提示'
				message = '请输入有效日期'
				messagebox.showinfo(title, message)
				self.__running.clear()
				break	
			Query_Ticket(txt_show_ticket, self.ticket_option, self.from_station, self.to_station, self.date).query()
			self.__running.clear()
# 查询回调函数
def bt_query_ticket():
	t_Query = Query_Thread()
	t_Query.start()
# 查询按钮
button_query = Button(root, text='查询', bd=5, width=10, height=2, command=bt_query_ticket, font=('楷体', 12), bg='skyblue')
button_query.place(relx=0.70, rely=0.12, anchor=CENTER)
# 抢票功能
class Buy_Thread(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(Buy_Thread, self).__init__(*args, **kwargs)
		self.__running = threading.Event()
		self.__running.set()
	def run(self):
		while self.__running.isSet():
			self.starts = str(en_starts_var.get()).replace(' ', '')
			self.ends = str(en_ends_var.get()).replace(' ', '')
			self.dtime = str(en_date_var.get()).replace(' ', '')
			self.passengers = str(en_passengers_var.get()).replace(' ', '')
			self.order = str(en_order_var.get()).replace(' ', '')
			self.username = str(en_user_var.get()).replace(' ', '')
			self.password = str(en_pwd_var.get()).replace(' ', '')
			if self.dtime:
				if datetime.strptime(self.dtime, '%Y-%m-%d') < datetime.now():
					self.title = '提示'
					self.message = '请输入有效日期'
					messagebox.showinfo(self.title, self.message)
					self.__running.clear()
					break
			else:
				title = '提示'
				message = '请输入有效日期'
				messagebox.showinfo(title, message)
				self.__running.clear()
				break
			if not self.username or not self.password:
				title = '提示'
				message = '请输入有效用户名和密码'
				messagebox.showinfo(title, message)
				self.__running.clear()
				break
			if not self.passengers:
				title = '提示'
				message = '请输入有效乘客名'
				messagebox.showinfo(title, message)
				self.__running.clear()
				break
			if not self.order:
				title = '提示'
				message = '请输入有效车次'
				messagebox.showinfo(title, message)
				self.__running.clear()
				break
			Buy_Tickets(self.username, self.password, self.order, self.passengers, self.dtime, self.starts, self.ends).start_buy()
			self.__running.clear()
# 抢票回调函数
def bt_buy_ticket():
	t_Buy = Buy_Thread()
	t_Buy.start()
# 抢票按钮
button_buy = Button(root, text='抢票', bd=5, width=10, height=2, command=bt_buy_ticket, font=('楷体', 12), bg='skyblue')
button_buy.place(relx=0.90, rely=0.12, anchor=CENTER)
# 查询显示框
txt_show_ticket = Text(root, bd=4, width=90, height=28, font=('楷体', 10))
txt_show_ticket.bind("<KeyPress>", lambda e : "break")
txt_show_ticket.place(relx=0.50, rely=0.60, anchor=CENTER)
# 输入框
# 乘客名
en_passengers_var = StringVar()
lb_passengers = Label(root, text='乘客名：', font=('楷体', 12))
lb_passengers.place(relx=0.10, rely=0.05, anchor=CENTER)
en_passengers = Entry(root, textvariable=en_passengers_var, width=10)
en_passengers.place(relx=0.10, rely=0.10, anchor=CENTER)
# 出发地
en_starts_var = StringVar()
lb_starts = Label(root, text='出发地：', font=('楷体', 12))
lb_starts.place(relx=0.22, rely=0.05, anchor=CENTER)
en_starts = Entry(root, textvariable=en_starts_var, width=10)
en_starts.place(relx=0.22, rely=0.10, anchor=CENTER)
# 目的地
en_ends_var = StringVar()
lb_ends = Label(root, text='目的地：', font=('楷体', 12))
lb_ends.place(relx=0.34, rely=0.05, anchor=CENTER)
en_ends = Entry(root, textvariable=en_ends_var, width=10)
en_ends.place(relx=0.34, rely=0.10, anchor=CENTER)
# 日期
en_date_var = StringVar()
lb_date = Label(root, text='日期：  ', font=('楷体', 12))
lb_date.place(relx=0.46, rely=0.05, anchor=CENTER)
en_date = Entry(root, textvariable=en_date_var, width=10)
en_date.place(relx=0.46, rely=0.10, anchor=CENTER)
# 类型(查询用)
en_option_var = StringVar()
lb_option = Label(root, text='类型(查询用)：', font=('楷体', 10))
lb_option.place(relx=0.12, rely=0.15, anchor=CENTER)
en_option = Entry(root, textvariable=en_option_var, width=10)
en_option.place(relx=0.26, rely=0.15, anchor=CENTER)
# 车次(抢票用)
en_order_var = StringVar()
lb_order = Label(root, text='车次(抢票用)：', font=('楷体', 10))
lb_order.place(relx=0.40, rely=0.15, anchor=CENTER)
en_order = Entry(root, textvariable=en_order_var, width=10)
en_order.place(relx=0.54, rely=0.15, anchor=CENTER)
# 用户名(抢票用)
en_user_var = StringVar()
lb_user = Label(root, text='用户名(抢票)：', font=('楷体', 10))
lb_user.place(relx=0.12, rely=0.20, anchor=CENTER)
en_user = Entry(root, textvariable=en_user_var, width=10)
en_user.place(relx=0.26, rely=0.20, anchor=CENTER)
# 密码(抢票用)
en_pwd_var = StringVar()
lb_pwd = Label(root, text='密码(抢票)：  ', font=('楷体', 10))
lb_pwd.place(relx=0.40, rely=0.20, anchor=CENTER)
en_pwd = Entry(root, textvariable=en_pwd_var, show='*', width=10)
en_pwd.place(relx=0.54, rely=0.20, anchor=CENTER)

root.mainloop()
#-------------------------------------------------------------------------------------------------------------------------------------------
