# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 17:21:46 2019

@author: Parth
"""
import time
import threading
import urllib
import re
import io
import active
import re
import sys
from time import sleep
import pickle
import os
from math import ceil
from pathlib import Path
import pandas as pd
import concurrent.futures 
import psycopg2
import GetOldTweets3 as got
import tweepy
start_time = time.time()
consumer_key='rNrnFupaEqKt0eb7hjbdHKdWg'
consumer_secret= 'DTTMoQOrCBmngaXmOnFhrBjdjwtT54x0AbGvNwwuqyYNWwEvc7'
access_token='1002268050513575936-gGrQUmDiMyCxO2Y88lc3ojqNzbtLGm'
access_token_secret='G572YTe2S5TQTTaXhFvl1WyNopa8ilrkgWSlCXBZQwU4C'
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

working_mumbai= "(buying mumbai flat) OR (buying mumbai property) OR (buying mumbai real estate) OR (purchasing mumbai flat) OR (purchasing mumbai property) OR (purchasing real estate mumbai) OR (buy mumbai flat) OR (buy mumbai property) OR (buy mumbai real estate) OR (purchase mumbai flat) OR (purchase mumbai property) OR (purchase real estate mumbai) -sale"

apartment= "(looking mumbai apartment) OR (searching mumbai apartment) OR (buying mumbai apartment) OR (purchasing mumbai apartment) OR (buy mumbai apartment) OR (purchase mumbai apartment) OR (look mumbai apartment) OR (search mumbai apartment) -sale"
#n
query3= "(buying mumbai house) OR (buying mumbai flat) OR (buying mumbai property) OR (buying mumbai real estate) OR (purchasing mumbai house) OR (purchasing mumbai flat) OR (purchasing mumbai property) OR (purchasing real estate mumbai) OR (buy mumbai house) OR (buy mumbai flat) OR (buy mumbai property) OR (buy mumbai real estate) OR (purchase mumbai house) OR (purchase mumbai flat) OR (purchase mumbai property) OR (purchase real estate mumbai) -sale"

query2=" (buying mumbai home) OR (buying mumbai house) OR (buying mumbai flat) OR (buying mumbai property) OR (buying mumbai real estate) OR (purchasing mumbai home) OR (purchasing mumbai house) OR (purchasing mumbai flat) OR (purchasing mumbai property) OR (purchasing real estate mumbai) OR (buy mumbai home) OR (buy mumbai house) OR (buy mumbai flat) OR (buy mumbai property) OR (buy mumbai real estate) OR (purchase mumbai home) OR (purchase mumbai house) OR (purchase mumbai flat) OR (purchase mumbai property) OR (purchase real estate mumbai) -sale"

query_chennai= "(buying chennai flat) OR (buying chennai property) OR (buying chennai real estate) OR (purchasing chennai flat) OR (purchasing chennai property) OR (purchasing real estate chennai) OR (buy chennai flat) OR (buy chennai property) OR (buy chennai real estate) OR (purchase chennai flat) OR (purchase chennai property) OR (purchase real estate chennai) -sale"

home_house= "(buying mumbai home) OR (buying mumbai house) OR (purchasing mumbai home) OR (purchasing mumbai house) OR (buy mumbai home) OR (buy mumbai house) OR (purchase mumbai home) OR (purchase mumbai house) -sale"

looking_searching= "(looking mumbai flat) OR (looking mumbai property) OR (looking mumbai real estate) OR (searching mumbai flat) OR (searching mumbai property) OR (searching real estate mumbai) OR (look mumbai flat) OR (look mumbai property) OR (look mumbai real estate) OR (search mumbai flat) OR (search mumbai property) OR (search real estate mumbai) -sale"

shift="(shift mumbai flat) OR (shifting mumbai flat) OR (shift mumbai property) OR (shifting mumbai property) OR (shift mumbai house) OR (shifting mumbai house) -packers"

move= "(move mumbai flat) OR (moving mumbai flat) OR (move mumbai property) OR (moving mumbai property) OR (move mumbai house) OR (moving mumbai house)"

shift_move="(move mumbai flat) OR (moving mumbai flat) OR (move mumbai property) OR (moving mumbai property) OR (move mumbai house) OR (moving mumbai house) OR (shift mumbai flat) OR (shifting mumbai flat) OR (shift mumbai property) OR (shifting mumbai property) OR (shift mumbai house) OR (shifting mumbai house) -packers"

table= "keywords"

#Defining tweet attributes
id1=list()
username1=list()
name=list()
location=()
polarity=()
created_at=list()
text1=list()

try:     
    conn = psycopg2.connect(database='Hiranandani', user = "postgres", password = "parth123n@#*", host = "127.0.0.1", port = "5432")    
except:
    print("Create database first")


if(conn):
    '''
    Check if this table exits. If not, then create a new one.
    '''
    mycursor = conn.cursor()
    mycursor.execute("""
        SELECT COUNT(*)
        FROM information_schema.tables
        WHERE table_name = '{0}'
        """.format(table)
    if mycursor.fetchone()[0] != 1:
        active.create_tweet_table(table)        
        conn.commit()
    mycursor.close()



tweetCriteria = got.manager.TweetCriteria().setQuerySearch(working_mumbai)\
                                           .setSince("2019-01-01")\
                                           .setUntil("2019-12-19")\
                                           .setMaxTweets(100000)
tweet = got.manager.TweetManager.getTweets(tweetCriteria)

    

for i in tweet:
    text1 = active.deEmojify(i.text)     
    text=active.clean_tweet(text1)
    sentiment = TextBlob(text).sentiment
    polarity = sentiment.polarity
    stat=api.get_status(i.id)
    loco=stat.user.location
    fname=stat.
    # Store all data in MySQL
    if(conn):
        mycursor = conn.cursor()
        if 'hiranandani' not in (i.user.screen_name).lower():
            sql = "INSERT INTO {} (id, name, username, tweet_text,created_at,location,polarity) VALUES \
                   (%s, %s, %s, %s, %s, %s, %s)".format(table)
            val = (i.id, i.username,i.text,i.date, loco, polarity)
            mycursor.execute(sql, val)
            
            conn.commit()
        





