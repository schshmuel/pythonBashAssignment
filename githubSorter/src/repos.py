import sys

from github import Github, Repository


def loop_over_repos(repositories) -> list:
    insert_values = []
    for repo in repositories:
        primary_language = find_primary_language(repo)
        print(f"{repo.full_name} has {repo.stargazers_count} stargazers and primary_language is {primary_language}")
        sys.stdout.flush()
        insert_values.append((repo.full_name, str(repo.stargazers_count), primary_language))
    return insert_values


def find_repositories(access_token: str) -> list:
    g = Github(access_token)
    # Notice, there is one to one connection between repo with org:kubernetes and user:kubernetes
    return g.search_repositories(query='user:kubernetes', sort='stars', order='desc')


def find_primary_language(repo: Repository) -> str:
    languages = repo.get_languages()
    if not languages:
        return 'NULL'
    else:
        v = list(languages.values())
        k = list(languages.keys())
        return k[v.index(max(v))]
