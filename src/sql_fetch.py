#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
from collections import namedtuple

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
    Steam_User = namedtuple('SteamUser', 'user_id')
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


def get_games_list( connection, users ) :
  try :
    Steam_Games = namedtuple('SteamGames', ['user_id', 'game_id_list'])
    user_games_list = []
    for user in users :
      my_good_list = []
      cur = connection.cursor()
      cur.execute("SELECT * FROM steam.games_1 where steamid='{}' LIMIT 0, 500 ;".format(user.user_id))
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


def init() :
  connection = create_connection()
  user_list = get_user_id( connection )
  user_games_list = get_games_list(connection, user_list)
  return user_games_list


if __name__ == '__main__' :
  print(init())


