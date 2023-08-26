class TrieNode:
    """
    Class Description : This class implements the node of a Trie and stores additional information like :
                        Terminator - indicating end of a sentence, used boolean instead of $ 
                        Freq - frequency, the amount of times sentence exist in sentences
    """
    def __init__(self):
        self.child = [None] * 26
        self.freq = 0
        self.terminator = False

class CatsTrie:
    """
    Class Description : Initialise and constructing Trie Structure according to sentences
    """
    def __init__(self, sentences):
        """
        Function Description : takes in a list of sentence (strings) and construct the Trie stucture to include every string in the sentences list

        Approach Description : It creates a root note and iterates to insert every word in the structure by representing every character as a node at it's specified
                               index. During inserting, it will check if current word is present in Trie structure and only create a new node if character 
                               at the specific index not found.

                               After insertion, a Trie structure is constructed where every word's character is represented by a TrieNode.

                                Input : 
                                    sentences = a list of sentences (strings) to be added to the Trie

                                Time Complexity Explanation :
                                    O(NM) - Insert each character which cost O(M) for each sentence O(N)

                                Aux Space Complexity Explanation :  
                                    O(NM) - in the worst case scenario where all words have different characters, the Trie structure needs extra nodes for each character

        Time complexity : O(NM), where N is number of sentence in sentences and M is number of characters in the longest sentence
        Aux Space complexity : O(NM), where N is number of sentence in sentences and M is number of characters in the longest sentence
        """
        self.root = self.getNode()                     ### Create root node
    
        # Insert every sentence in sentences into Trie - O(NM) 
        for sentence in sentences:
            self.insert(sentence)                      ### inserting a sentence cost O(M)

    def getNode(self,):
        """
        Function description : Creates a TrieNode object including initialising its details

        Time complexity : O(1), constant time complexity
        """
        return TrieNode()

    def toIndex(self, c):
        """ 
        Function description : Turns a character to it's corresponding number representative using ASCII value
        """
        return ord(c) - ord("a")
    
    def toChar(self, n):
        """ 
        Function description : Turns a number to it's corresponding lowercase character using ASCII value 
        """
        return chr(ord('a') + n )

    def insert(self, sentence):
        """
        Function description : Iterates over each character in sentences and create a node if the child node
                               does no exist. It then moves to the next child node and update the current node.

        Time complexity : O(M), where M is number of characters in the longest sentence
        """
        node = self.root                           ### start at root node

        # to check child node for each character in the sentence - O(M)
        for char in range(len(sentence)):
            index = self.toIndex(sentence[char])   ### change character to ASCII numeric value to get index of where to find node

            # checks if child node exists, if not, create a new node
            if not node.child[index]:
                node.child[index] = self.getNode() 
            
            node = node.child[index]               ### set current node to child node to traverse down Trie to check next character
        
        # After the sentence is inserted, sets terminator to True to indicate end of sentence
        node.terminator = True
        # Keeps track of frequency to see how often the sentence is used
        node.freq += 1

    def autoComplete(self, prompt):
        """
        Function description : Accepts a string of characters (prompt) and return a string representing the 
                               completed sentence / best word to use for auto-complete from prompt

        Approach description : After having a Trie structure with all sentences inserted. We can traverse Trie according to prompt to check it's existence.
                               If the prompt does not exist, getting the node's child index when traversing will return None when the character at it's intended 
                               index is not found. It will return None right way without running the rest of the function.

                               After confirming it's existence, find_best_sentence returns the best word to be used for auto-complete.
                               This is by traversing every possible sentence starting with prompt, which is all nodes under the last character in prompt's node
                               in lexicographic order.

                               Because it traverses in lexicographically order and only updates when frequency is higher, it ensures that even when frequency is 
                               the same, the best word will still be the most lexicographically smaller one.

                               It will eventually return the word with the highest frequency or in cases where they have the same frequency it will return
                               the lexicographically smaller string

                                Time complexity explanation :
                                        Best : O(X) - in the best case where word does not exist, find_best_sentence is not ran, therefore complexity is just O(X)
                                        Worst : O(X) - from checking existence, and then running find_best_sentence

                                Input :
                                        prompt = a string of characters from a to z representing the incomplete sentence to be completed

                                Output :
                                        self.bestsentence = a string of the best word to be used as auto completed by Trie

        Time complexity :   Best : O(X), where X is length of prompt and prompt doesn't exist in Trie
                            Worst / Average : O(X + Y), where X is length of prompt and Y is the lenght of the most frequently used sentence in sentences 
                                    that begins with prompt 
        Aux space Complexity : O(1), in-place 
        """
        node = self.root                        ### start at root node

        # Check existence of prompt by traversing Trie according to each character in prompt - O(X)
        for char in prompt:
            index = self.toIndex(char)          ### change character to ASCII numeric value to get index of where to find node

            # If at some point, the node doesn't have a child of next character in prompt
            if not node.child[index]:
                return None                     ### Prompt doesn't exist
        
            node = node.child[index]            ### set current node to child node to traverse down Trie to check next character

        # Initialisation to keep track of the best sentence to be used for auto-complete
        self.bestsentence = ""                  ### best sentence to be used 
        self.bestfreq = 0                       ### frequency of the current best sentence
        self.bestlength = 0                     ### length of current best sentence

        # After confirming existence of word, perform find_best_sentence to find all words with the given prompt and pick the best sentence - O(Y)
        self.find_best_sentence(node, prompt)
        
        # Return the best sentence to be used for auto-complete
        return self.bestsentence

    def find_best_sentence(self, node, word):
        """
        Function description : recursively traverse Trie from given node according to each char in prompt and update the 
                               best sentence information based on frequency

        Approach description : If a node terminator is reached while traversing Trie according to prompt, the current sentence exist in sentences. 
                               It then compares the current sentence and the best recorded sentence up to that point using it's frequency and 
                               always pick the highest, in the case where they have the same frequency, it will update if current sentence is 
                               lexicographically smaller. It will continue calling itself until there is no more sentence in sentences starting 
                               with prompt that isn't checked. 

                               This way all potential sentences to be used as auto-complete is checked and the best is picked.

                               Note : word is used to represent current sentence throughout this function

        Time complexity : O(Y), where Y is the length of the most frequently used sentence in sentences that begins with prompt 
                                unless it doesn't exist
        """
        # If terminator is true, it means the current sentence exist in sentences meaning it could be a candidate
        if node.terminator:
            frequency = node.freq                   ### frequency : number of times current word appeared in sentences

            # If current sentence frequency is higher than the best sentence up to this point
            # This also ensures it always picks the lexicographically smaller string because of the way the Trie is constructed
            if node.freq > self.bestfreq:
                # update the information with current word, current word is now the best sentence up to this point to be used for auto-complete
                self.bestsentence = word
                self.bestlength = len(word)
                self.bestfreq = frequency

        # Iterates all 26 character to ensure no nodes are missed out when traversing for node's child
        for i in range(26):
            # if a child exist for node
            if node.child[i]:
                char = self.toChar(i)               ### gets character of node's child
                # Runs function again with current word and node's child character 
                self.find_best_sentence(node.child[i], word + char)

if __name__ == "__main__":
    pass




