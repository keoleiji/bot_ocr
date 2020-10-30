import psycopg2
import os
from os import environ

DATABASE_URL = environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cursor = conn.cursor()

def insert_db(sn,ti,d):
    try:        
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

def read_db(id):
    try:
        postgres_select_query = """ SELECT * FROM ANSWER """

        cursor.execute(postgres_select_query)
        print("Selecting rows from answer table using cursor.fetchall")
        mobile_records = cursor.fetchall() 
        
        print("return if tweet already was replied")
        for row in mobile_records:
            if str(id) in row:
                return True
    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching data from PostgreSQL", error)
    finally:
        #closing database connection.
        if(conn):
            cursor.close()
            conn.close()
            print("PostgreSQL connection is closed")