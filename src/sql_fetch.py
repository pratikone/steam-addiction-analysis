#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
from collections import namedtuple

#friendly neighborhood tuples
Steam_User = namedtuple('SteamUser', 'user_id')
Steam_Games = namedtuple('SteamGames', ['user_id', 'game_id_list'])
Steam_Friends = namedtuple('SteamFriend', 'user_id_a, user_id_b')
Steam_User_Groups = namedtuple('SteamUserGroups', 'user_id, group_id')
# Steam_User_Games_Playtime_Genre = namedtuple('SteamUserGamesPlaytimeGenre', 'user_id, group_id, game_id, playtime')
Steam_User_Games = namedtuple('SteamUserGames', 'user_id, game_id, playtime, genre')


dummy_Steam_User_Groups = Steam_User_Groups(0,0)
dummy_Steam_User_Games = Steam_User_Games(0,0,0,0)

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

def fetch_user_group_games_playtime(connection) :
  try :
    final_list = []
    cur = connection.cursor()
    #cur.execute("SELECT gr.steamid, gr.groupid, g1.appid FROM steam.groups as gr, steam.games_1 as g2 \
    #                         where gr.steamid = g2.steamid  LIMIT 1000, 5000")

    #cur.execute("SELECT gr.steamid, gr.groupid, g1.appid FROM steam.groups as gr, steam.games_1 as g2 \
    #                         where gr.steamid = g2.steamid  LIMIT 1000, 5000")

    #op = cur.fetchall()
    

    #get users
    cur.execute(" SELECT steamid from steam.player_summaries limit 1000, 12500 ;")
    op = cur.fetchall()
    user_list = []
    for entry in op :    
      user_list.append(entry[0])

    #get groups of those users
    user_groups = []
    for user in user_list :
      cur.execute(" SELECT steamid, groupid from steam.groups where steamid={} limit 3;".format(user)  )
      op = cur.fetchall()
      for entry in op :    
        groupid = entry[1]
        if groupid is None : continue
        user_groups.append(  Steam_User_Groups(user, groupid) )

    #get games
    user_games = []
    for i in user_groups :
      cur.execute(" SELECT steamid, appid, playtime_forever from steam.games_1 where steamid={} limit 150;".format(i.user_id)  )
      op = cur.fetchall()
      for entry in op :    
        game_id = entry[1]
        if game_id is None :      continue
        playtime_forever = entry[2]
        if playtime_forever is None :    continue
        cur.execute("SELECT Genre FROM steam.games_genres where appid={} LIMIT 1;".format(game_id) )
        op = cur.fetchall()
        for entry in op :
          user_games.append( Steam_User_Games( i.user_id, game_id, playtime_forever, entry[0]) )

    return user_groups, user_games
  except mdb.Error as e:
      print( "Error %d: %s" % (e.args[0],e.args[1]))
      if connection:    
        connection.close()
      sys.exit(1)

def find_friends_from_user_groups(user_groups) :
    users = set()
    for i in user_groups :
      users.add( i.user_id )
    return find_friends(users)

def find_friends(users) :
  connection = create_connection()
  cur = connection.cursor()
  friends = []
  try :
    for user in users :
      cur.execute("SELECT * FROM steam.friends where steamid_a = {0} or steamid_b = {0};".format(user) )
      op = cur.fetchall()
      for entry in op :
        if entry[0] == user :
          friend = entry[1]
        else :
          friend = entry[0]
        if friend in users :
          friends.append( (user, friend))
  except mdb.Error as e:
    print( "Error %d: %s" % (e.args[0],e.args[1]))
    if connection:    
      connection.close()
    sys.exit(1)
  return friends





def init() :
  connection = create_connection()
  # user_list = get_user_id( connection )
  # friends_list = get_user_via_friends( connection )
  # user_games_list = get_games_list(connection, get_user_id_from_friends( friends_list) )
  
  # friends_list, user_games_list = get_user_and_games_together( connection )
  # return friends_list, user_games_list
  return fetch_user_group_games_playtime(connection)


if __name__ == '__main__' :
  print(init())


