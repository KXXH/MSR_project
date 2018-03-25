from urllib import request
import json
from ClassUser import User
import addinfo
import re
import get_new_url
import os


def get_user_info(username):
    data = {"query":
          'query {user(login:"%s"){contributedRepositories(last:100){edges{node{name url}}}followers(last:20){edges{node{login' % username
        + '}}}following(last:20){edges{node{login}}}issues(last:20){edges{node{labels(first:5){nodes{name}}'
        + '}}}organizations(last:20){edges{node{name}}}pullRequests(last:20){edges{node{title'
        + '}}}repositories(last:20){edges{node{name url}}}starredRepositories(last:20){edges{node{name}}}'
        + 'watching(last:20){edges{node{name}}}}}'
            }
    headers = {'Authorization': 'token 8c12627af039588a6c63e9a735e8a145dd641fee'}

    req = request.Request(url='https://api.github.com/graphql', data=json.dumps(data).encode('utf-8'),headers=headers)
    resopnse = request.urlopen(req)
    infomation = resopnse.read().decode('utf-8')

    info = json.loads(infomation)

    addinfo.append_contributedRepositories(info, addinfo.contributedRepositories_list)
    addinfo.append_contributedRepositories_url(info, addinfo.contributedRepositories_url_list)
    addinfo.append_followers(info, addinfo.followers_list)
    addinfo.append_following(info, addinfo.following_list)
    addinfo.append_issues(info, addinfo.issues_list)
    addinfo.append_organizations(info, addinfo.organizations_list)
    addinfo.append_pullRequests(info, addinfo.pullRequests_list)
    addinfo.append_repositories(info, addinfo.repositories_list)
    addinfo.append_repositories_url(info, addinfo.repositories_url_list)
    addinfo.append_starredRepositories(info, addinfo.starredRepositories_list)
    addinfo.append_watching(info, addinfo.watching_list)

    user_info = User(addinfo.contributedRepositories_list,addinfo.contributedRepositories_url_list,addinfo.followers_list,addinfo.following_list,addinfo.issues_list,addinfo.organizations_list,
                    addinfo.pullRequests_list,addinfo.repositories_list,addinfo.repositories_url_list,addinfo.starredRepositories_list,addinfo.watching_list)

    '''print('%s %s %s %s %s %s %s %s %s' % (user_info.set_contributedRepositories(), user_info.set_contributedRepositories_url(), user_info.set_followers(), user_info.set_following(),
                                          user_info.set_issues(), user_info.set_organizations(), user_info.set_pullRequests(),
                                          user_info.set_repositories(),user_info.ser_repositories_url(),user_info.set_starredRepositories(),user_info.set_watching()))
    '''
    filename = username

    with open(filename + '.json','w') as f:
        f.write(str(user_info.set_contributedRepositories())+str(user_info.set_contributedRepositories_url())+str(user_info.set_followers())+str(user_info.set_following())+
                str(user_info.set_issues())+str(user_info.set_organizations())+str(user_info.set_pullRequests())+
                str(user_info.set_repositories())+str(user_info.set_repositories_url())+str(user_info.set_starredRepositories())+str(user_info.set_watching()))
    following_username = addinfo.following_list
    return following_username

def Set_username():
    print('请输入你的userlogin：')
    username = str(input())
    print('请输入你的语言标签： ')
    language_topic = str(input())
    mf_username = get_user_info(username)
    with open('following_username.txt','w') as f:
        f.write(str(mf_username))
    with open('following_username.txt','r') as f:
        p = r"'(.*?)'"
        my_following_username = re.findall(p , f.read())
    addinfo.del_info()
    os.mkdir('following_info')
    os.chdir('following_info')
    for fname in my_following_username:
        #print('Your followings ' + fname + ' have repositories: ')
        get_user_info(fname)
        with open(fname + '.json', 'r') as f:
            contributedRepositories = (f.read().split(']'))[0][1:]
            #print(contributedRepositories)
        with open(fname + '.json', 'r') as f:
            contributedRepositories_urls = ((f.read().split(']'))[1][1:]).split(', ')
        os.mkdir(fname+'_topic')
        os.chdir(fname+'_topic')
        for contributedRepositories_url in contributedRepositories_urls:
            owner = contributedRepositories_url.split('/')[3]
            name = contributedRepositories_url.split('/')[4][:-1]
            topic = get_new_url.get_retopic(owner, name)
            topic_filename = str(name) + '.json'
            with open(topic_filename,'w') as f:
                f.write(str(name) + ': ' + str(topic))
            #print(name + ' has topic: ' + str(topic))
            topic.clear()
        os.chdir('D:/MSR/MSR_project/scripts/user/following_info')
        addinfo.del_info()

    for fname in my_following_username:
        with open(fname + '.json') as f:
            contributedRepositories = (f.read().split(']'))[0][1:]
        p = r"'(.*?)'"
        contributedRepositories_list = re.findall(p , contributedRepositories)
        #print(contributedRepositories_list)
        os.chdir(fname + '_topic')
        for contributedRepository in contributedRepositories_list:
            with open(contributedRepository + '.json') as f:
                p = r"'(.*?)'"
                topic_list = re.findall(p, f.read())
                if language_topic in topic_list:
                    print('根据你的语言标签，我们从你的following列表中选出了：')
                    print(fname +"’s "+ contributedRepository)
        os.chdir('D:/MSR/MSR_project/scripts/user/following_info')




if __name__ == '__main__':
    Set_username()