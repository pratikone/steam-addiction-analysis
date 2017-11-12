#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
from collections import namedtuple

#friendly neighborhood tuples
Steam_User = namedtuple('SteamUser', 'user_id')
Steam_Games = namedtuple('SteamGames', ['user_id', 'game_id_list'])
Steam_Friends = namedtuple('SteamFriend', 'user_id_a, user_id_b, since')
Steam_User_Games = namedtuple('SteamUserGames', 'user_id, group_id, game_id')



def create_connection() :
  try:
      con = mdb.connect('localhost', 'root', 'root', 'steam');
      cur = con.cursor()
      cur.execute("SELECT VERSION()")
      ver = cur.fetchone()
      print("Database version : %s " % ver)
      return con

  except mdb.Error as e:
      print( "Error %d: %s" % (e.args[0],e.args[1]))
      if con:    
          con.close()
      sys.exit(1)
      
def get_user_id( connection ) :
  try :
    my_good_list = []
    cur = connection.cursor()
    cur.execute("SELECT * FROM steam.player_summaries LIMIT 0, 500;")
    op = cur.fetchall()
    for entry in op :
      user = Steam_User(entry[0])
      my_good_list.append(user)

    return my_good_list
  except mdb.Error as e:
      print( "Error %d: %s" % (e.args[0],e.args[1]))
      if connection:    
        connection.close()
      sys.exit(1)

def get_user_id_from_friends( friends ) :
  user_list = []
  for entry in friends :
     user_list.append(Steam_User(entry.user_id_a))
     user_list.append(Steam_User(entry.user_id_b))
  return user_list

def get_games_list( connection, users ) :
  try :
    user_games_list = []
    for user in users :
      my_good_list = []
      cur = connection.cursor()
      cur.execute("SELECT * FROM steam.games_1 where steamid='{}' LIMIT 10000, 500;".format(user.user_id))
      op = cur.fetchall()
      for entry in op :
        my_good_list.append(entry[1])
        
      user_game = Steam_Games(user.user_id, my_good_list)
      
      if user_game.game_id_list :      #prevent empty lists
        user_games_list.append(user_game)


    return user_games_list
  except mdb.Error as e:
      print( "Error %d: %s" % (e.args[0],e.args[1]))
      if connection:    
        connection.close()
      sys.exit(1)

def get_user_via_friends( connection ) :
  try :
    friends_list = []
    cur = connection.cursor()
    cur.execute("SELECT * FROM steam.friends LIMIT 100000, 5000;")
    op = cur.fetchall()
    for entry in op :
      user = entry[0]
      another_user = entry[1]
      friends_since = entry[3]
      friends_obj = Steam_Friends(user_id_a = user, user_id_b = another_user, since=friends_since )
      friends_list.append( friends_obj )
    return friends_list
  except mdb.Error as e:
      print( "Error %d: %s" % (e.args[0],e.args[1]))
      if connection:    
        connection.close()
      sys.exit(1)


def get_user_and_games_together(connection) :
  try :
    friends_list = []
    user_games_list = []
    cur = connection.cursor()
    cur.execute("SELECT f.steamid_a, f.steamid_b, f.friend_since, g.steamid, g.appid from steam.friends as f,\
                           steam.games_1 as g where g.steamid = f.steamid_a or g.steamid = f.steamid_b LIMIT 0, 5000000;")
    op = cur.fetchall()
    for entry in op :
      user = entry[0]
      another_user = entry[1]
      friends_since = entry[2]
      game_user = entry[3]
      game_id = entry[4]

      friends_obj = Steam_Friends(user_id_a = user, user_id_b = another_user, since=friends_since )
      friends_list.append( friends_obj )
      if user == game_user :
        entry_user = user
      else :
        entry_user = another_user
      user_game = Steam_Games(entry_user, game_id)
      user_games_list.append(user_game)
    return friends_list, user_games_list
  except mdb.Error as e:
      print( "Error %d: %s" % (e.args[0],e.args[1]))
      if connection:    
        connection.close()
      sys.exit(1)


def fetch_user_group_games(connection) :
  try :
    final_list = []
    cur = connection.cursor()
    cur.execute("SELECT gr.steamid, gr.groupid, g2.appid FROM steam.groups as gr, steam.games_2 as g2 \
                             where gr.steamid = g2.steamid  LIMIT 100000")
    op = cur.fetchall()
    for entry in op :
      user_id = entry[0]
      group_id = entry[1]
      game_id = entry[2]
      final_list.append(Steam_User_Games( user_id, group_id, game_id)  )
    return final_list
  except mdb.Error as e:
      print( "Error %d: %s" % (e.args[0],e.args[1]))
      if connection:    
        connection.close()
      sys.exit(1)




def init() :
  connection = create_connection()
  # user_list = get_user_id( connection )
  # friends_list = get_user_via_friends( connection )
  # user_games_list = get_games_list(connection, get_user_id_from_friends( friends_list) )
  
  # friends_list, user_games_list = get_user_and_games_together( connection )
  # return friends_list, user_games_list
  return fetch_user_group_games(connection)


if __name__ == '__main__' :
  print(init())


