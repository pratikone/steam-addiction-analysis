import networkx as nx
import sql_fetch
def create_graph( given_list ) :

    G = nx.Graph()
    for user_obj in given_list :
        user = user_obj.user_id
        games_id = user_obj.game_id_list
        for game in games_id :
            G.add_edge( user, game )

    return G


if __name__ == '__main__' :
    user_games_list = sql_fetch.init()
    G  = create_graph(user_games_list)
    print(G.nodes())