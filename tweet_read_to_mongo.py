# -*- coding: utf-8 -*-
"""
Created on Fri Aug 19 06:50:45 2016

@author: ready_000
"""

import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
import io
#get Twitter keys
ckey = '7qtfsNQL9UjQTWnaIoODmpEtK'
consumer_secret = 'KP9HsjrjiUr8q2samZpWum2JiIwCaPY3e5Lz21rVroughe0qFz'
access_token_key = '759797965221343232-fmijl4goTHa21WmzifC528Km7LkTiAZ'
access_token_secret = 'X1vGV6GaEy6toOEvBFktdtINTu5KwBaMEC98dfgMs1uRw'
 
 
start_time = time.time() #grabs the system time
keyword_list = ['Olympics'] #track list

#Listener Class Override
class listener(StreamListener):
 
	def __init__(self, start_time, time_limit=60):
 
		self.time = start_time
		self.limit = time_limit
		self.tweet_data = []
 
	def on_data(self, data):
 
		saveFile = io.open('raw_tweets.json', 'a', encoding='utf-8')
 
		while (time.time() - self.time) < self.limit:
 
			try:
 
				self.tweet_data.append(data)
 
				return True
 
 
			except BaseException as e:
				print('failed ondata,', str(e))
				time.sleep(5)
				pass
 
		saveFile = io.open('raw_tweets.json', 'w', encoding='utf-8')
		saveFile.write(u'[\n')
		saveFile.write(','.join(self.tweet_data))
		saveFile.write(u'\n]')
		saveFile.close()
		exit()
 
	def on_error(self, status):
 
		print(status)
  
auth = OAuthHandler(ckey, consumer_secret) #OAuth object
auth.set_access_token(access_token_key, access_token_secret)
 
 
twitterStream = Stream(auth, listener(start_time, time_limit=20)) #initialize Stream object with a time out limit
twitterStream.filter(track=keyword_list, languages=['en'])  #call the filter method to run the Stream Object