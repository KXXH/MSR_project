# coding=UTF-8


from urllib import request
import re
import json

def get_language_list():
	url = 'https://github.com/trending/'
	with request.urlopen(url) as trend_page:
		data = trend_page.read()
		bt = 'https://github.com/trending/[a-z0-9%-]+'
		m = re.findall(bt,str(data))
		print(m[10:])
		with open('Github_language_url_list.json', 'w') as f:
			json.dump(m[10:],f)

if __name__ == '__main__':
	get_language_list()

