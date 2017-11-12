import networkx as nx
import numpy as np
import sql_fetch
import pickle
import matplotlib.pyplot as plt

def create_graph( given_list ) :
    G = nx.Graph()
    for user_obj in given_list :
        user = user_obj.user_id
        games_id = user_obj.game_id_list
        if type(games_id) == type([]) :  #if it is a list
            for game in games_id : 
                G.add_edge( user, game )
        else : # if it is an entry
            G.add_edge( user, games_id )
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

    print((len(all_users), len(all_groups), len(all_games)))
    arr = np.zeros((len(all_users), len(all_groups), len(all_games)))
    for entry in final_list :
        user_index = all_users.index(entry.user_id)                     
        group_index = all_groups.index(entry.group_id)
        game_index = all_games.index(entry.game_id)
        arr[user_index, group_index, game_index] = 1
    return arr




if __name__ == '__main__' :
    '''
    Uncomment the lines below to fetch from database 

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
    '''

##############################################################
    final_list = sql_fetch.init()
    arr = get_all( final_list )
    achaar_it(arr, "user_group_game_adj.p")
    arr = unachaar_it("user_group_game_adj.p")
    arr = unachaar_it("user_group_game_adj.p",)
    print(np.shape(arr))

