# Recommending Games, Communities and estimating Gameplay time in Gaming Social Network : A case study of Steam
In this paper, we propose a scalable method for jointly recommending( link prediction) games, users and communities in the context of social gaming network,specifically focusing on the Steam gaming network. This joint framework also allows us to estimate interesting patterns in the Steam graph like which users are likely to be heavy or addicted users based on the communities, friendships and the subset of the games they play, which users in this community are likely to play this  game.

### Authors : Pratik Anand (@pratikone) and Sanket Lokegaonkar (@sloke)


### Summary
Our goal in this paper is to model a specific-types of social networks with the user products and community structure. Specifically in the context of Steam gaming network, we assume that the we have three entities, U (total users), C (total Communities), and G(total Games).     
We model the gaming network as a tripartite network with 3 entities U (total users) , C (total Communities) , and G(total Games). There exists an edge between a user and community entity if user u is part of community(c). There exists an edge between user u and game g, if the user has bought this game. The edge between user u and the game is weighted and the weights models the hours played. The community membership edge is an unweighted graph.     
Given this problem formulation, our objective in this paper is to develop a model which can jointly predict the missing edges between users and communities and predict the weighted missing edges between games and users (indicating interest and hours played.). We also interested in knowing latent connections between the communities and games as well.

### Results

![alt text](https://github.com/pratikone/steam-addiction-analysis/blob/master/doc/users50K.png "Playtime vs users")
  

### How to run
* Requires python 3 to run       
* Uses Pickle version 2 for pickling for maximum compatibility       
Run cmd : ``` python src/graph.py ```      
SQL parameters can be changed in ```src/sql_fetch.py```      
Visualization code is in ```src/visualization.py```      