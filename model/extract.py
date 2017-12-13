#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb
import sys
from collections import namedtuple

from pdb import set_trace as st
#friendly neighborhood tuples
Steam_User = namedtuple('SteamUser', 'user_id')
Steam_Games = namedtuple('SteamGames', ['user_id', 'game_id_list'])
Steam_Friends = namedtuple('SteamFriend', 'user_id_a, user_id_b, since')
Steam_User_Groups = namedtuple('SteamUserGroups', 'user_id, group_id')
# Steam_User_Games_Playtime_Genre = namedtuple('SteamUserGamesPlaytimeGenre', 'user_id, group_id, game_id, playtime')
Steam_User_Games = namedtuple('SteamUserGames', 'user_id, game_id, playtime')


dummy_Steam_User_Groups = Steam_User_Groups(0,0)
dummy_Steam_User_Games = Steam_User_Games(0,0,0)
curG=None
def create_connection() :
  try:
      con = mdb.connect('127.0.0.1','sloke', 'password', 'steam', port=3307,read_default_file="/home/sloke/MySQL/my.cnf");
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

user_set =set()
from collections import deque
userq = deque()
def bfs(limit,cur):
    while len(userq)!=0:
        elem = userq.pop()
        cur.execute(" SELECT steamid_b from steam.Friends where steamid_a= "+str(elem)+";")
        op = cur.fetchall()
        for entry in op:
            if entry[0] not in user_set:
                userq.append(entry[0])
        user_set.add(elem)
        if len(user_set)%1000==0:
            print len(user_set)
        if len(user_set)>limit:
            print 'H2'
            break
    friends_graph=[]
    print len(user_set)
    for i in user_set:
        cur.execute(" SELECT steamid_b from steam.Friends where steamid_a= "+str(i)+";")
        op = cur.fetchall()
        for entry in op:
            if entry[0] in user_set:
                friends_graph.append((i,entry[0]))
    return (user_set,friends_graph)


def fetch_user_group_games_playtime(connection,usr_count) :
  try :
    final_list = []
    cur = connection.cursor()
    #cur.execute("SELECT gr.steamid, gr.groupid, g1.appid FROM steam.groups as gr, steam.games_1 as g2 \
    #                         where gr.steamid = g2.steamid  LIMIT 1000, 5000")

    #cur.execute("SELECT gr.steamid, gr.groupid, g1.appid FROM steam.groups as gr, steam.games_1 as g2 \
    #                         where gr.steamid = g2.steamid  LIMIT 1000, 5000")

    #op = cur.fetchall()
    

    #get users
    cur.execute(" SELECT steamid from steam.Player_Summaries limit 1 ;")
    op = cur.fetchall()
    user_list = set()
    for entry in op :    
      userq.append(entry[0])
    print userq
    uset,graph = bfs(usr_count,cur)
    user_list = list(uset)

    #get groups of those users
    i=0
    users_dict = {}
    for user in user_list:
        users_dict[user] = i
        i+=1
    i=0
    
    user_groups = []
    groups_dict={}
    group_set =  set()
    for user in user_list :
      cur.execute(" SELECT steamid, groupid from steam.Groups where steamid={} limit 3;".format(user)  )
      op = cur.fetchall()
      for entry in op :    
        groupid = entry[1]
        group_set.add(groupid)
        if groupid is None : continue
        user_groups.append(  Steam_User_Groups(user, groupid) )

    groups_count_dict={}
    for ug in user_groups:
        usr = ug[0]
        group = ug[1]
        if group not in groups_count_dict:
            groups_count_dict[group]=set()
            groups_count_dict[group].add(usr)
        else:
            if len(groups_count_dict[group])<2:
                groups_count_dict[group].add(usr)

    i=0
    for group_id in group_set:
        if len(groups_count_dict[group_id])>1:
            groups_dict[group_id] = i
            i+=1

    #get games
    user_games = []
    j=0
    games_dict={}
    game_set=set()
    for i in user_groups :
      cur.execute(" SELECT steamid, appid, playtime_forever from steam.Games_2 where steamid={} ;".format(i.user_id)  )
      op = cur.fetchall()
      j+=1
      for entry in op :    
        game_id = entry[1]
        if game_id is None :      continue
        playtime_forever = entry[2]
        if playtime_forever is None :    continue
        game_set.add(game_id)
        user_games.append( Steam_User_Games( i.user_id, game_id, playtime_forever) )

    games_count_dict={}
    for ug in user_games:
        usr = ug[0]
        game = ug[1]
        if game not in games_count_dict:
            games_count_dict[game]=set()
            games_count_dict[game].add(usr)
        else:
            if len(games_count_dict[game])<2:
                games_count_dict[game].add(usr)

    i=0
    game_names =[]
    for game_id in game_set:
        if len(games_count_dict[game_id])>1:
            cur.execute("SELECT * from App_ID_Info where appid="+str(game_id))
            op = cur.fetchall()
            games_dict[game_id] = i 
            for entry in op:
              # (i,entry)
              cur.execute("SELECT * from Games_Genres where appid="+str(game_id))
              op2 = cur.fetchall()
              genres = []
              for entry2 in op2:
                genres.append(entry2[1])
              game_names.append((','.join(genres),))
            i+=1
    j=0
    games_dict_2={}
    for i in user_games:
      if i[2] > 0 and i[1] in games_dict and i[1] not in games_dict_2:
          games_dict_2[i[1]]=j
          j+=1
          #print sorted(games_dict_2.values())[0]   
    games_dict = games_dict_2

    graph_conv = set()
    for i in graph:
        l2 =  (users_dict[i[0]],users_dict[i[1]],)
        if i[0] in users_dict and i[1] in users_dict :
            graph_conv.add(l2)

    user_groups_conv=[]
    for i in user_groups:
        if i[0] in users_dict and i[1] in groups_dict:
            user_groups_conv.append( (users_dict[i[0]],groups_dict[i[1]]))
    
    user_games_conv=set()
    for i in user_games:
        if i[0] in users_dict and i[1] in games_dict and i[2]>0:
            user_games_conv.add((users_dict[i[0]],games_dict[i[1]],i[2]) )
    return graph_conv, user_groups_conv, user_games_conv,users_dict,groups_dict,games_dict,game_names

  except mdb.Error as e:
      print( "Error %d: %s" % (e.args[0],e.args[1]))
      if connection:    
        connection.close()
      sys.exit(1)



