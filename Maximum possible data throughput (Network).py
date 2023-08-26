import math 

def maxThroughput(connections, maxIn, maxOut, origin, targets):

    """
    Function Description : This function returns the maximum amount of flow that can be sent from origin to targets. It uses the Ford-Fulkerson method by 
                           finding augmenting paths in the residual network. The process of finding augmenting path is implemented using breadth-first search (BFS).
                           It will continue to find a path while adhering to capacity constraints and flow conservation and update edges in residual network after 
                           until there's no more augmenting path. 
    

    Approach Description : Since we only need to return the maximum flow, there is no need to update the actual network, therefore only the residual network 
                           needs to be created. In respect of flow conservation where sum of the incoming flow should be equal to the sum of the outgoing flow 
                           at every data centre vertex, the smallest allowed data the data centre can process is used instead, which is the smallest out of 
                           maxIn and maxOut. For origin, only outgoing data matters and for targets only incoming data matters so they are set accordingly.
                           + Capacity = amount of data the data centre can process

                           In cases where there are more than 1 target, a supersink is created to connect all targets to one. The edges connecting to 
                           supersink have a throughput according to target's capacity as that will be the maximum flow that's allowed to flow from targets.

                           To add edges in residual network, forward edges are set to maximum throughput for that connection to indicate the amount of data that 
                           can still be passed while backward edges are set to 0 as there is no flow to undo yet. Due to the possibility of a connection existing 
                           when a backward edge in the direction of the connection is already created, we have to replace the backward edge. In order to prevent
                           creating extra edges, a caught boolean is added.
                           + Caught = current connection already has a backward edge created in it's place

                           After initialisation of residual network, Ford-Fulkerson is used to find maximum flow in the created residual network. The concept 
                           of Ford-Fulkerson is where it continues to find an augmenting path, update each vertex and edge involved until no path is found.

                           If an augmenting path is found, it means there is still a path to increase the total flow. The algorithm used to find path is 
                           implemented using BFS to ensure it runs in O(D + C). A BFS involves using a queue to discover vertices. During discovery, it will 
                           check the edge's throughput and vertex's capacity to adhere to the constraints and ensure that there is still available flow.
                           In the meantime, it will also track each vertex's previous edge to make udpating augmenting paths easier.

                           After target is reached in BFS, backtracking is performs to check for bottleneck which is the flow allowed throughout path. To get
                           bottleneck, the smallest capacity out of all vertices and smallest throughput out of all edges involved in path is chosen.

                           Now that we have the path, we traverse augmenting path to add flow. This includes adding bottleneck to backward edge and reducing 
                           forward edge by bottleneck. This process it then repeated while adding it's bottleneck until no paths are found meaning maximum flow 
                           is achieved. 
                           
                            Time complexity explanation :
                                O(D + C + T) - from initialising residual graph (creating vertex, creating edges, join targets to one final vertex)
                                O(D + C + D) - from finding augmented path (Running BFS where worst case is each vertex is visited once and each edge is visited once, 
                                           backtracking is only ran once and D is from reversing the path)
                                O(D + C + (F * (D + C))) -> O(DC^2) - from ford fulkerson (finding augmented path, finding augmented path until there's no more path)

                            Aux space complexity Explanation:
                                O(D) - storing data centres (vertex) in residual graph
                                O(C) - storing connection channels (edges) in residual graph
                                O(D) - using Queue to store data centres (vertex) while performing BFS
                                O(C) - path to store paths for each augmented path iteration

                            Input : 
                                connections - a list of tuples with each edge's from vertex, to vertex and maximum throughput allowed for the communication channel
                                maxIn - the maximum incoming throughput each data center can accept
                                maxOut - the maximum outgoing throughput each data center can accept
                                origin - a positve integer of indicating the starting vertex
                                targets - a list containing targets that has to be reached from origin

                            Output :
                                bottlecaptotal - an int showing the maximum flow allowed from origin to targets 

    Time complexity : O(D * C^2) where D is the number of data centres and C is the number of connections
    Aux space complexity : O(D + C), where D is the number of data centres and C is the number of connections

    """
    # create a residual network from input
    graph = Graph(connections, maxIn, maxOut, origin, targets)

    # # perform Ford Fulkerson with residual network already created
    bottlecapTotal = graph.ford_fulkerson()

    return bottlecapTotal
    
