import os
import sys

from github import Github, Repository


def calculate_repo_language(repo: Repository) -> str:
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            print(file_content)


def main(access_token: str):
    g = Github(access_token)
    # Notice, there is one to one connection between repo with org:kubernetes and user:kubernetes
    repositories = g.search_repositories(query='user:kubernetes', sort='stars', order='desc')
    for repo in repositories:
        print(f"{repo.full_name}:{repo.stargazers_count}:{repo.organization}")
        sys.stdout.flush()
        main_language = calculate_repo_language(repo)


if __name__ == '__main__':
    access_token = os.getenv('GITHUB_ACCESS_TOKEN')
    print(access_token)
    main(access_token)
