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

def select_sections(matrix):
    """
    Function description : This function returns a list of two items, the first item is an integer of the smallest possible total values for the sections removed.
        The second item is a list of tuples where where each tuple is the (row, column) of the matrix representing the sections to be removed.
        This function uses Dynamic Programming's concept of storing information in memory and back-tracking for the smallest sections that can be removed.
    

    Approach description : Since the input is in the form of a matrix, we can create a matrix in the memory with each section being [-1] temporary 
        to store information for each section later. This problem 
        requires us to know the smallest occupancy rate of the last row, the problem can be simplified to finding the smallest occupancy up to
        for every row. We can just fill up the matrix in memory with the smallest occupancy up until each section.
        With the restriction of only being able to remove sections where the section is directly above or diagonally right and left. For every entry, 
        we can only add the section where row - 1 representing the section above, section where row - 1 and col + 1 representing section diagonally right and section 
        where row -1 and col - 1 representing diagonally left and pick whichever smaller. Index out of range has to be considered by making sure the first row being exactly same and 
        last column has no diagonally right section. Now that we have the matrix with every section having the smallest occupancy. We can backtrack from
        the last row of the matrix starting with the smallest in the row which would surely be the last tuple in the list and also the value for the total
        occupancy rate. The back-tracing process works by comparing the value, again, above and diagonally right or left using the same concept above. By storing each 
        section in stack, we can reverse it by popping to get the tuples in order for each section to be removed.

    Given n is the number of rows and m is the number of columns in input matrix:
        Creating and Filling up the matrix in memory costs O(n-1) * O(m) = O(nm) respectively
        Finding the minimum of the last row cost O(m)
        Starting at minimum, going through each row and comparing the current section with the section above and diagonally right or left O(n) 0r
        Reversing the stack O(n)

        Total time complexity : O(nm) + O(m) + O(n) = O(nm)

    Creating the matrix takes O(nm) auxillary space while the stack take up O(n) and output list of tuples take O(n) because they are fixed size.

        Total auxillary space: O(nm) + O(n) + O(n) = O(nm) 
    
    Input : 
        matrix : a list of rows with every item is the occupancy probability and it's position represents the column

    Output : 
        a list containing :
            minimum_total_occupancy : an integer for the total values for the sections removed
            sections_locations : a list of tuple (row, column) each representing the sections to remove where 
        

    Time complexity : O(nm), where n is the number of rows (number of list in the list) and m is the number of columns (number of items in each list) 
                      in the input matrix
    Aux space complexity : O(nm), where n is the number of rows and m is the number of columns
    """

    def allUpperOnly(positon):
        """
        Function description : Used only when last column reaches, meaning the sections to be removed can only be directly above.
            This function adds the sections direcly above all tuple columns as the last column without the need to go through comparing the diagonally right section

        Time complexity : O(n) in the worst case, where n is number of rows in matrix.
                          Worst case is when it is the section of the last row of the last column, this function push tuple for every row.
        """
        # for every row starting from the row where section from last column is detected up till the first row. That row is already appended so it starts from position - 1 in range
        for i in range(position[0]-1,-1,-1):    
            sections_location.push((i,no_col-1))

    # finding number of rows and columns - O(1)
    no_col = len(matrix[0])
    no_row = len(matrix)

    # sections_location stored using Stack to reverse it later as backtracking returns the path from last row to first and we want to opposite
    sections_location = Stack()

    # making no_col by no_row memory space and filling them with -1 - O(nm)
    mem = no_row * [None]      
    for col in range(no_row):       
        mem[col] = [-1] * no_col               ### -1 because impossible to have negative probability 

    # Base case - first row always same because it is the minimum occupancy itself 
    mem[0] = matrix[0]

    # Filling up mem with their own minimum occupancy up to that section
    for row in range(1,no_row):
        for col in range(no_col):

            # Accessing specific sections - O(1)
            curr = matrix[row][col]            ### curr, current is the section we are looking at    
            prevUp = mem[row-1][col]           ### prevUp, previous up is the section directly above
            min_total = curr + prevUp          ### min_total to get the smallest total probablity by adding current section with previous upper section

            if no_col != 1:
                # If it's last col, it only has the option of adding the one above therefore we only perform comparison for columns not equals to last column
                if col != no_col-1 and col != 0  :
                    # it has the option of either adding the one above or diagonally right
                    prevDiagRight = mem[row-1][col+1]   ### prevDiag, previous diagonal is the section diagonally right
                    # it will then compare the both of them and pick the lesser value
                    if prevDiagRight + curr < min_total:    ### comparing with a specific position takes O(1)
                        min_total = prevDiagRight + curr
                    prevDiagLeft = mem[row-1][col-1]
                    if prevDiagLeft + curr < min_total:    
                        min_total = prevDiagLeft + curr
                    
                    
                # If it's the first column, it can only move diagonally right
                elif col == 0  :
                    prevDiagRight = mem[row-1][col+1]  

                    if prevDiagRight + curr < min_total:  
                        min_total = prevDiagRight + curr

                # If it's the last column, it can only move diagonally left
                elif col == no_col-1:
                    prevDiagLeft = mem[row-1][col-1]
                    if prevDiagLeft + curr < min_total:    
                        min_total = prevDiagLeft + curr     

            # replace -1 with the smallest probability up until that section
            mem[row][col] = min_total       
    

    # Now that we have a mem matrix where each value is the minimum occupancy up to that section
    # We can backtrack up the matrix to find the path by picking the lesser item from the last row and move either up or diagonally 
    # set minimum as the first item of the last row temporary
    minimum_total_occupancy = mem[no_row-1][0]
    # position to keep track of the position of which we took the value from
    position = (no_row-1,0)
    # Loop through the last row to find the minimum #O(m)
    for col in range(1,no_col):
        if mem[no_row-1][col] < minimum_total_occupancy:
            minimum_total_occupancy = mem[no_row-1][col]
            position = (no_row-1,col)

    # add the position of the minimum to sections_locations because it's one of the paths    
    sections_location.push(position)
    
    # if there is only one column, it can only move directly up
    if no_col == 1:
        allUpperOnly(position)

    else:
        for row in range(no_row-2,-1,-1):         ### -2 because last row added and also because it's inclusive 
            # since we can only move up or diagonally from the previous position, allowed_col tells us which col are we allowed to move to
            allowed_cols = position[1]

            # If it is the First column it only checks the section above and diagonally right for the next smaller section
            if allowed_cols == 0 :
                if mem[row][allowed_cols] < mem[row][allowed_cols+1]:
                    position = (row, allowed_cols)
                else:
                    position = (row, allowed_cols+1)

            # If it is the Last column it only checks the section above and diagonally left for the next smaller section
            elif allowed_cols == no_col-1:
                if mem[row][allowed_cols] < mem[row][allowed_cols-1]:
                    position = (row, allowed_cols)
                else:
                    position = (row, allowed_cols-1)

        
            # If it is the middle columns, it checks all three
            else:
                if mem[row][allowed_cols] < mem[row][allowed_cols-1] and mem[row][allowed_cols] < mem[row][allowed_cols+1] :
                    position = (row, allowed_cols)
                elif mem[row][allowed_cols+1] < mem[row][allowed_cols-1] and mem[row][allowed_cols+1] < mem[row][allowed_cols] :
                    position = (row, allowed_cols+1)
                else:
                    position = (row, allowed_cols-1)

            # push the smallest next value's position 
            sections_location.push(position)

    
    # Since it was backtracking, sections_locations is in a reversed path, so we have to reverse it with stack which cost O(n)
    final_sections_location = []
    for i in range(no_row):
        final_sections_location.append(sections_location.pop())    ### popping removes the top item and place it in a list
    
    return [minimum_total_occupancy, final_sections_location]
    
if __name__ == "__main__":
    pass