def write_csv(samples, csv_file):
    import csv
    if type(samples)==dict:
        samples = [(v, k) for k, v in samples.iteritems()]
    with open(csv_file, "wb") as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerows(samples)

def construct_cooccurence(samples,g_dict):
  # Identify unique groups
  g_cooccurence_dict = {}
  for ug in samples:
    u = ug[0]
    g = ug[1]
    if g not in g_cooccurence_dict:
      g_cooccurence_dict[g] = set()
      g_cooccurence_dict[g].add(u)
    else:
      g_cooccurence_dict[g].add(u)

  context_dict_g = []
  for g1 in g_dict.values():
    for g2 in g_dict.values():
      l2 = len(g_cooccurence_dict[g1].intersection(g_cooccurence_dict[g2]))
      l = float(l2) / (len(g_cooccurence_dict[g1])*len(g_cooccurence_dict[g2]))
      if g1!=g2 and l2>1 :
        context_dict_g.append((g1,g2,l))

  return context_dict_g


  # Identify unique games

def init() :
  connection = create_connection()
  # user_list = get_user_id( connection )
  # friends_list = get_user_via_friends( connection )
  # user_games_list = get_games_list(connection, get_user_id_from_friends( friends_list) )
  
  # friends_list, user_games_list = get_user_and_games_together( connection )
  # return friends_list, user_games_list
  graph_conv, user_groups_conv, user_games_conv,users_dict,groups_dict,games_dict,game_names = fetch_user_group_games_playtime(connection,int(sys.argv[1]))  
  from pdb import set_trace as st
  groups_cooccurence = construct_cooccurence(user_groups_conv,groups_dict)
  games_cooccurence = construct_cooccurence(user_games_conv,games_dict)
  write_csv(graph_conv,'friends.txt')
  write_csv(user_groups_conv,'group_matrix.txt')
  write_csv(user_games_conv,'game_matrix.txt')
  write_csv(users_dict,'user_mapping.txt')
  write_csv(groups_dict,'group_mapping.txt')
  write_csv(games_dict,'game_mapping.txt')
  write_csv(game_names,'game_names.txt')
  write_csv(groups_cooccurence,'groups_cooccurence.txt')
  write_csv(games_cooccurence,'games_cooccurence.txt')



if __name__ == '__main__' :
  print(init())

