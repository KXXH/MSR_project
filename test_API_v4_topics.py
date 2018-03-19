# coding=UTF-8
# Version=1.0
# TODO:整合入get_trend.py
from urllib import request
import json
data = {
	"query":'query {repository(name:"PyGithub" owner:"PyGithub"){repositoryTopics(last:20){nodes{topic {name}}}}}'
}
headers = {'Authorization': 'token 0db8e6ec963b57f43b01cbef8c1359c4a844eaa0'}
req = request.Request(url = 'https://api.github.com/graphql', data = json.dumps(data).encode('UTF-8'), headers = headers)
print(type(json.dumps(data)).encode('UTF-8'))
resopnse = request.urlopen(req)
ans = resopnse.read().decode('UTF-8')
d = json.loads(ans)
for item in d['data']['repository']['repositoryTopics']['nodes']:
	print(item['topic']['name'])