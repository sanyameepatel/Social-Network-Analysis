#INSTRUCTIONS TO RUN THE CODE:
#Just run the program and there will be choices offered to see the value of the variables obtained in the form of entering 1 or 0 for each choice. Since the variables sometimes will be very large, we try to not print everything.
#In the beginning, a choice will be given to get all the functions for one of the three datasets. I recommend the Bitcoin dataset, solely because the other two are very large and will take a while to run.
##For the last function for each dataset, the user is asked to enter three values to get k-length chains between two nodes. Please make sure the nodes are in the graph to get the accurate result. I recommend printing out isolated nodes and influencers and trying to find k-length chains between an influencer and an isolated node.
#Running it on repl.it does not require taking care of any files since I have added them to this repl. However, in the zip file try running it from the folder the dataset files are in.
#REPL.IT LINK:https://repl.it/@sanyamee/MiniProjectSanyameePatel?language=python3
import csv
import copy
#Graph is a list of adjacency nodes
class Graph:
  def __init__(self):
    self.vertices = {}
    self.indegree = {}
    self.reverse = {}

  def node_init(self, node):
    self.vertices[node]=[]
    self.indegree[node]=0
    self.reverse[node]=[]

  def append_to_list(self,fromV,toV):
    li=self.vertices[fromV]
    li.append(toV)
    self.vertices[fromV]=li

  def append_to_reverse_list(self,fromV,toV):
    li=self.reverse[toV]
    li.append(fromV)
    self.reverse[toV]=li

  def add_edge_undirected(self, fromV, toV):
    if fromV not in self.vertices.keys():
        self.node_init(fromV)
    if toV not in self.vertices.keys():
        self.node_init(toV)
    ##Adding edge fromV - toV
    self.append_to_list(fromV, toV)
    a=self.indegree[toV]
    self.indegree[toV]=a+1
    ##Adding edge toV - fromV
    self.append_to_list(toV, fromV)
    a=self.indegree[fromV]
    self.indegree[fromV]=a+1
    ##Adding reverse edges
    self.append_to_reverse_list(fromV,toV)
    self.append_to_reverse_list(toV,fromV)

  def add_edge_directed(self, fromV, toV):
    if fromV not in self.vertices.keys():
        self.node_init(fromV)
    if toV not in self.vertices.keys():
        self.node_init(toV)
    self.append_to_list(fromV, toV)
    a=self.indegree[toV]
    self.indegree[toV]=a+1
    #adding reverse edge
    self.append_to_reverse_list(fromV,toV)


  def adjacencyList(self):
    if len(self.vertices) >= 1:
      return [str(key) + ":" + str(self.vertices[key]) for key in self.vertices.keys()]
    else:
      return dict()

  def find_influencers(self,num):
      reverse_sorted = sorted(((value, key) for (key,value) in self.indegree.items()), reverse=True)
      influencers= [(t[1],t[0]) for t in reverse_sorted[:num]]
      return influencers

  def bfs_connected_components(self, given_nodes):
      nodes = given_nodes.copy()
      visited, path, largest_connected, comp_index, C, isolated, connected_components=set(), [], [], 0, {}, [], []
      visited.add(nodes[0])
      for start_node in nodes:
          queue, path = [start_node], [start_node]
          visited.add(start_node)
          nodes.remove(start_node)
          while len(queue)!=0:
              start=queue.pop()
              for neighbour in self.vertices[start]:
                  if neighbour not in visited:
                      queue.append(neighbour)
                      visited.add(neighbour)
                      path.append(neighbour)
                      C[neighbour]=comp_index+1
                      if neighbour in nodes:
                          nodes.remove(neighbour)
          connected_components.append(path)
          comp_index+=1
          if len(path) < 3:#based on size of my networks
              isolated.extend(path)
          if len(largest_connected)<len(path):
              largest_connected=path.copy()
          if len(nodes)==1:  #edge case
              node, C[node]=nodes[0], comp_index+1
              connected_components.append([node])
              isolated.append(node)
      return connected_components, largest_connected, C, isolated

  def dfs(self,start,opt,search_stack):
      edges = copy.deepcopy(self.vertices if opt==0 else self.reverse)
      stack = [start]
      path = []
      while stack:
          vertex = stack[-1]
          if vertex in search_stack or vertex in path:
              stack.remove(vertex)
              continue
          if len(edges[vertex])==0 or all(elem in path for elem in edges[vertex]):
              path.append(vertex)
              stack.remove(vertex)
              continue
          curr=min(edges[vertex])
          stack.append(curr)
          #print("removing ", curr, "from", edges[vertex], "::", vertex, " path so far: ", path)
          edges[vertex].remove(curr)
      #print(path)
      return path


  def find_sccs(self, given_nodes):
      nodes = given_nodes.copy()
      all_scc, search_stack, total_nodes=[], [], len(nodes)
      #Initial DFS on graph
      while len(search_stack) < total_nodes:
          node = min(nodes)
          nodes.remove(node)
          if node not in search_stack:
              path=self.dfs(node,0, search_stack)  #do dfs at current_node if not already explored
              search_stack.extend(path)

      #Reverse DFS on graph nodes in order of search_stack
      all_visited=[]
      while len(search_stack) > 0:
          u = search_stack[-1]
          scc_stack = self.dfs(u,1,all_visited)
          all_visited.extend(scc_stack)
          for v in scc_stack:
              if v in self.reverse.keys():
                  del self.reverse[v]
              search_stack.remove(v)
          all_scc.append(scc_stack)
      return all_scc

  def k_len_chains(self,src,dest,k):
       if len(self.vertices[src])>0:
           paths = [[src, a] for a in self.vertices[src]]
       else:
           return [],0
       finalpaths = []
       for i in range(k-2):
           for path in paths:
               newpaths=[]
               #print("MAIN PATH: ", path)
               if len(self.vertices[path[-1]])>0:
                   #print("children of last_node :", self.vertices[path[-1]])
                   for child in self.vertices[path[-1]]:
                       #print("now child ", child, " of ", path[-1])
                       if child not in path:
                           #print("appending", child, " to ", path)
                           newpath = path.copy()
                           newpath.append(child)
                           if newpath not in newpaths and len(newpath)<k:
                               #print("APPENDING PATH : ", newpath, " to ", path)
                               newpaths.append(newpath)
                           if newpath not in newpaths and len(newpath)==k and newpath[-1]==dest:
                               #print("APPENDING PATH : ", newpath, " to ", path)
                               finalpaths.append(newpath)
           #print(i, src, dest, k)
           paths = newpaths.copy()
       #finalpaths = [x for x in finalpaths if len(x) == k]
       return finalpaths, len(finalpaths)


