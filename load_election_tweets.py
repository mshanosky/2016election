"""
Read tweets from MongoDB and add to mySQL election database
Adds Retweet as a regular tweet for first retweet and ignores duplicate retweets
Adds quoted tweet
Runs AFINN , sentiNET and sentiWordCOunt sentiment and inserts in DB
Uses DB election and table tweets
"""
import datetime
from dateutil import parser
from afinn import Afinn
from sentinet import SentimentAnalysis
from sentiwordcount import SentiWordCount
from pymongo import MongoClient
import mysql.connector  
from mysql.connector import Error


#client = MongoClient('mongodb://192.168.1.91:27018')
client = MongoClient('mongodb://localhost:27017')
# database name
db = client['twitterP5_db']
# collection name
collection = db['collection']
print ("Records to process: " + str(collection.count()))

cnx = mysql.connector.connect(user='root', password='MySQLfromOracle',
                              host='127.0.0.1', db='election', charset='utf8mb4', collation='utf8mb4_unicode_ci')
cur = cnx.cursor()
insert_sql= """INSERT IGNORE INTO tweets_a (tweet_id, usr_id, text, date,retweet,quoted,referrer_tweet_id,rt_cnt,trump, \
              clinton, af_score, senti_score, wc_score, regression) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) """
select_sql= """SELECT COUNT(1) FROM tweets_a WHERE tweet_id = %s LIMIT 1"""

# create Afinn, SentiNet and SentiWordCount scorers
#afinn = Afinn ()
#senti = SentimentAnalysis(filename='sentiwordnet.txt',weighting='average')
#wc = SentiWordCount(pos_file='positive-word-list.txt', neg_file='negative-word-list.txt')

def add_tweet(text) :
    tw_id = int(text['id'])
    usr_id = int(text['user']['id'])
    tweet_str = text['text'] 
    rt_cnt = int(text['retweet_count'])
    #af_score = afinn.score (tweet_str)
    #senti_score = senti.score(tweet_str)
    #wc_score = wc.wordcount(tweet_str)
    af_score, wc_score, senti_score = None, None, None
    ins_data = (tw_id,usr_id,tweet_str,date,retweet,quoted,referrer_tweet_id, \
                rt_cnt,trump,clinton,af_score,senti_score,wc_score,None) 
    try:
        cur.execute(insert_sql,ins_data)
    except Error as error:
        print(error)
        print("record # " + str(i))
    cnx.commit() 
    return

i, j = 0, 100000
tweets_iterator = collection.find()
for tweet in tweets_iterator:
    i += 1 
    if tweet['lang'] == 'en':
        retweet, quoted, referrer_tweet_id = False, False, None
        #check that tweet mentions trump or clinton
        tweet_str = tweet['text']
        trump = True if 'trump' in tweet_str.lower() else False
        clinton = True if 'clinton' in tweet_str.lower() else False
        if trump or clinton:
            # add user and retweet user and tweet
            date = parser.parse(tweet['created_at']).strftime("%Y-%m-%d %H:%M:%S")
            if 'retweeted_status' in tweet:
                #check if tweet is in database
                tweet_id = int(tweet['retweeted_status']['id'])
                cur.execute(select_sql,(tweet_id,))
                if cur.fetchone()[0]: 
                    continue
                else: #add tweet
                    retweet = True
                    referrer_tweet_id = int(tweet['id'])
                    add_tweet(tweet['retweeted_status'])    
            else: 
                add_tweet(tweet) 
            # if a quoted tweet add quoted tweet
            if 'quoted_status' in tweet:
                tweet_str = tweet['quoted_status']['text']
                trump = True if 'trump' in tweet_str.lower() else False
                clinton = True if 'clinton' in tweet_str.lower() else False
                if trump or clinton:
                    #check if utweet is in database
                    tweet_id = int(tweet['quoted_status']['id'])
                    cur.execute(select_sql,(tweet_id,))
                    if cur.fetchone()[0]: 
                        continue
                    else: 
                        quoted = True
                        referrer_tweet_id = int(tweet['id'])
                        add_tweet(tweet['quoted_status'])
    if i >= j :
        print("processed " + str(i))
        j = i + 100000
        #break
cur.close()  
cnx.close() 

               

       
