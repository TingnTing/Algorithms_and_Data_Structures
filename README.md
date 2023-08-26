# Algorithms_and_Data_Structures
A compilations of projects undertaken to explore a different of algorithms

FUNCTION DESCRIPTIONS

Auto-complete Suggestion (Trie)
  - Suggest words to complete the incomplete input based on previous usage of words

Finding Optimal Path with Carpool Decisions (Dijkstra)
  - Utilises Dijkstra's concept to find the shortest path to each vertex and after getting the shortest path for each vertex
  - Then trace back from the end vertex to the start using   information obtained previously where it provides the previous weight and position

Maximum possible data throughput (Network)
  - Returns the maximum flow that can be sent from origin to targets
  - Utilises Ford-Fulkerson method by finding augmenting paths in the residual network
  - Process of finding augmenting path is implemented using breadth-first search (BFS) and it continues finding a path while adhering to capacity constraints
    and flow conservation and update edges in residual network after until there's no more augmenting path. 

Optimizing Space in a Building (Dynamic Programming)
  - Returns an integer of the smallest possible total values for the sections removed.
    and a list of tuples (row, column) of the matrix representing the sections to be removed.
  - Uses Dynamic Programming's concept of storing information in memory and back-tracking for the smallest sections that can be removed.
    
