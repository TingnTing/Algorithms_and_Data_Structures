import math  # to use inf

def optimalRoute(start, end, passengers_list, roads):
    """
    Function description : This function returns a list of vertices to pass through to get to the destination edge with the least total accumulated weights.
                           This function uses Dijkstra's concept to find the shortest path to each vertex and after getting the shortest path for each vertex.
                           We can trace back from the end vertex to the start using information obtained by dijkstra where it provides the previous weight and position.
    

    Approach description : Because the original graph provided by the problem results in edges having 2 weights, one solo and one carpool time. We can simplify it
                           for dijkstra by making an extra copy of vertices in the same list. This makes the vertices list twice the size 
                           which gives an auxillary space : O(2L) = O(L). 

                           Theoretically, it is possible to have any vertex where when the driver already has a passenger in the car, it's just a matter of reachability.
                           On the contrary, it is impossible to not fetch a passenger when the vertex already has a passenger (vertex is in passenger_list).
                           Therefore, in the graph's vertices list, True means a passenger is present, False means it's solo. For the first section of the list, all
                           True exists but only for vertices where it's not in passenger_list, a vertex with False is able to exist and it is places at the back section
                           after minusing the original set of vetices and placing it in its index position.

                           The edges are added which takes O(R) time because there are R edges to be added. There are three cases for adding edges.
                           All carpool edges are added but only solo edges where it is not coming from a vertex in passenger list is added.

                           This way we have a graph with all edges only having one weight.

                           Dijkstra's algorithm is then ran from the start vertex to update the each vertex's (MinFrmStart) which is the smallest distance
                           from starting vertex. 
                           
                           Discovered is stored in a heap to know which is the vertex with the smallest weight we should examine next. Everytime a vertex is discoverec
                           but not processed it is added to the heap. 

                           The while loop until discovered is empty costs O(R log 2L), O(log 2L) is from extractMin heap function and O(R) because we are looping each edge.
                           At every loop, adjacent edges are checked for the current vertex and for every edge we can find the weight needed to reach it's adjacent vertex
                           by adding the current vertex's MinFrmStart with the weight and update it if a smaller weight can be found. We can then add the adjacent vertices to the heap.

                           Dijkstra updates all the vertices with the correct minutes taken from start and the previous vertex to get that weight.
                           Back tracing be done to get the path need for the optimal solution.It starts from the final vertex and following each pervious vertex up till the starting vertex.
                           Since the tuples are in reverse. We can reverse it by popping off the stack to get the final path.
                           Back tracing takes O(2L) as the worst case is passing through all the locations.

                            Time complexity Explanation:
                                O(R + P + L + R) - from graph initialization ( get_largest_vertex, creating boolean list, adding locations, adding roads)
                                O(log L + O((L + R) log L)) -  from dijkstra ( adding starting vertex, edge relaxation with add involving rising)
                                O(L + L) - from back tracing ( tracing back every vertex, reversing stack)

                            Aux space complexity Explanation:
                                O(L) - storing passenger_list in boolean list form
                                O(L) - storing vertices in a graph
                                O(R) - Min Heap to store path
                                O(R) - list to store output path

                        Input : 
                                start - starting vertex
                                end - destination vertex
                                passenger_list - vertices where no passengers can't exist
                                roads - list of tuples with edges information and weight
                        Output :
                                a list containing vertices to pass through to get optimal solution


    Time complexity : O(L log L) where R is the number of edges and L is the number of vertices
    Aux space complexity : O(L + R) where L is the number of locations and R is number of roads


    """

    # creates a graph object by calling graph class
    graph = Graph(start, end, passengers_list, roads)

    # runs dijkstra to update all vertices in the graph with the shortest path to get to each them - O(R log L)
    graph.dijkstra(graph.start)
    
    # using the info from dijsktra we backtrack from the end by using each previous vertex to get the final path - O(L)
    path = graph.traceBack(start,end)

    min_dist = graph.vertices[end].MinFrmStart  ### to check total time taken
    return path
    
