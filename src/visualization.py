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

def create_graph_partition_viz(G, partition) :
    # plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(G)  # compute graph layout
    plt.axis('off')
    colors = ['r','g','b','k','c','y','r','g','b','k','c','y','m', 'r','g','b','k','c','y']
    comms = {}
    for node, comm in partition.items() :
        if comm not in comms : 
            comms[comm] = set()
        comms[comm].add(node)
    print(len(comms.keys()))
    for key in comms :
        print(key, len(comms[key]))
        nx.draw_networkx_nodes(G, pos, nodelist = list(comms[key]) ,node_size=10, node_color= colors[key])
    nx.draw_networkx_edges(G, pos, alpha=0.1)
    plt.show(G)
    