class Graph:
    """
    Class Description: A residual graph is created to represent  Data centres and Connections
                        vertices: a list of vertices representing Data Centres
                        num_of_vertices : the total number of vertices (but it starts from 0 so the largest id is num_of_vertices - 1)
                        added_target : to indicate if an extra vertex is added to join multiple targets together
                        start : the origin
                        target : the target (if there's multiple it will then be updated to supersink)
    """
    def __init__(self, connections, maxIn, maxOut, origin, target):
        """ 
        Initialising a residual graph and modifying it to solve the problem 

        Time complexity : O(D + C + T), where D is number of data centres, C is number of connections and T is number of targets 
        Aux space complexity : O(D), where D is number of data centres
        """
        self.vertices = []
        self.num_of_vertices = len(maxIn)
        self.added_target = False
        self.start = origin
        self.target = target[0]

        # create a empty vertices Adjacency List 
        self.vertices = [None] * self.num_of_vertices

        # Flow Conservation - O(D), where D is number of data centres
        for vertex in range(self.num_of_vertices): 
            # If vertex is origin, only maximum flow going out matters
            if vertex == self.start:
                self.vertices[vertex] = Vertex(vertex, maxOut[vertex])
            # If vertex is target, only maximum flow going in matters
            elif vertex in target:
                self.vertices[vertex] = Vertex(vertex, maxIn[vertex])
            # For others, whichever smallest from maxOut and maxIn is picked
            else:
                if maxIn[vertex] < maxOut[vertex]:
                    self.vertices[vertex] = Vertex(vertex, maxIn[vertex])
                else:
                    self.vertices[vertex] = Vertex(vertex, maxOut[vertex])

        # if more than one target, a final vertex has to be created
        if len(target) > 1:
            self.added_target = True
            self.num_of_vertices += 1
            self.vertices.append(Vertex(self.num_of_vertices-1, math.inf))
            self.target = self.num_of_vertices-1


        # create edges for residual graph - O(C), where C is number of connections
        for edge in connections:
            # check if edge already exist
            index = 0             
            caught = False               ### caught is for cases where the connection already has a backward edge initialised
            # In such a case, we have to replace the previously initialised backward edge with current connection
            for opposite_edge in  self.vertices[edge[0]].edges:
                if opposite_edge.v == edge[1]:
                    opposite_edge = Edge(edge[0], edge[1], edge[2] )
                    caught = True
                index += 1

            # only proceed to create forward and backward edge if connection does not already exist
            if caught != True:
                # Add the going edges (the available flow )
                self.vertices[edge[0]].add_edges(edge[0], edge[1], edge[2] )
                # to initialise flow
                self.vertices[edge[1]].add_edges(edge[1], edge[0], 0 )  
           
        # If a final vertex added, need to add edges to join all targets to that final vertex - O(T)
        if self.added_target:
            for i in range(len(target)):
                targetVertex = target[i]
                self.vertices[targetVertex].add_edges(targetVertex, self.num_of_vertices-1, self.vertices[targetVertex].capacity )
                self.vertices[self.num_of_vertices-1].add_edges(self.num_of_vertices-1, targetVertex, 0 )

    def aug_path(self):
        """
        Function description : To find an augmented path from origin to target. If no path is found, an empty list is returned. 
                               Implemented using BFS.

        Time complexity : O((D + C) + D), where D is number of Data Centres and C is number of Connections
        Aux space complexity : O(D + D + D), where D is number of Data Centres (Queue + parent + visited)
        """
        
        queue = Queue()                           ### Queue is used to perform BFS when traversing the graph
        parent = [-1] * self.num_of_vertices      ### A list to store the parent vertex of each vertex in the augmented path
        visited = [False] * self.num_of_vertices  ### To indicate if a vertex is visited

        # Starting with origin, it is visited and add it to queue to ensure BFS starts from origin
        visited[self.start] = True
        queue.enqueue(self.start)

        # Checks if origin still has maxOut capacity, if not return empty path
        if self.vertices[self.start].capacity == 0:
            return [],0

        # continues traversing the graph until queue is empty
        while queue.length != 0:
            # since it's implemented using a queue, dequeue will serve the first item added resulting in BFS
            vertex = queue.dequeue()

            # If the destination vertex is found, backtrack from the destination to the source
            if vertex == self.target:
                # Initialisation for backtracking
                bottlecap = math.inf                      ### bottlecap is the largest flow allowed in the entire path
                path = []                                 ### path is the augmented path 
                current = self.target 
                # iterating all vertices in the path
                while current != -1:
    
                    # check capacity for bottlecap, reduce bottleneck if capcity smaller
                    if self.vertices[current].capacity < bottlecap:
                        bottlecap = self.vertices[current].capacity

                    # check throughput for bottlecap, we do not run this for origin because origin has no parent
                    if current != self.start:
                        # checking the edge connecting parent to current vertex
                        edge = self.vertices[current].previous
                        # reduce bottleneck if throughput smaller
                        if  edge.throughput < bottlecap:
                            bottlecap = edge.throughput

                    path.append(current)
                    current = parent[current]
                
                # If a path has only one vertex, it's not a valid path
                if len(path) <= 1:
                    return [],0

                # Because we performed backtracking, the path is in reverse order - O(D)
                path.reverse()

                # update origin's capacity too since it's not updated in backtracking
                self.vertices[self.start].capacity -= bottlecap

                return path, bottlecap

            # Get all adjacent vertices of the dequeued vertex.
            # If an adjacent vertex has not been visited, mark it as visited, set its parent, and enqueue it.
            for edge in self.vertices[vertex].edges:

                if not visited[edge.v]:
                    # If it's 0, it shouldnt pass
                    if edge.throughput != 0 :
                        
                        if self.vertices[edge.v].capacity != 0 :
          
                            visited[edge.v] = True
                            parent[edge.v] = vertex

                            # to remember the previous edge for the vertex
                            self.vertices[edge.v].previous = edge

                            queue.enqueue(edge.v)
                    
        # If the destination vertex is not reachable from the source, return an empty path
        return [],0

    def ford_fulkerson(self):
        """
        Function description : Continues looping until there is no path found. After every path, residual graph's forward and backward edges are edited based on
                               bottleneck obtained from path. All the bottlenecks are then combined to get maximum flow.
        
        Time Complexity : O((D + C) + F * (D + C)) -> O(DC^2) where D is number of data centres, C is number of connections and F is the maximum flow
        """
        
        # Get the first augmented path and it's bottlecap - O(D + C)
        path, bottlecap = self.aug_path()
        # Initialise total bottlecap / maximum flow to target
        bottlecaptotal = 0

        # Continue looping as long as there's a path available from origin to target - O(F * (D + C)) -> O(FC) -> O(DC^2)
        # By the implementation of BFS, we have secure the time complexity of O(DC^2)
        while path != []:

            # Each time a path is ran, we have to go through all the vertices and update edges for each edge through the path - O(1)
            for i in range(len(path)-1):
                
                # reducing available capacity by throughput
                self.vertices[path[i+1]].capacity -= bottlecap

                # modifying forward edge by throughput, reduce available flow
                self.vertices[path[i+1]].previous.throughput -= bottlecap

                # modifying backward edge by throughput, to allow it to be possibly undone in the future
                for edge in self.vertices[path[i+1]].edges:
                    if edge.v == path[i]:
                        edge.throughput += bottlecap

            # current bottlecap is the max flow reaching target for the current path
            # Adding the bottlecap for every path will give us the total maximum flow to all targets
            bottlecaptotal += bottlecap

            # Continues to get it's augmented path : O(D + C)
            path, bottlecap = self.aug_path()

        return(bottlecaptotal)
        