class Graph:
    """
        Class Description: A graph is created to represent the map of the Location and roads
                           start: the starting location
                           end: destination 
                           vertices: a list of vertices representing Locations
                           passenger_list: input passengers_list but representing in a list form with boolean
        """

    def __init__(self, start, end, passengers_list, roads):
        """ 
        Initialising the graph and modifying it to solve the problem with the concept of splitting vertices into two parts in a list

        Time complexity : O(R + P + L + R), where P is number of Passengers, L is number of Locations and R is number of roads
        Aux space complexity : O(L) + O(L), where L is number of Locations
        """
        self.start = start
        self.end = end
        self.vertices = []
        self.passengers_list = passengers_list

        # Get the largest vertex, + 1 to include vertex 0 - O(R)
        self.num_of_vertices = get_largest_vertex(roads)+ 1
    
        # turn passenger_list (input) into a list of True and False for O(1) access later - O(L) time complexity and aux space complexity
        self.passengers_list = [False] * (self.num_of_vertices + 1)

        for location in passengers_list:                   # O(P) because looping every passenger_list item and replacing item takes constant time
            self.passengers_list[location] = True
            
        # create a empty vertices Adjacency List with double the number of vertices, this is because the front num_of_vertices are to store vertex where passengers are on board
        self.vertices = [None] * ((self.num_of_vertices*2))

        # Assign Vertex object to the vertices list in graph - O(L)
        # for every vertex a route where there is a passenger is possible, what matters is it's reachability, it can exist but not be reachable from the start
        for vertex in range(self.num_of_vertices):
            self.vertices[vertex] = Vertex(vertex, True)
            # If the vertex already has a passenger, a Vertex without passenger is not possible, this makes only vertices without passengers waiting have a vertex where there are no passengers
            # If it is the destination vertex, it doesn't matter if it's True or False but we can just let one vertex exist which is True even when there are no passengers
            if self.passengers_list[vertex] == False and vertex != self.end:
                self.vertices[vertex+ self.num_of_vertices] = Vertex(vertex, False)


        # adding edges to the vertices - O(R) since all operations inside loop takes constant time, including add_edges
        for road in roads:

            # only pick roads where it is not coming out from destination as it redundant to add edges coming out from destination
            if road[0] != self.end:
                from_vertex = road[0]
                to_vertex = road[1]

                # Add edge for with passengers, an edge always exist
                from_vertexPass = [from_vertex,True]
                # add_adges is a function in Vertex class where it appends an edge (from vertex, to vertex, time needed)
                # road[3] because if vertex True means there's a passenger so we can use carpool lane
                self.vertices[from_vertex].add_edges(from_vertexPass, [to_vertex, True], road[3])

                # If a vertex can exist without passengers, we have to add the edge where the solo lane is used
                if self.passengers_list[from_vertex] == False:
                    from_vertexPass = [from_vertex,False]
                    # Two cases can exist
                    # Case #1 : It is going from a vertex without passengers to a vertex in passenger_list
                    if to_vertex == self.end or self.passengers_list[to_vertex]== True:
                        self.vertices[self.num_of_vertices + from_vertex].add_edges(from_vertexPass, [to_vertex, True], road[2])
                    # Case #2 : It is going from a vertex without passengers to another vertes without passengers
                    else:
                        self.vertices[self.num_of_vertices + from_vertex].add_edges(from_vertexPass, [to_vertex, False], road[2])
        
        

    def dijkstra(self, starting_vertex):
        """"
        Function description : This function updates all the vertices's weight from start and also noting it's previous vertex to get to that weight
        
        Approach description : It uses a BFS concept where it goes to all vertices and picking the next smallest vertex to discover next using a Min Heap.
                               From each vertex it checks the adjacent vertex to see if a shorter minutes taken can be found. If yes, it's MinFrmStart and previous 
                               will be updated
                               
        Time complexity: O(R log L), where L is number of locations
        Aux space complexity: O(L), where L is number of locations

        """
        # since in adjacent list of vertices, the starting vertex wihout passenger starts at the second part of the list after all the vertices with passengers
        starting_Vertex = self.vertices[starting_vertex + self.num_of_vertices]

        # Initialization of starting vertex
        starting_Vertex.MinFrmStart = 0
        starting_Vertex.previous = 0

        # a Min Heap to store vertex's distance from the starting vertex and the Vertex itself
        discovered = MinHeap()
        # adding the starting vertex into Heap - (log L)
        discovered.add(0, starting_Vertex)


        # Stops when all Locations are discovered  - O((L + R) log L) because each location is visited once and each edge is relaxed once
        while discovered.count > 0:
            # extractMin function from heap gets the smallest distance from Heap, this is to ensures we always continue with the 
            # smallest possible edge to pass at every iteration - O(log L) due to sinking
            [distFromStart, curr_Vertex] = discovered.extractMin()

            adjacentEdges = curr_Vertex.edges

            # Edge Relaxation, checks all edges and if a shorter time is found to it's neighbours, it updates the MinFrmStart of the neighbours
            # Total complexity = O(R log L)
            # Explanation : This loops O(R) time because all the roads has to be examined once and each location's MinFrmStart 
            #               is only updated once. 
            #               O(log L) is because the inner operations of min heap, such as add that contains rising cost O(log L)
            for edge in adjacentEdges:

                # Check if the vertex we are going to has passenger, if yes, it's vertex position in self.vertices is the front part, else is the second
                if edge.v[1] == True:
                    to_Vertex = self.vertices[edge.v[0]]
                else:
                    to_Vertex = self.vertices[edge.v[0] + self.num_of_vertices]

                edgeWeight = edge.w
                
                # if we can reach to_vertex with a shorter time with the current vertex + the time taken to get to to_vertex
                if to_Vertex.MinFrmStart > curr_Vertex.MinFrmStart + edgeWeight:
                    # we can update it together with the position
                    to_Vertex.MinFrmStart = curr_Vertex.MinFrmStart + edgeWeight
                    to_Vertex.previous = curr_Vertex
        
                    # Add entry to min-heap with an updated distance
                    discovered.add(to_Vertex.MinFrmStart, to_Vertex)
              
    def traceBack(self, start, end):
        """
        Function description: This function returns a list of vertices needed to pass through to get to the end vertex from the start.

        Approach description: Since we have the shortest minutes needed to get to each vertex from Dijkstra. We can trace back from 
                              the end vertex by following the vertex's previous vertex until we reach the starting vertex.

                              Worst case is we have to pass by every location twice before getting to end vertex which cost O(2L).
                              Reversing the stack to get output path also takes O(2L) in the worst case

                              The stack takes up O(L) space and output list takes O(L)
        
        Time complexity: O(L), where L is the number of Locations
        Aux space complexity: O(L), where L is the number of Locations
        """
        # Initialisation of output path and the temporary pathStack to be reversed later
        path = []
        pathStack = Stack()

        # destination vertex always assigned to the first section in Graph implementation
        end_Vertex = self.vertices[end] 
        # start vertex has no passengers so it's the back section for no passengers
        start_Vertex = self.vertices[self.num_of_vertices + start]
        
        # pushed the last vertex to stack because it is part of the path
        pathStack.push(end_Vertex.id)

        # get previous vertex by previous from the current vertex
        previous_Vertex = end_Vertex.previous 
        pathStack.push(previous_Vertex.id)

        # continue until we reached the start_vertex - the worst case is needing to go through all vertices once, a vertex can only appear at most twice
        while previous_Vertex != start_Vertex:
            previous_Vertex = previous_Vertex.previous
            pathStack.push(previous_Vertex.id)
        
        # pop all items from stack to a list to reverse the back tracked paths - O(2L)
        for i in range(Stack.getSize(pathStack)):
            item = pathStack.pop()
            path.append(item)

        return(path)
        
