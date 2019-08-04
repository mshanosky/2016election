"""
Check if user is in database, then add User , check if user is Russian
Uases DB election and table users
"""

import datetime
from restapi import fetch_users
from dateutil import parser
import mysql.connector  
from mysql.connector import Error

sql= """INSERT IGNORE INTO users (usr_id, name, screen_name, created, description, location, url, verified, followers, \
            friends, statuses, lists, current_usr, russian_usr, new_followers, new_friends, new_statuses, new_lists) \
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

sql0= """SELECT (1) FROM users WHERE usr_id = %s LIMIT 1"""
sql1= """SELECT (1) FROM russian_users WHERE usr_id = %s LIMIT 1"""

sql2= """UPDATE users SET followers = %s, friends = %s, statuses = %s, lists = %s WHERE usr_id = %s"""

def add_usr(user,cur,cnx,i):
    usr_id = int(user['id'])
    #check if user is in database
    if cur.execute(sql0,(usr_id,)): 
        return
    else: #add user
        name = user['name'] 
        screen_name = user['screen_name']
        created = parser.parse(user['created_at']).strftime("%Y-%m-%d %H:%M:%S") 
        description = user['description'] 
        location = user['location'] 
        url = user['url']  
        verfied = int(user['verified'])
        followers = int(user['followers_count'])
        friends = int(user['friends_count'])
        statuses = int(user['statuses_count'])
        # fix encountered error in one input record 
        if user['listed_count'] is None :
            lists = 0
            print("user Listed_count NoneType error " + str(j))
            print(user)
        else:
            lists = int(user['listed_count'])
        current_usr = None
        new_followers, new_friends, new_statuses, new_lists = None, None, None, None 
        #check for Russian user
        if cur.execute(sql1,(usr_id,)):
            russian_usr = 1
        else :
            russian_usr = 0    
        ins_data = (usr_id, name, screen_name, created, description, location, url, verfied, \
        followers, friends, statuses, lists, current_usr, russian_usr, new_followers, new_friends,  \
        new_statuses, new_lists)
        try:
            cur.execute(sql,ins_data)
        except Error as error:
            print(error)
        cnx.commit()
        return

   