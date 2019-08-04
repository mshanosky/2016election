"""
Updates sentiment score fields
Uases DB election and table tweets


"""
import mysql.connector  
from mysql.connector import Error
from afinn import Afinn
from sentinet import SentimentAnalysis
from sentiwordcount import SentiWordCount

cnx = mysql.connector.connect(user='root', password='MySQLfromOracle',
                              host='127.0.0.1', db='election', charset='utf8mb4', collation='utf8mb4_unicode_ci')
cur = cnx.cursor()

searchSQL= """SELECT tweet_id, text FROM tweets_a where senti_score IS NULL LIMIT 1"""
updateSQL= """UPDATE tweets_a SET af_score = %s, senti_score = %s, wc_score = %s WHERE tweet_id = %s;"""


afinn = Afinn ()
senti = SentimentAnalysis(filename='sentiwordnet.txt',weighting='average')
wc = SentiWordCount(pos_file='positive-word-list.txt', neg_file='negative-word-list.txt')


i, j = 0, 100000
while i <= 1000000 :
    i += 1
    try:
        cur.execute(searchSQL)
    except Error as error:
        print(error)
        break
    search_list = cur.fetchone()
    tweet_id = search_list[0]
    tweet_str = search_list[1]

    af_score = afinn.score (tweet_str)
    senti_score = senti.score(tweet_str)
    wc_score = wc.wordcount(tweet_str)
                
    update_data = (af_score,senti_score,wc_score,tweet_id)
    #print(tweet_str)
    #print(update_data)
    try:
        cur.execute(updateSQL,update_data)
    except Error as error:
        print(error)
    cnx.commit()
    if i >= j :
        print("processed " + str(i))
        j = i + 100000
        #break
cur.close()  
cnx.close() 