import os

from . import db
from . import repos


def load_env_variables() -> tuple:
    access_token = os.getenv('GITHUB_ACCESS_TOKEN')
    db_host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    return access_token, db_host, db_name, db_user, db_password


if __name__ == '__main__':
    (access_token, db_host, db_name, db_user, db_password) = load_env_variables()
    repositories = repos.find_repositories(access_token)
    insert_values = repos.loop_over_repos(repositories)
    conn, curse = db.connect(db_host, db_name, db_user, db_password)
    table = "github"
    db.insert(conn, curse, table, insert_values)
    db.close_connection(conn, curse)
