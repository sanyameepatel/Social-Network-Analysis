# Social-Network-Analysis

Datasets chosen

Bitcoin Alpha trust weighted signed network
This is who-trusts-whom network of people who trade using Bitcoin on a platform called Bitcoin Alpha. Since Bitcoin users are anonymous, there is a need to maintain a record of users' reputation to prevent transactions with fraudulent and risky users. Members of Bitcoin Alpha rate other members in a scale of -10 (total distrust) to +10 (total trust) in steps of 1. The graph is a weighted signed directed network that contains 3,783 nodes and 24,186 edges. Each line has one rating with the following format: [SOURCE, TARGET, RATING, TIME]

GITHUB Social Network
A large social network of GitHub developers which was collected from the public API in June 2019. Nodes are developers who have starred at least 10 repositories and edges are mutual follower relationships between them. The vertex features are extracted based on the location, repositories starred, employer and e-mail address. The task related to the graph is binary node classification - one has to predict whether the GitHub user is a web or a machine learning developer. This target feature was derived from the job title of each user. This undirected graph contains 37,700 nodes and 289,003 edges. We only use the edges given to us.

High Energy Physics Theory Citation Network
Arxiv HEP-TH (high energy physics theory) citation graph is from the e-print arXiv and covers all the citations within a dataset of 27,770 papers with 352,807 edges. If a paper i cites paper j, the graph contains a directed edge from i to j. If a paper cites, or is cited by, a paper outside the dataset, the graph does not contain any information about this. The data covers papers in the period from January 1993 to April 2003 (124 months). It begins within a few months of the inception of the arXiv, and thus represents essentially the complete history of its HEP-TH section. This graph contains 27,770 nodes and 352,807 edges. 

REPL.IT Link to Code: 
https://repl.it/@sanyamee/MiniProjectSanyameePatel?language=python3



Algorithmic Choices

1.	Data Structure
For milestone 1, the graph given is supposed to be encoded as a list of edges where each edge is a pair of nodes. However, storing each edge will require a lot of space. Hence, an adjacency list data structure is used to store the graph. A dictionary data structure is used to make search and insertion of O(1) time complexity.

2.	Finding Influencers
The solution to this was to record the indegree of each node. While the graph was being encoded, the indegree was recorded as a property of the graph. The indegree of a node is incremented by 1 when it appears in the ‘to’ part of an edge. Due to this, we only need to sort the nodes by indegree. The default sort in python is used. Python uses a Timsort algorithm which is of complexity O(n.log n) in the average and worst case. In the best case, it runs in linear time.

3.	Finding Isolated Nodes
Connected components were obtained by doing BFS on the graph. If the size of the connected component is 1 to 3, which means it is either not connected to any node or connected to only two nodes, it becomes an isolated node. Even though we have edges in the graph, there are isolated nodes because some nodes only have outgoing edges and no ingoing ones. Hence, there may not be any isolated nodes in undirected graphs. The complexity of BFS is O(V+E) on an adjacency list.

4.	Finding Strongly Connected Components
Kosaraju’s Algorithm is used to find SCCs by doing a DFS on the graph and then doing a DFS on the reversed edges of the graph. This would only require O(V+E) time since we are storing the reverse edges in the initialization process itself. A better algorithm that requires only a single is Tarjan’s algorithm but maintaining the values for the disc would have been a little more complex. 

5.	Finding k-length chains between two nodes
Given two nodes (source and destination) and the value of k, we add all the neighbours of ‘source’ to different lists, initializing the possible paths, then we keep adding neighbours to those paths until the size of paths is k. If a neighbor has n neighbours we make n new lists and add those to possible paths. We only keep the paths that have the destination in the last node of the path. In the worst case where the nodes are very dense, we would have to make n^k lists. However, this is not the case with our datasets.
