import os
import sys

from github import Github, Repository


def find_primary_languages(repo: Repository) -> str:
    languages = repo.get_languages()
    print(languages)
    if not languages:
        return None
    else:
        v = list(languages.values())
        k = list(languages.keys())
        return k[v.index(max(v))]


def main(access_token: str):
    g = Github(access_token)
    # Notice, there is one to one connection between repo with org:kubernetes and user:kubernetes
    repositories = g.search_repositories(query='user:kubernetes', sort='stars', order='desc')
    for repo in repositories:
        main_language = find_primary_languages(repo)
        print(f"{repo.full_name}:{repo.stargazers_count}:{main_language}")
        sys.stdout.flush()


if __name__ == '__main__':
    access_token = os.getenv('GITHUB_ACCESS_TOKEN')
    print(access_token)
    main(access_token)
