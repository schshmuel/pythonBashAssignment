import os
import sys

from github import Github, Repository
import psycopg2


def connect_postgresql_db(db_host: str, db_name: str, db_user: str, db_password: str):
    conn = psycopg2.connect(host=db_host,
                            database=db_name,
                            user=db_user,
                            password=db_password)
    return (conn, conn.cursor())


def close_db_connection(conn, curse):
    conn.close()
    curse.close()


def find_primary_language(repo: Repository) -> str:
    languages = repo.get_languages()
    if not languages:
        return 'NULL'
    else:
        v = list(languages.values())
        k = list(languages.keys())
        return k[v.index(max(v))]


def find_repositories(access_token: str):
    g = Github(access_token)
    # Notice, there is one to one connection between repo with org:kubernetes and user:kubernetes
    return g.search_repositories(query='user:kubernetes', sort='stars', order='desc')


def insert_to_db(conn, curse, table: str, insert_values: list):
    sql = f"INSERT INTO {table} VALUES(%s,%s,%s)"
    curse.executemany(sql, insert_values)
    print(f"Writing to values {insert_values} to table {table}")
    sys.stdout.flush()
    conn.commit()


def loop_over_repos(repositories) -> list:
    insert_values = []
    for repo in repositories:
        primary_language = find_primary_language(repo)
        print(f"{repo.full_name} has {repo.stargazers_count} stargazers and primary_language is {primary_language}")
        sys.stdout.flush()
        insert_values.append((repo.full_name, str(repo.stargazers_count), primary_language))
    return insert_values


if __name__ == '__main__':
    access_token = os.getenv('GITHUB_ACCESS_TOKEN')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    repositories = find_repositories(access_token)
    insert_values = loop_over_repos(repositories)
    conn, curse = connect_postgresql_db(db_host, db_name, db_user, db_password)
    table = "github"
    insert_to_db(conn, curse, table, insert_values)
    close_db_connection(conn, curse)
