import networkx as nx
import sql_fetch
import pickle

def create_graph( given_list ) :
    G = nx.Graph()
    for user_obj in given_list :
        user = user_obj.user_id
        games_id = user_obj.game_id_list
        for game in games_id :
            G.add_edge( user, game )
    return G


def add_edges_friends( G, friends_list ) :
    for entry in friends_list :
        G.add_edge( entry.user_id_a, entry.user_id_b )   # TODO : add weight here , if needed

def achaar_it( G, file_name ) :  #pickle it, pickle = achaar in Hindi
    try :
        pickle.dump( G, open( file_name, "wb" ) )
    except pickle.PickleError as e :
        print("Could not pickle due to error ", e)

def unachaar_it( file_name) : #unpickle it, pickle = achaar in Hindi
    try :
        G = pickle.load( open( file_name, "rb" ) )
        return G
    except pickle.PickleError as e :
        print("Could not pickle due to error ", e)
    return None



if __name__ == '__main__' :
    friends_list, user_games_list = sql_fetch.init()
    G  = create_graph(user_games_list)
    add_edges_friends(G, friends_list)
    print(G.number_of_edges())
    achaar_it(G, "achaar.p")
    G = unachaar_it("achaar.p")
    print(G.number_of_edges())


