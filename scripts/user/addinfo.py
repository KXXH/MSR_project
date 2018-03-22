contributedRepositories_list = []
followers_list = []
following_list = []
issues_list = []
organizations_list = []
pullRequests_list = []
repositories_list = []
starredRepositories_list = []
watching_list = []

def append_contributedRepositories(info, list):
    for i in info['data']['user']['contributedRepositories']['edges']:
        list.append(i['node']['name'])
    return list

def append_followers(info, list):
    for i in info['data']['user']['followers']['edges']:
        list.append(i['node']['name'])
    return list

def append_following(info, list):
    for i in info['data']['user']['following']['edges']:
        list.append(i['node']['name'])
    return list

def append_issues(info, list):
    for i in info['data']['user']['issues']['edges']:
        for j in i['node']['labels']['nodes']:
            list.append(j['name'])
    return list

def append_organizations(info, list):
    for i in info['data']['user']['organizations']['edges']:
        list.append(i['node']['name'])
    return list

def append_pullRequests(info, list):
    for i in info['data']['user']['pullRequests']['edges']:
        list.append(i['node']['title'])
    return list

def append_repositories(info, list):
    for i in info['data']['user']['repositories']['edges']:
        list.append(i['node']['name'])
    return list

def append_starredRepositories(info, list):
    for i in info['data']['user']['starredRepositories']['edges']:
        list.append(i['node']['name'])
    return list

def append_watching(info, list):
    for i in info['data']['user']['watching']['edges']:
        list.append(i['node']['name'])
    return list