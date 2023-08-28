import configparser
import psycopg2
from sql.sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Function that executes COPY command queries to load data from S3 to the staging tables.
    
    Args:
        cur (psycopg2.extensions.cursor): The cursor object for executing queries.
        conn (psycopg2.extensions.connection): The database connection object.
    
    Returns:
        None
    """
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    """
    Function that executes INSERT queries to populate database tables.
    
    Args:
        cur (psycopg2.extensions.cursor): The cursor object for executing queries.
        conn (psycopg2.extensions.connection): The database connection object.
    
    Returns:
        None
    """
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
