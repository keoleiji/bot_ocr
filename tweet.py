import tweepy
import time
import requests
import json
import sched
import os
import csv
import sys
import psycopg2
import database
from database import insert_db, read_db
#from keys import keys
from datetime import datetime
from os import environ

def bot():
    CONSUMER_KEY = environ['CONSUMER_KEY']
    CONSUMER_SECRET = environ['CONSUMER_SECRET']
    ACCESS_TOKEN = environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = environ['ACCESS_TOKEN_SECRET']
    ANSWER_FILE_NAME = 'answer.csv'
    OCR_KEY = environ['OCR_KEY']
    OCR_KEY_2 = environ['OCR_KEY_2']

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    if not os.path.isfile(ANSWER_FILE_NAME):
        write_file = open(ANSWER_FILE_NAME, 'w', newline="")
        write_answer = csv.writer(write_file)
        write_answer.writerow(['Screen_Name', 'Tweet_Id', 'Answer_Date'])
        write_file.close()

    # Instanciando atividades concluídas
    read_file = open(ANSWER_FILE_NAME, 'rt')
    read_answer = csv.reader(read_file)
    answer_data = list(read_answer)
    read_file.close()

    search = '@ConvertToText'
    numero_de_tweets = 250

    for tweet in tweepy.Cursor(api.search, search, include_entities=True).items(numero_de_tweets):
        for row in read_db(tweet.id):
            found = False
            if str(tweet.id) in row:
                found = True
                print('found', tweet.id)
                break
        #if found == False:
        if found == False:
            try:
                print('not found', tweet.id)
                if 'media' in tweet.entities:
                    for image in tweet.entities['media']:
                        image_url = image['media_url']
                        req = requests.get('https://api.ocr.space/parse/imageurl?apikey='+OCR_KEY+'&url='+image_url)
                        res = json.loads(req.text)
                        reply_text = res['ParsedResults'][0]['ParsedText']
                        print('texto:', tweet.text, '\nid:', tweet.id)
                        try:
                            api.update_status(status = '@'+tweet.user.screen_name + '\n' + reply_text, in_reply_to_status_id = tweet.id, auto_populate_reply_metadata=True)                            
                            insert_db(tweet.user.screen_name, tweet.id, datetime.now())
                            #write_file = open(ANSWER_FILE_NAME, 'a', newline="")
                            #write_answer = csv.writer(write_file)
                            #write_answer.writerow([tweet.user.screen_name, tweet.id, datetime.now()])
                            #write_file.close()
                            time.sleep(25)                                
                        except tweepy.TweepError as e:
                            print(e.reason)
            except tweepy.TweepError as e:
                print(e.reason)
            except StopIteration:
                break

while True:
    bot()
