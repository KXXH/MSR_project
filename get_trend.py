# coding=UTF-8
'''
Version=1.2
date=2018-3-16
TODO:
- 在线测试
'''
from urllib import request
import re
import json
import threading
import sqlite3

class Project:
	def __init__(self, name, language = None, stars = None, forks = None, stars_today = None, contributors = None):
		self.__name = name
		self.__language = language
		self.__stars = stars
		self.__forks = forks
		self.__contributors = contributors
		self.__stars_today = stars_today

	def change_name(self, name = None):
		if name!=None:
			if type(name)==str:
				self.__name = name
			else:
				raise ValueError('Project name must be str, not %s' % type(name))
		return self.__name
	
	def change_language(self, language = None):
		if language!=None:
			if type(language)==str:
				self.__language = language
			else:
				raise ValueError('Language name must be str, not %s' % type(language))
		return self.__language
	
	def change_stars(self, stars = None):
		if stars!=None:
			if type(stars)==int:
				self.__stars = stars
			else:
				raise ValueError('Star number must be int, not %s' % type(stars))
		return self.__stars

	def change_forks(self, forks = None):
		if forks!=None:
			if type(forks)==int:
				self.__forks = forks
				pass
			else:
				raise ValueError('Fork number must be int, not %s' % type(forks))
		return self.__forks

	def change_stars_today(self, stars_today = None):
		if stars_today!=None:
			if type(stars_today)==int:
				self.__stars_today = stars_today
				pass
			else:
				raise ValueError('Stars_today number must be int, not %s' % type(stars_today))
		return self.__stars_today

	def change_contributors(self, contributors = None):
		if contributors!=None:
			if type(contributors)==list:
				self.__contributors = contributors
			else:
				raise ValueError('Contributors must be list, not %s' % type(contributors))
		return self.__contributors


def get_language_list():
	url = 'https://github.com/trending/'
	with request.urlopen(url) as trend_page:
		data = trend_page.read()
		bt = 'https://github.com/trending/[a-z0-9%-]+'
		urls = re.findall(bt,str(data))
		with open('Github_language_url_list.json', 'w') as f:
			json.dump(urls[10:],f)
	# print(urls[10:])
	urls = urls[10:]
	return urls

def get_project_list(project_url):
	# print(project_url)
	print('now opening :'+project_url)
	try:
		with request.urlopen(project_url) as project_page:
			data = project_page.read().decode('UTF-8')
			bt0 = r'<li class="col-12 d-block width-full py-4 border-bottom" id="[A-Za-z0-9-%/_]+">'
			bt1 = r'https://github.com/[A-Za-z0-9-%/:_]+|<a href="[A-Za-z0-9-%_/]+'
			# 正则表达式1，用于获取项目名称
			bt2 = r'</svg>\s*[0-9,]+'
			# 正则表达式2，用于获取star，fork，today
			bt3 = r'<img class="avatar mb-1" title="[a-zA-Z0-9]+'
			# 正则表达式3，用于获取contributors
			m = re.split(bt0, data, 25)[1:]
			# 划分每个项目的区域
			project_list = list()
			for item in m:
				language = project_url.split('https://github.com/trending/')[1]
				try:
					name = re.findall(bt1, item)[0]
					name = re.sub('<a href="', '', name)
				except IndexError:
					raise IndexError('list index out of range, HTML: %s' % item)
				nums = re.findall(bt2, item)
				if(len(nums)<3):
					# print('缺数字！' + str(len(nums)))
					if re.search('stargazers', item)==None:
						nums.insert(0, '0')
					if re.search('network', item)==None:
						nums.insert(1, '0')
					if re.search('stars today|star today', item)==None:
						nums.insert(2, '0')
				cons = re.findall(bt3, item)
				for i, num in enumerate(nums):
					nums[i] = str2num(re.sub(r'</svg>\s*', '', num))
				for i, con in enumerate(cons):
					cons[i] = re.sub(r'<img class="avatar mb-1" title="', '', con)
				t_project = Project(name, language, nums[0], nums[1], nums[2], cons)
				print('name: %s' % name)
				print('nums: %s' % nums)
				print('cons: %s' % cons)
				lock.acquire()
				try:
					conn1 = sqlite3.connect('hot_project_info.db')
					cursor1 = conn1.cursor()
					cursor1.execute('insert into hot_projects(name, language, stars, forks, stars_today, contributors) '\
						'values(?, ?, ?, ?, ?, ?)', (name, language, nums[0], nums[1], nums[2], list2str(cons)))
					cursor1.close()
					conn1.commit()
					conn1.close()
				finally:
					lock.release()
				project_list.append(t_project)
			# print(len(m))
			# print(data)
			for pro in project_list:
				print('%s %s %s %s %s %s' % (pro.change_name(), pro.change_language(), pro.change_stars(), 
					pro.change_forks(), pro.change_stars_today(), pro.change_contributors()))
			# print(re.search(bt1,data))
		# break
	except Exception as e:
		get_project_list(project_url)
		print(e)
	return project_list