def test_routine(G):
    all_nodes = list(G.vertices.keys())
    choice = int(input("Do you want to find influencers for this graph? Enter 1 for yes and 0 for no.\n"))
    if choice==1:
        choice=None
        influencers  = G.find_influencers(100)
        print("Influencers: (top 100) ", influencers)

    choice = int(input("Enter 1 if you want to find connected components and 0 if you don't.\n"))
    #To test strongly connected components
    if choice ==1:
        choice=None
        connected_components, largest_connected, C, isolated = G.bfs_connected_components(all_nodes)
        print("Number of connected components: ", len(connected_components))
        print("Number of isolated nodes: ", len(isolated))
        print("Length of largest connected component", len(largest_connected))
        choice = int(input("Would you like to see the nodes in the largest connected component? Enter 1 if yes, 0 if no.\n"))
        if choice==1:
            choice=None
            print("Largest connected component: \n",largest_connected)
        choice = int(input("Would you like to see the len of each component and their starting node? Enter 1 if yes, 0 if no.\n"))
        if choice==1:
            choice=None
            print("start : length")
            for comp in connected_components:
                print(comp[0],len(comp))

    choice = int(input("Enter 1 if you want to find strongly connected components and 0 if you don't.\n"))
    if choice ==1:
        choice = None
        strongly_connected = G.find_sccs(all_nodes)
        print("Number of strongly connected components: ", len(strongly_connected))

    choice = int(input("Enter 1 if you want to find k-length chains in the graph between two nodes and 0 if you don't.\n"))
    if choice ==1:
        choice = None
        node1,node2,steps = int(input("Enter two nodes from the graph and the value of k. \nExample input if you want 4-length  chains from 1 to 3 will be: 1 3 4\n"))
        klenpaths, kpaths = G.k_len_chains(node1,node2,steps)
        print("PATHS : ", klenpaths, "\nNumber of paths : ", kpaths)


def citation_test():
    ###CITATION DATASET
    phy=open('Cit-HepTh.txt',"r")
    phyG=Graph()
    edges =0
    for x in phy:
      line = phy.readline()
      edge = line.split()
      if len(edge)!=0:
          edges+=1
          fromNode=int(edge[0],10)
          toNode=int(edge[1],10)
          phyG.add_edge_undirected(fromNode,toNode)
    phy.close()
    print("\nCITATION")
    test_routine(phyG)


def github_test():
    ###GITHUB DATASET
    gitG=Graph()
    with open('musae_git_edges.csv') as git:
        gitReader = csv.reader(git, delimiter=',')
        edges=0
        for edge in gitReader:
            edges+=1
            fromNode=int(edge[0],10)
            toNode=int(edge[1],10)
            gitG.add_edge_undirected(fromNode,toNode)
    git.close()
    print("\nGITHUB")
    test_routine(gitG)


def bitcoin_test():
    ###BITCOIN DATASET
    bitG=Graph()
    with open('soc-sign-bitcoinalpha.csv') as bit:
        bitReader = csv.reader(bit, delimiter=',')
        edges=0
        for edge in bitReader:
            edges+=1
            fromNode=int(edge[0],10)
            toNode=int(edge[1],10)
            bitG.add_edge_directed(fromNode,toNode)
    bit.close()
    print("\nBITCOIN")
    test_routine(bitG)

def main():
    print("The datasets we have are \n1.Collaboration network of Arxiv High Energy Physics Theory. ",
          "\nType: Undirected Nodes:9,877 Edges:25,998",
          "\n\n2.Social network of Github developers \nType:Undirected Node:37,700	Edges:289,003",
          "\n\n3.Bitcoin Alpha web of trust network \nType: Weighted, Signed, Directed, Temporal Nodes:3,783 Edges:24,186 \n\n\n")
    dset=int(input("Enter 1,2 or 3\n"))
    if dset==1:
        citation_test()
    elif dset==2:
        github_test()
    elif dset==3:
        bitcoin_test()
    else:
        print("invalid choice.")

if __name__ == "__main__":
    main()
