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

def create_graph( given_list ) :
    G = nx.Graph()
    for entry in given_list :
        user = str(entry[0])+"u"
        group = str(entry[1])+"p"
        game = str(entry[2])+"g"
        playtime = entry[3]
        if user not in G.nodes() :
            G.add_node(user, type="user", playtime = 0)
        if group not in G.nodes() :
            G.add_node(group, type="group")
        if game not in G.nodes() :
            G.add_node(game, type="game", playtime = 0)
        if G.has_edge(user, group ) is False :
            G.add_edge( user, group )
        if G.has_edge( user, game ) is False :
            G.nodes[user]['playtime'] += playtime
            G.nodes[game]['playtime'] += playtime
            G.add_edge( user, game, weight = playtime)
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

def create_list_user_group_game_playtime( final_list ) :
    a_large_list = []
    stats_users = set()
    stats_groups = set()
    stats_games = set()
    for entry in final_list :
        inner_list = []
        inner_list.append( entry.user_id )
        inner_list.append( entry.group_id )
        inner_list.append( entry.game_id )
        inner_list.append( entry.playtime )
        a_large_list.append( inner_list )

        stats_users.add( entry.user_id )
        stats_groups.add( entry.group_id )
        stats_games.add( entry.game_id )

    print(  " users : {} groups : {}  games {} ".format(  len(stats_users), len(stats_groups), len(stats_games)    )    )
    if None in stats_users or None in stats_groups or None in stats_games : print("None is found. Clean the data")
    return a_large_list

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
    friends_list, user_games_list = sql_fetch.init()
    G  = create_graph(user_games_list)
    add_edges_friends(G, friends_list)
    achaar_it(G, "achaar.p")
    G = unachaar_it("achaar.p")
    print("edges", G.number_of_edges())
    print("nodes", G.number_of_nodes())
    # print(nx.betweenness_centrality(G))
    # print( nx.number_connected_components(G))
    # print(sorted(nx.triangles(G).values()))


def init_3() :
    #final_list = sql_fetch.init()
    #data = create_list_user_group_game_playtime( final_list )
    # print(data)
    #achaar_it(data, "user_groups_games_playtime.p")
    data = unachaar_it("user_groups_games_playtime.p")
    data = init_3()
    G = create_graph(data)
    partition = community.best_partition(G)  # compute communities
    create_graph_partition_viz(G, partition)

if __name__ == '__main__' :
    #init_3()
    init_2()
    #data = init_3()
    # G = create_graph(data)
    # c = list(k_clique_communities(G, 2))
    # print(len(c))
    