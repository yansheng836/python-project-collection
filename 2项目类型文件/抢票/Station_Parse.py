import re
import requests

class parse_station():
	def __init__(self):
		pass
	def parse(self, station_opt):
		self.url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9042'
		self.res = requests.get(self.url, verify=False)
		self.pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
		self.stations = dict(re.findall(self.pattern, self.res.text))
		try:
			return self.stations[station_opt]
		except:
			return None
	def disparse(self, station_opt):
		self.url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9042'
		self.res = requests.get(self.url, verify=False)
		self.pattern = u'([\u4e00-\u9fa5]+)\|([A-Z]+)'
		self.stations = dict(re.findall(self.pattern, self.res.text))
		try:
			return list(self.stations.keys())[list(self.stations.values()).index(station_opt)]
		except:
			return None