class Vertex:
    """
    Class Description: A Vertex can be used to represent the locations in a graph
                       id : to indentify the location
                       edges : the edges coming out from the vertex
                       hasPassenger : to indicate if vertex has a passenger, TRUE means all roads after can use carpool
                       MinFrmStart : an int to be later updated in Dijkstra to store the shortest minutes needed to get to the vertex
                       previous : the vertex added after MinFrmStart in Dijkstra to store the vertex to go FROM to get that shortest minutes
                       
    """
    def __init__(self, id, hasPassenger):
        self.id = id
        self.edges = []
        self.hasPassenger = hasPassenger  ### True means a passenger exist in the vertex, and False means solo
        self.MinFrmStart = math.inf      ### to be updated later in dijkstra, inf for a large number to be replaced
        self.previous = None

    def __str__(self):
        """ When print() is used on a vertex, this provides an organised return string"""
        if self.hasPassenger == True:
            return_string = "Vertex " + str(self.id) + " with passenger with edges" + str(self.edges) + "\n" + " From Source: " + str(self.MinFrmStart)
        else:
            return_string = "Vertex " + str(self.id) + " no passenger with edges" + str(self.edges) + "\n" + " From Source: " + str(self.MinFrmStart)
        return return_string
    
    def add_edges(self,frm_vertex, to_vertex, minutes):
        """ adds an edge from Edge Class to the vertex's edges list"""
        self.edges.append(Edge(frm_vertex, to_vertex, minutes))

