
class User:
    def __init__(self, contributedRepositories=None, followers=None, following=None, issues=None,
                 organizations=None, pullRequests=None, repositories=None, starredRepositories=None, watching=None):
        self.__contributedRepositories = contributedRepositories
        self.__followers = followers
        self.__following = following
        self.__issues = issues
        self.__organizations = organizations
        self.__pullRequests = pullRequests
        self.__repositories = repositories
        self.__starredRepositories = starredRepositories
        self.__watching = watching

    def set_contributedRepositories(self, contributedRepositories=None):
        if contributedRepositories != None:
            if type(contributedRepositories) == str:
                self.__contributedRepositories = contributedRepositories
            else:
                raise ValueError('Project contributedRepositories must be str, not %s' % type(contributedRepositories))
        return self.__contributedRepositories

    def set_followers(self, followers=None):
        if followers != None:
            if type(followers) == str:
                self.__followers = followers
            else:
                raise ValueError('Project followers must be str, not %s' % type(followers))
        return self.__followers

    def set_following(self, following=None):
        if following != None:
            if type(following) == str:
                self.__following = following
            else:
                raise ValueError('Project following must be str, not %s' % type(following))
        return self.__following

    def set_issues(self, issues=None):
        if issues != None:
            if type(issues) == str:
                self.__issues = issues
            else:
                raise ValueError('Project issues must be str, not %s' % type(issues))
        return self.__issues

    def set_organizations(self, organizations=None):
        if organizations != None:
            if type(organizations) == str:
                self.__organizations = organizations
            else:
                raise ValueError('Project organizations must be str, not %s' % type(organizations))
        return self.__organizations

    def set_pullRequests(self, pullRequests=None):
        if pullRequests != None:
            if type(pullRequests) == str:
                self.__pullRequests = pullRequests
            else:
                raise ValueError('Project pullRequests must be str, not %s' % type(pullRequests))
        return self.__pullRequests

    def set_repositories(self, repositories=None):
        if repositories != None:
            if type(repositories) == str:
                self.__repositories = repositories
            else:
                raise ValueError('Project repositories must be str, not %s' % type(repositories))
        return self.__repositories

    def set_starredRepositories(self, starredRepositories=None):
        if starredRepositories != None:
            if type(starredRepositories) == str:
                self.__starredRepositories = starredRepositories
            else:
                raise ValueError('Project starredRepositories must be str, not %s' % type(starredRepositories))
        return self.__starredRepositories

    def set_watching(self, watching=None):
        if watching != None:
            if type(watching) == str:
                self.__watching = watching
            else:
                raise ValueError('Project watching must be str, not %s' % type(watching))
        return self.__watching