import configparser
import psycopg2
from sql.tables import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Function to drop all tables in the database in order to create all the tables
    properly.
    
    Args:
        cur (psycopg2.extensions.cursor): The cursor object for executing queries.
        conn (psycopg2.extensions.connection): The database connection object.
    
    Returns:
        None
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Function to create the database tables.
    
    Args:
        cur (psycopg2.extensions.cursor): The cursor object for executing queries.
        conn (psycopg2.extensions.connection): The database connection object.
    
    Returns:
        None
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