class Edge:
    """
    Class Description: An edge can be used to represent a road in the Graph.
                       u : From vertex / location
                       v : To vertex / location
                       w : Weight of edge / Time taken from Vertex to the other Vertex
    """
    def __init__(self, u, v, w):
        """ Initialisation of an edge """
        self.u = u
        self.v = v
        self.w = w
        
    def __str__(self):
        """ When print() is used on an edge, this provides an organised return string"""
        return_string =  "From: " + str(self.u) + " To: " + str(self.v) + " Time: " + str(self.w) 
        return return_string

def get_largest_vertex(lst):
    """
    Function description : When given a list of lists, it returns the largest item in position index 1 out of all of the lists.
                           To get the largest vertex in the entire graph, we only need to check index 1 because there will always be 
                           an incoming road to every location.

                           The time complexity is O(R) because we check every road and comparison takes constant time.
    
    Time complexity: O(R), where R is the number of roads
    """

    largest_vertex = 0
    for x in lst:
        if x[1] > largest_vertex:
            largest_vertex = x[1]
    return largest_vertex

class MinHeap:
    """
    Class description: A min heap data structure taken from FIT1008's min heap implementation written by Brendon Taylor and modified by Jackson Goerner
                       with some functions modified for Dijkstra to add lists.

    Time complexity to take note when used with Dijkstra:
                       - Adding All locations: 
                            O(L log L), where L is number of locations 
                            Explanation: because we have to check every location meaning we have to add O(L) times, 
                            and in each add function, rise takes (log L), therefore O(L log L).

                       - Performing Extract Min on All Locations: 
                            O(L log L), where L is number of locations 
                            Explanation: because we have to check every location meaning we have to loop ExtractMin() O(L) times, 
                            and in each ExtractMin function, sink takes (log L), therefore O(L log L).
    """
    def __init__(self):
        """ Initialisation of the Min Heap using array"""
        self.array = [None]
        self.count = 0

    def __len__(self):
        """ Counts number of items in Min Heap"""
        return self.count

    def add(self, MinFrmStart, PrevLocation):
        """ 
        Adds an item to Min Heap, modified in a way that it's a list instead of an item
        List contains [ The shortest time taken from starting location, the previous location to get this time]
        """
        self.array.append([MinFrmStart, PrevLocation])
        self.count += 1
        self.rise(self.count)  ### rise to ensure it's at the correct position in Min Heap

    def swap(self, i, j):
        """ Swaps the positions of two items"""
        self.array[i], self.array[j] = self.array[j], self.array[i]

    def rise(self, k):
        """
        Rise item at index k to it's correct position
        Time complexity = O(log L), where L is number of locations
        """
        while k > 1 and self.array[k][0] < self.array[k//2][0]:
            self.swap(k, k//2)
            k //= 2

    def sink(self, k):
        """
        Sink item at index k to it's correct position
        Time complexity = O(log L), where L is number of locations
        """
        while 2*k <= self.count:
            child = self.smallestChild(k)
            if self.array[k][0] <= self.array[child][0]:
                break
            self.swap(child, k)
            k = child

    def smallestChild(self, k):
        """
        returns the position of the smallest child in MinHeap
        """
        if 2*k == self.count or self.array[2*k][0] < self.array[2*k+1][0]:
            return 2*k
        else:
            return 2*k + 1

    def extractMin(self):
        """
        Pop the smallest item from Min Heap and return the item
        Time complexity = O(log L), where L is number of locations
        """
        self.swap(1, self.count)
        min = self.array.pop(self.count)
        self.count -= 1
        self.sink(1)
        return min

class Stack:
    """ 
    Class description: A simple Stack class implemented using an array as the underlying data structure.
                       It follows a LIFO principle meaning the last item to be added is the first to be popped.
                       This data structure is used to store the path because it is easier to reverse it for the 
                       for the output.
    """
    def __init__(self):
        """ Initialisation of the stack using an empty array"""
        self.items = []
        self.length = 0
    
    def push(self, item):
        """ Pushes item to the top of the stack """
        self.length += 1
        self.items.append(item)
        
    def pop(self):
        """ Pops item to the top of the stack """
        self.length -= 1
        return self.items.pop()
        
    def getSize(self):
        """ Gets the number of items in the stack """
        return self.length

if __name__ == "__main__":
    pass


