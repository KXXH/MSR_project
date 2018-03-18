# coding=UTF-8
# Version=1.0
# TODO:整合入get_trend.py
from urllib import request
import json
data = {
	"query":'query {repository(name:"PyGithub" owner:"PyGithub"){repositoryTopics(last:20){nodes{topic {name}}}}}'
}
headers = {'Authorization': 'token 76acc3f4a484314266f7578e767d0e50e37b0118'}
req = request.Request(url = 'https://api.github.com/graphql', data = json.dumps(data).encode('UTF-8'), headers = headers)
print(type(json.dumps(data)).encode('UTF-8'))
resopnse = request.urlopen(req)
ans = resopnse.read().decode('UTF-8')
d = json.loads(ans)
for item in d['data']['repository']['repositoryTopics']['nodes']:
	print(item['topic']['name'])