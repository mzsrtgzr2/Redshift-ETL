import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    cur.execute('select * from stl_load_errors')
    rows = cur.fetchall()
    for row in rows:
        print (row)

    conn.close()


if __name__ == "__main__":
    main()