def str2num(c):
	nums = c.split(',')
	s = 0
	for num in nums:
		s*=1000
		s+=int(num)
	return s

def list2str(l):
	s = ''
	if len(l)>1:
		for item in l:
			s = s + str(item) + '|'
	elif len(l)>0:
		s = str(l[0])
	return s

def test_language_page():
	filename='Trending 1C Enterprise repositories on GitHub today.html'
	with open(filename, 'r', encoding = 'UTF-8') as f:
		data = f.read()
		bt0 = r'<li class="col-12 d-block width-full py-4 border-bottom" id="[A-Za-z0-9-%/_]+">'
		# print(data)
		bt1 = r'https://github.com/[A-Za-z0-9-%/:_]+'
		bt2 = r'</svg>\s*[0-9,]+'
		bt3 = r'Built by'
		bt4 = r'<img class="avatar mb-1" title="[a-zA-Z0-9]+'
		m = re.split(bt0, data, 25)[1:]
		print(m[0])
		# print(m)
		for item in m:
			name = re.findall(bt1, item)[0].split('https://github.com/')[1]
			nums = re.findall(bt2, item)
			cons = re.findall(bt4, item)
			for i, num in enumerate(nums):
				nums[i] = str2num(re.sub(r'</svg>\s*', '', num))
			for i, con in enumerate(cons):
				cons[i] = re.sub(r'<img class="avatar mb-1" title="', '', con)
			print('names: %s' % name)
			print('nums: %s' % nums)
			print('cons: %s' % cons)
		# m = m[1:]
		# print(m)
'''
		cons = list()
		for i in m:
			t = list()
			c = re.findall(bt4, i)
			for ic in c:
				ic = re.sub(r'<img class="avatar mb-1" title="', '', ic)
				t.append(ic)
			cons.append(t)
			print(t)
'''
		# print(m)
		# project_list=list()
		# print(len(m))
'''
		b='<div class="d-inline-block col-9 mb-1">\n    <h3>\n      <a href="'
		for item in m:
			# item = item[len(b):-1]
			item = re.sub(r'<img class="avatar mb-1" title="','',item)
			print(item)
			project_list.append(item)
		print(project_list)
		print(len(project_list))
'''


if __name__ == '__main__':
	# urls = get_language_list()
	conn = sqlite3.connect('hot_project_info.db')
	cursor = conn.cursor()
	cursor.execute('create table if not exists hot_projects (_id integer primary key autoincrement, name text, language text, stars integer, forks integer, stars_today integer, contributors text)')
	cursor.close()
	conn.commit()
	conn.close()
	lock = threading.Lock()
	with open('Github_language_url_list.json', 'r') as f:
		data = f.read()
		urls = json.loads(data)
	for i in range(0, len(urls), 4):
		t1 = threading.Thread(target = get_project_list, args = (urls[i],))
		t2 = threading.Thread(target = get_project_list, args = (urls[i+1],))
		t3 = threading.Thread(target = get_project_list, args = (urls[i+2],))
		t4 = threading.Thread(target = get_project_list, args = (urls[i+3],))
		t1.start()
		t2.start()
		t3.start()
		t4.start()
		t1.join()
		t2.join()
		t3.join()
		t4.join()
		# get_project_list(project_url)
	# test_language_page()
