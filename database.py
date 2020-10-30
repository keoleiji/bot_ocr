import psycopg2
import os
from os import environ

def db(sn,ti,d):

    try:
        DATABASE_URL = environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        postgres_insert_query = """ INSERT INTO answer (screen_name, tweet_id, data) VALUES (%s,%s,%s)"""
        records_to_insert = (sn, ti, d)
        cursor.execute(postgres_insert_query, records_to_insert)
        conn.commit()
        count = cursor.rowcount
        print(count, "Record inserted successfully into mobile table")
    except (Exception, psycopg2.Error) as error :
        if(conn):
            print("Failed to insert record into mobile table", error)

    finally:
        #closing database connection.
        if(conn):
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")