import urllib.request
import os
import re
import time
import json

def open_url(url):
    req = urllib.request.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299')
    response = urllib.request.urlopen(req)
    html = response.read()
    return html

def get_pages(url):
    html = open_url(url).decode('utf-8')
    p = r'(\d+) repository results'
    pages = re.findall(p, html)
    return pages

def get_repository(url):
    html = open_url(url).decode('utf-8')
    p = r',&quot;url&quot;:&quot;([^"]+)&quot;},'
    url_list = re.findall(p, html)
    return url_list

## 利用爬虫获取标签
'''def get_retopic(url):
    html = open_url(url).decode('utf-8')
    p = r'<div class="d-table-cell col-2 text-gray pt-2">(?:.|\n)(.*(?:.|\n).*(?:.|\n)  |[^"]+)</div>'
    re_topic = re.findall(p, html)
    for num in range(len(re_topic)):
        if len(re_topic[num]) > 5:
            re_topic[num] = re_topic[num].split('      ')[-1]
        if len(re_topic[num]) > 2:
            re_topic[num] = re_topic[num].split('\n')[0]
        if 'div' in re_topic[num]:
            re_topic[num] = '  '
    print(re_topic)
    return re_topic'''
## 利用API获取标签
def get_retopic(owner, name):
    data = {"query":
            'query {repository(owner:"%s", name:"%s") {repositoryTopics(last:20){nodes{topic {name}}}}}' % (owner, name)
            }

    headers = {'Authorization': 'token 8c12627af039588a6c63e9a735e8a145dd641fee'}
    req = urllib.request.Request(url='https://api.github.com/graphql', data=json.dumps(data).encode('utf-8'), headers=headers)
    resopnse = urllib.request.urlopen(req)
    html = resopnse.read().decode('utf-8')

    topics = json.loads(html)

    topic_list = []
    for topic in topics['data']['repository']['repositoryTopics']['nodes']:
        topic_list.append(topic['topic']['name'])

    return topic_list

def GetRe(folder = 'repository'):
    os.mkdir(folder)
    os.chdir(folder)

    new_topics = ['beginner-friendly', 'first-timers-only', 'first-timer-only']
    for new_topic in new_topics:
        filename = new_topic + '-url.json'
        url = 'https://github.com/search?p=1&q=' + new_topic + '&type=Repositories&utf8=%E2%9C%93'
        ## 获得项目页数
        pages = get_pages(url)
        if int(pages[0]) % 10 > 0:
            nums = int(pages[0]) // 10 + 1
        else:
            nums = int(pages[0]) // 10
        for num in range(1, nums + 1):
            try:
                url = 'https://github.com/search?p=' + str(num) + '&q=' + new_topic + '&type=Repositories&utf8=%E2%9C%93'
                re_url = get_repository(url)
                f = open(filename ,'a+')
                for i in range(len(re_url)):
                    ##从URL获得owner和name
                    owner = re_url[i].split('/')[-2]
                    name = re_url[i].split('/')[-1]
                    topic = get_retopic(owner, name)
                    json.dump('page: ' + str(num) +'  ' + str(re_url[i]) + '   topic:  ' + str(topic) + '  ', f)
            except urllib.error.HTTPError as e:
                print("已经无法访问了！")
            time.sleep(10)
        f.close()

if __name__ == '__main__':
    GetRe()