class Vertex:
    """
    Class Description: A Vertex can be used to represent the data centres in a graph
                       id : to identify the data center
                       capacity : the minimum amount of data this data centre can process
                       edges : the edges coming out from the vertex
                       previous : the edge connecting to the data center to be used in the current augmented path
                    
    """
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.edges = []
        self.previous = 0

 
    def __str__(self):
        """ When print() is used on a vertex, this provides an organised return string"""
        if self.hasPassenger == True:
            return_string = "Vertex " + str(self.id) + " with passenger with edges" + str(self.edges) + "\n" + " From Source: " + str(self.MinFrmStart)
        else:
            return_string = "Vertex " + str(self.id) + " no passenger with edges" + str(self.edges) + "\n" + " From Source: " + str(self.MinFrmStart)
        return return_string
    
    def add_edges(self,frm_vertex, to_vertex, throughput):
        """ adds an edge from Edge Class to the vertex's edges list"""
        self.edges.append(Edge(frm_vertex, to_vertex, throughput))

class Edge:
    """
    Class Description: An edge can be used to represent a connection in the Graph
                       u : From data center / vertex
                       v : To data center / vertex
                       throughput : the amount of throughput allowed for the connection / edge
    """
    def __init__(self, u, v, throughput):
        """ Initialisation of an edge """
        self.u = u
        self.v = v
        self.throughput = throughput

    def __str__(self):
        """ When print() is used on an edge, this provides an organised return string"""
        return_string =  "From: " + str(self.u) + " To: " + str(self.v) + " Throughput: " + str(self.throughput) 
        return return_string
    
class Queue:
    """
    Class description: A simple Queue class implemented using an array as the underlying data structure
                       It follows a FIFO principle meaning the first item to be added is the first to be poppped.
                       This data structure is used to implement a Breadth First Search concept for finding augmented path.
    """
    def __init__(self):
        """ Initialisation of the queue using an empty array"""
        self.items = []
        self.length = 0

    def enqueue(self,item):
        """ Append item to the queue """
        self.length += 1
        self.items.append(item)
    
    def dequeue(self):
        """ Serves the first item in the queue"""
        if self.length == 0:
            return 0
        self.length -= 1
        return self.items.pop(0)

    def __str__(self):
        """ To print the list of items in queue"""
        return str(self.items)


if __name__ == "__main__":
    pass