# Recommending Games, Communities and estimating Gameplay time in Gaming Social Network : A case study of Steam
Gaming communities like Steam are one of the less-studied social networks. We intend to study this network from the
point of relationship between friendship, communities and game ownership having an influence on addiction of gam-
ing and ability to make predictions of game ownership and playtime, leading to prediction of addiction. In this project, We propose JFactor, a joint matrix factorization approach, which predicts game-play times and recommended communities for users jointly for the Steam network.We optimize our method by coupling the factorization from
the derived community and game co-occurrence matrix. We perform extensive experiments to compare our proposed
joint matrix factorization model and report findings in the paper.

[Paper](https://github.com/pratikone/steam-addiction-analysis/blob/master/doc/LOKEGAONKAR-ANAND-final.pdf)     
[Slides](https://github.com/pratikone/steam-addiction-analysis/blob/master/doc/slides.pdf)

### Authors : Pratik Anand (@pratikone) and Sanket Lokegaonkar (@sloke)


### Summary
Our goal in this paper is to model a specific-types of social networks with the user products and community structure. Specifically in the context of Steam gaming network, we assume that the we have three entities, U (total users), C (total Communities), and G(total Games).     
We model the gaming network as a tripartite network with 3 entities U (total users) , C (total Communities) , and G(total Games). There exists an edge between a user and community entity if user u is part of community(c). There exists an edge between user u and game g, if the user has bought this game. The edge between user u and the game is weighted and the weights models the hours played. The community membership edge is an unweighted graph.     
Given this problem formulation, our objective in this paper is to develop a model which can jointly predict the missing edges between users and communities and predict the weighted missing edges between games and users (indicating interest and hours played.). We also interested in knowing latent connections between the communities and games as well.

### Results

![](https://github.com/pratikone/steam-addiction-analysis/blob/master/doc/users50K.png "Playtime vs users")
![](https://github.com/pratikone/steam-addiction-analysis/blob/master/doc/for50kusers.PNG "Playtime by genre")    
![](https://github.com/pratikone/steam-addiction-analysis/blob/master/doc/pca_users.png "PCA - Users")    
![](https://github.com/pratikone/steam-addiction-analysis/blob/master/doc/pca_games.png "PCA - Games")    
![](https://github.com/pratikone/steam-addiction-analysis/blob/master/doc/pca_communities.png "PCA - Communities")        
### How to produce the network 
* Requires python 3 to run       
* Uses Pickle version 2 for pickling for maximum compatibility       
* Install the SQL database as mentioned below    
Run cmd : ``` python src/graph.py ```      
SQL parameters can be changed in ```src/sql_fetch.py```      
Visualization code is in ```src/visualization.py```      

### How to train your dragon(model)!
#### Requirements
* Requires python 2
* Pickle version 2
* Matlab
* [TensorLab 2016 Version](https://www.tensorlab.net)
* [Data](https://steam.internet.byu.edu)

#### Steps
1. Download the steam.sql from the data link
2. Install MySQL instance and load the database too it
3. Change user-name, password to the assigned database credentials
4. Run ```python model/extract.py sample_size``` Creates multiple files. Current dir becomes dataset_path.
5. Change the directory paths in train.sh
5. Run ```python model/script.py --dataset dataset_path --max_iter maximum_iterations --setting model_setting --rank rank ``` .
   Results should contain the MSE Error and the Ranking Metrics output.