f.__language = language
			else:
				raise ValueError('Language name must be str, not %s' % type(language))
		return self.__language
	
	def change_stars(self, stars = None):
		if stars!=None:
			if type(stars)==int:
				self.__stars = stars
			else:
				raise ValueError('Star number must be int, not %s' % type(stars))
		return self.__stars

	def change_forks(self, forks = None):
		if forks!=None:
			if type(forks)==int:
				self.__forks = forks
				pass
			else:
				raise ValueError('Fork number must be int, not %s' % type(forks))
		return self.__forks

	def change_stars_today(self, stars_today = None):
		if stars_today!=None:
			if type(stars_today)==int:
				self.__stars_today = stars_today
				pass
			else:
				raise ValueError('Stars_today number must be int, not %s' % type(stars_today))
		return self.__stars_today

	def change_contributors(self, contributors = None):
		if contributors!=None:
			if type(contributors)==list:
				self.__contributors = contributors
			else:
				raise ValueError('Contributors must be list, not %s' % type(contributors))
		return self.__contributors


def get_language_list():
	url = 'https://github.com/trending/'
	with request.urlopen(url) as trend_page:
		data = trend_page.read()
		bt = 'https://github.com/trending/[a-z0-9%-]+'
		urls = re.findall(bt,str(data))
		with open('Github_language_url_list.json', 'w') as f:
			json.dump(urls[10:],f)
	# print(urls[10:])
	urls = urls[10:]
	return urls

def get_project_list(project_url):
	# print(project_url)
	print('now opening :'+project_url)
	try:
		with request.urlopen(project_url) as project_page:
			data = project_page.read().decode('UTF-8')
			bt0 = r'<li class="col-12 d-block width-full py-4 border-bottom" id="[A-Za-z0-9-%/_]+">'
			bt1 = r'https://github.com/[A-Za-z0-9-%/:_]+|<a href="[A-Za-z0-9-%_/]+'
			# 正则表达式1，用于获取项目名称
			bt2 = r'</svg>\s*[0-9,]+'
			# 正则表达式2，用于获取star，fork，today
			bt3 = r'<img class="avatar mb-1" title="[a-zA-Z0-9]+'
			# 正则表达式3，用于获取contributors
			m = re.split(bt0, data, 25)[1:]
			# 划分每个项目的区域
			project_list = list()
			for item in m:
				language = project_url.split('https://github.com/trending/')[1]
				try:
					name = re.findall(bt1, item)[0]
					name = re.sub('<a href="', '', name)
				except IndexError:
					raise IndexError('list index out of range, HTML: %s' % item)
				nums = re.findall(bt2, item)
				if(len(nums)<3):
					# print('缺数字！' + str(len(nums)))
					if re.search('stargazers', item)==None:
						nums.insert(0, '0')
					if re.search('network', item)==None:
						nums.insert(1, '0')
					if re.search('stars today|star today', item)==None:
						nums.insert(2, '0')
				cons = re.findall(bt3, item)
				for i, num in enumerate(nums):
					nums[i] = str2num(re.sub(r'</svg>\s*', '', num))
				for i, con in enumerate(cons):
					cons[i] = re.sub(r'<img class="avatar mb-1" title="', '', con)
				t_project = Project(name, language, nums[0], nums[1], nums[2], cons)
				print('name: %s' % name)
				print('nums: %s' % nums)
				print('cons: %s' % cons)
				lock.acquire()
				try:
					conn1 = sqlite3.connect('hot_project_info.db')
					cursor1 = conn1.cursor()
					cursor1.execute('insert into hot_projects(name, language, stars, forks, stars_today, contributors) '\
						'values(?, ?, ?, ?, ?, ?)', (name, language, nums[0], nums[1], nums[2], list2str(cons)))
					cursor1.close()
					conn1.commit()
					conn1.close()
				finally:
					lock.release()
				project_list.append(t_project)
			# print(len(m))
			# print(data)
			for pro in project_list:
				print('%s %s %s %s %s %s' % (pro.change_name(), pro.change_language(), pro.change_stars(), 
					pro.change_forks(), pro.change_stars_today(), pro.change_contributors()))
			# print(re.search(bt1,data))
		# break
	except Exception as e:
		# get_project_list(project_url)
		print(e)
	return project_list


