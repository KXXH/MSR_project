from urllib import request
import json
from ClassUser import User
import addinfo


def get_user_info(username):
    data = {"query":
          'query {user(login:"%s"){contributedRepositories(last:20){edges{node{name}}}followers(last:20){edges{node{name' % username
        + '}}}following(last:20){edges{node{name}}}issues(last:20){edges{node{labels(first:5){nodes{name}}'
        + '}}}organizations(last:20){edges{node{name}}}pullRequests(last:20){edges{node{title'
        + '}}}repositories(last:20){edges{node{name}}}starredRepositories(last:20){edges{node{name}}}'
        + 'watching(last:20){edges{node{name}}}}}'
            }

    headers = {'Authorization': 'token 0336fec6883af02572eed01e022b86b388c4bf3e'}

    req = request.Request(url='https://api.github.com/graphql', data=json.dumps(data).encode('utf-8'),headers=headers)
    resopnse = request.urlopen(req)
    infomation = resopnse.read().decode('utf-8')

    info = json.loads(infomation)

    addinfo.append_contributedRepositories(info, addinfo.contributedRepositories_list)
    addinfo.append_followers(info, addinfo.followers_list)
    addinfo.append_following(info, addinfo.following_list)
    addinfo.append_issues(info, addinfo.issues_list)
    addinfo.append_organizations(info, addinfo.organizations_list)
    addinfo.append_pullRequests(info, addinfo.pullRequests_list)
    addinfo.append_repositories(info, addinfo.repositories_list)
    addinfo.append_starredRepositories(info, addinfo.starredRepositories_list)
    addinfo.append_watching(info, addinfo.watching_list)

    user_info = User(addinfo.contributedRepositories_list,addinfo.followers_list,addinfo.following_list,addinfo.issues_list,addinfo.organizations_list,
                    addinfo.pullRequests_list,addinfo.repositories_list,addinfo.starredRepositories_list,addinfo.watching_list)

    print('%s %s %s %s %s %s %s %s %s' % (user_info.set_contributedRepositories(), user_info.set_followers(), user_info.set_following(),
                                          user_info.set_issues(), user_info.set_organizations(), user_info.set_pullRequests(),
                                          user_info.set_repositories(),user_info.set_starredRepositories(),user_info.set_watching()))



def Set_username():
    username = str(input())
    get_user_info(username)

if __name__ == '__main__':
    Set_username()