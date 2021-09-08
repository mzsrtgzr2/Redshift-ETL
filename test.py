import configparser
import psycopg2
from sql_queries import select_table_queries


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    for query in select_table_queries:
        print('running', query)
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            print (row)

    conn.close()


if __name__ == "__main__":
    main()