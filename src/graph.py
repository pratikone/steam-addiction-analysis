import networkx as nx
import numpy as np
import sql_fetch
import pickle
import matplotlib.pyplot as plt
import sys
from networkx.algorithms.community import k_clique_communities
from networkx.algorithms.approximation import k_components
import community
from visualization import *
from collections import Counter

def create_graph( given_list_tuple, friends = None ) :
    G = nx.Graph()
    for given_list in given_list_tuple :
        for entry in given_list :
            user = str(entry[0])+"u"
            # if user == "14698u" :
                # print(entry)
            if user not in G.nodes() :
                G.add_node(user, type="user", playtime = 0)

            if len(entry) == 3 :  #harcoded user groups playtime
                group = str(entry[1])+"p"
                if group not in G.nodes() :
                    G.add_node(group, type="group")
                if G.has_edge(user, group ) is False :
                    G.add_edge( user, group, weight = 1 )
            else :
                game = str(entry[1])+"g"
                playtime = int(entry[2])
                genre = entry[3]
                if game not in G.nodes() :
                    G.add_node(game, type="game", playtime = 0, genre=None)
                if G.has_edge( user, game ) is False :
                    G.nodes[game]['genre'] = genre
                    G.nodes[user]['playtime'] += playtime
                    G.nodes[game]['playtime'] += playtime
                    G.add_edge( user, game, weight = playtime)
    if friends is not None :
        for f in friends :
            nodeA = str(f[0]) + 'u'
            nodeB = str(f[1]) + 'u'
            G.add_edge( nodeA, nodeB, weight=1)

    return G


def add_edges_friends( G, friends_list ) :
    for entry in friends_list :
        G.add_edge( entry.user_id_a, entry.user_id_b )   # TODO : add weight here , if needed

def achaar_it( G, file_name ) :  #pickle it, pickle = achaar in Hindi
    try :
        pickle.dump( G, open( file_name, "wb" ), protocol=2 )
    except pickle.PickleError as e :
        print("Could not pickle due to error ", e)

def unachaar_it( file_name) : #unpickle it, pickle = achaar in Hindi
    try :
        G = pickle.load( open( file_name, "rb" ) )
        return G
    except pickle.PickleError as e :
        print("Could not pickle due to error ", e)
    return None


def get_all( final_list  ) :
    all_users = []
    all_games = []
    all_groups = []
    for entry in final_list :
        if entry.user_id not in all_users :
            all_users.append( entry.user_id )
        if entry.group_id not in all_groups :
            all_groups.append( entry.group_id )
        if entry.game_id not in all_games :
            all_games.append( entry.game_id )

    all_users_size, all_groups_size, all_games_size = len(set(all_users)), len(set(all_groups)), len(set(all_games))
    # print(len(all_users), len(all_groups), len(all_games) )
    print(all_users_size, all_groups_size, all_games_size)
    arr = np.zeros((all_users_size, all_groups_size, all_games_size))
    for entry in final_list :
        user_index = all_users.index(entry.user_id)                     
        group_index = all_groups.index(entry.group_id)
        game_index = all_games.index(entry.game_id)
        arr[user_index, group_index, game_index] = 1
    return arr


def stats( G, partition) :
    print("Nodes :", G.number_of_nodes())
    print("Edges :", G.number_of_edges())
    print("partitions", len(set(partition.values())))
    temp_game_genre_list = []
    avg_playtime = {}
    for node in G.nodes() :
        if G.nodes[node]['type'] == 'game' :
            genre = G.nodes[node]['genre'] 
            if genre is not None :
                genre_list =  genre.split(",")
                temp_game_genre_list += genre_list
                for g in genre_list :
                    if g in avg_playtime : 
                        avg_playtime[g] +=  G.nodes[node]['playtime']
                        avg_playtime[g] =  round(avg_playtime[g] / 2.0)
                    else :
                        avg_playtime[g] = 0

    c = Counter(temp_game_genre_list)
    print(c.most_common())
    print(avg_playtime)



def show() :
    G = create_graph(data)
    draw_graph(G)
    playtime_list = [ G.nodes[x]['playtime'] for x in G.nodes() if G.nodes[x]['type'] == "user" ]
    plt.plot( sorted(playtime_list))
    plt.ylabel('playing mins')
    plt.title("Users")
    plt.show()
    playtime_game_list = [ G.nodes[x]['playtime'] for x in G.nodes() if G.nodes[x]['type'] == "game" ]
    plt.plot( sorted(playtime_game_list))
    plt.title("Games")
    plt.show()

def create_list_user_group_game_playtime( final_lists ) :  #final_lists is user_groups, user_games
    a_large_list = []
    user_groups_list = []
    user_games_list = []

    for final_inner_list in final_lists :
        for entry in final_inner_list :
            inner_list = []
            inner_list.append( entry.user_id )
            if type(entry) == type(sql_fetch.dummy_Steam_User_Groups) :
                inner_list.append( entry.group_id )
                inner_list.append( 1 )
            else :
                inner_list.append( entry.game_id )
                inner_list.append( entry.playtime )
                inner_list.append( entry.genre )
            a_large_list.append( inner_list )
        if type(entry) == type(sql_fetch.dummy_Steam_User_Groups) :
            user_groups_list = a_large_list
        else :
            user_games_list = a_large_list
    return (user_groups_list, user_games_list)

