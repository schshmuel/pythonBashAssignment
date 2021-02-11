import sys

import psycopg2


def connect(db_host: str, db_name: str, db_user: str, db_password: str):
    conn = psycopg2.connect(host=db_host,
                            database=db_name,
                            user=db_user,
                            password=db_password)
    return conn, conn.cursor()


def close_connection(conn, curse):
    conn.close()
    curse.close()


def insert(conn, curse, table: str, insert_values: list):
    sql = f"INSERT INTO {table} VALUES(%s,%s,%s)"
    curse.executemany(sql, insert_values)
    print(f"Writing to values {insert_values} to table {table}")
    sys.stdout.flush()
    conn.commit()