def str2num(c):
	nums = c.split(',')
	s = 0
	for num in nums:
		s*=1000
		s+=int(num)
	return s

def list2str(l):
	s = ''
	if len(l)>1:
		for item in l:
			s = s + str(item) + '|'
	elif len(l)>0:
		s = str(l[0])
	return s

def test_language_page():
	filename='Trending 1C Enterprise repositories on GitHub today.html'
	with open(filename, 'r', encoding = 'UTF-8') as f:
		data = f.read()
		bt0 = r'<li class="col-12 d-block width-full py-4 border-bottom" id="[A-Za-z0-9-%/_]+">'
		# print(data)
		bt1 = r'https://github.com/[A-Za-z0-9-%/:_]+'
		bt2 = r'</svg>\s*[0-9,]+'
		bt3 = r'Built by'
		bt4 = r'<img class="avatar mb-1" title="[a-zA-Z0-9]+'
		m = re.split(bt0, data, 25)[1:]
		print(m[0])
		# print(m)
		for item in m:
			name = re.findall(bt1, item)[0].split('https://github.com/')[1]
			nums = re.findall(bt2, item)
			cons = re.findall(bt4, item)
			for i, num in enumerate(nums):
				nums[i] = str2num(re.sub(r'</svg>\s*', '', num))
			for i, con in enumerate(cons):
				cons[i] = re.sub(r'<img class="avatar mb-1" title="', '', con)
			print('names: %s' % name)
			print('nums: %s' % nums)
			print('cons: %s' % cons)
		# m = m[1:]
		# print(m)
'''
		cons = list()
		for i in m:
			t = list()
			c = re.findall(bt4, i)
			for ic in c:
				ic = re.sub(r'<img class="avatar mb-1" title="', '', ic)
				t.append(ic)
			cons.append(t)
			print(t)
'''
		# print(m)
		# project_list=list()
		# print(len(m))
'''
		b='<div class="d-inline-block col-9 mb-1">\n    <h3>\n      <a href="'
		for item in m:
			# item = item[len(b):-1]
			item = re.sub(r'<img class="avatar mb-1" title="','',item)
			print(item)
			project_list.append(item)
		print(project_list)
		print(len(project_list))
'''


if __name__ == '__main__':
	# urls = get_language_list()
	conn = sqlite3.connect('hot_project_info.db')
	cursor = conn.cursor()
	cursor.execute('create table if not exists hot_projects (_id integer primary key autoincrement, name text, language text, stars integer, forks integer, stars_today integer, contributors text)')
	cursor.close()
	conn.commit()
	conn.close()
	lock = threading.Lock()
	with open('Github_language_url_list.json', 'r') as f:
		data = f.read()
		urls = json.loads(data)
	for i in range(0, len(urls), 4):
		t1 = threading.Thread(target = get_project_list, args = (urls[i],))
		t2 = threading.Thread(target = get_project_list, args = (urls[i+1],))
		t3 = threading.Thread(target = get_project_list, args = (urls[i+2],))
		t4 = threading.Thread(target = get_project_list, args = (urls[i+3],))
		t1.start()
		t2.start()
		t3.start()
		t4.start()
		t1.join()
		t2.join()
		t3.join()
		t4.join()
		# get_project_list(project_url)
	# test_language_page()