def draw_graph(G) :
    pos=nx.spring_layout(G) # positions for all nodes
    # nodes
    nx.draw_networkx_nodes(G,pos,
                       nodelist=[x for x in G.nodes() if G.nodes[x]['type'] == "user"],
                       node_color='r',
                       node_size=10,
                   alpha=0.8)
    nx.draw_networkx_nodes(G,pos,
                       nodelist= [x for x in G.nodes() if G.nodes[x]['type'] == "group"],
                       node_color='b',
                       node_size=10,
                   alpha=0.8)

    nx.draw_networkx_nodes(G,pos,
                       nodelist= [x for x in G.nodes() if G.nodes[x]['type'] == "game"],
                       node_color='g',
                       node_size=10,
                   alpha=0.8)


    # edges
    nx.draw_networkx_edges(G,pos,
                       edgelist = G.edges(),
                       width=0.2,alpha=0.5,edge_color='k')
    plt.show()

DIR = "C:/Users/Pratik Anand/Desktop/dataset10000"
def read_gamefile() :
    user_games_list = []
    user_set = set()
    game_genre = {}
    with open(DIR+"/game_matrix.txt") as f :
        for line in f :
            user, game , playtime = line.strip().split()
            user_games_list.append([user.strip(), game.strip(), playtime.strip()])
            game_genre[game] = None
            user_set.add(user)

    
    with open(DIR + "/game_names.txt") as f :  
        i = 0
        for line in f :
            i = i+1
            game_genre[str(i)] = line.strip()

    # print(game_genre)
    for entry in user_games_list :
       game = entry[1]
       entry.append( game_genre[game])
    #print(user_games_list)
    print(len(user_set))

    return user_games_list

def read_groupmatrix() :
    user_group_list = []
    user_set = set()
    with open(DIR + "/group_matrix.txt") as f :
        for line in f :
            user, group = map(  lambda x: x.strip()  , line.split())
            user_group_list.append([user, group, 1])
            user_set.add(user)
    # print(user_group_list)   
    print(len(user_set))
    return user_group_list





def init_1() :
    final_list = sql_fetch.init()
    # achaar_it(final_list, "user_group_game_list.p")
    arr = get_all( final_list )
    achaar_it(arr, "user_group_game_adj.p")
    arr = unachaar_it("user_group_game_adj.p")
    print(np.shape(arr))
    print(arr[arr==1].shape)

    import numpy as np
    import tensorflow as tf
    from scipy.io.matlab import loadmat
    sys.path.insert(0,'../../tf-decompose')
    from ktensor import KruskalTensor

    X = arr
    # Build ktensor and learn CP decomposition using ALS with specified optimizer
    T = KruskalTensor(X.shape, rank=300, regularize=1e-6, init='nvecs', X_data=X)
    X_predict = T.train_als(X, tf.train.AdadeltaOptimizer(0.05), epochs=1)
    

def init_2() :
    #friends_list, user_games_list = sql_fetch.init()
    #G  = create_graph(user_games_list)
    #add_edges_friends(G, friends_list)
    #achaar_it(G, "achaar.p")
    G = unachaar_it("achaar.p")
    print("edges", G.number_of_edges())
    print("nodes", G.number_of_nodes())
    # print(nx.betweenness_centrality(G))
    # print( nx.number_connected_components(G))
    # print(sorted(nx.triangles(G).values()))


#def init_3() :
    # final_lists = sql_fetch.init()
    # data = create_list_user_group_game_playtime( final_lists )
    # achaar_it(data, "user_data.p")
    # friends = sql_fetch.find_friends_from_user_groups(final_lists[0])
    # achaar_it(friends, "user_friends.p")

    # data = unachaar_it("user_data.p")
    # friends = unachaar_it("user_friends.p")
    # G = create_graph(data, friends)
    # partition = community.best_partition(G)  # compute communities
    # stats(G, partition)
    # #create_graph_partition_viz(G, partition)
    # show_bargraph(G)

def init_4() :
    data =   [read_groupmatrix(), read_gamefile()]
    G = create_graph(data, None)
    partition = community.best_partition(G)  # compute communities
    stats(G, partition)
    # #create_graph_partition_viz(G, partition)
    show_bargraph(G)

    # user_playtime = {}
    # final_list = []
    # for x in G.nodes() :
    #     if G.nodes[x]['type'] == "user" :
    #         user_playtime[ x[:-1] ] = G.nodes[x]['playtime']
    # for key, value in sorted(user_playtime.items(), key = lambda item: item[1], reverse =  True):
    #     final_list.append( [key, value] )
    # f = open('user_playtime', 'w')
    # for entry in final_list :
    #     f.write('{} {}\n'.format( entry[0], entry[1] ))  # python will convert \n to os.linesep
    # f.close()
   

    # group_playtime = {}
    # final_list = []
    # for x in G.nodes() :
    #     if G.nodes[x]['type'] == "group" :
    #         total_playtime = 0
    #         for n in G.neighbors(x) :
    #             if G.nodes[n]['type'] == "user" :
    #                 total_playtime += G.nodes[n]['playtime'] 
    #         group_playtime[ x[:-1] ] = total_playtime
    # for key, value in sorted(group_playtime.items(), key = lambda item: item[1], reverse =  True):
    #     final_list.append( [key, value] )
    # f = open('group_playtime', 'w')
    # for entry in final_list :
    #     f.write('{} {}\n'.format( entry[0], entry[1] ))  # python will convert \n to os.linesep
    # f.close()

    # game_playtime = {}
    # final_list = []
    # for x in G.nodes() :
    #     if G.nodes[x]['type'] == "game" :
    #         game_playtime[ x[:-1] ] = G.nodes[x]['playtime']
    # for key, value in sorted(game_playtime.items(), key = lambda item: item[1], reverse =  True):
    #     final_list.append( [key, value] )
    # f = open('game_playtime', 'w')
    # for entry in final_list :
    #     f.write('{} {}\n'.format( entry[0], entry[1] ))  # python will convert \n to os.linesep
    # f.close()


   
    








if __name__ == '__main__' :
    init_4()
  
    