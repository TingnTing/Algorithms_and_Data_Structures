__author__ = "T06G06"

from pokemon import Charmander, Bulbasaur, Squirtle, MissingNo
from stack_adt import ArrayStack
from queue_adt import CircularQueue
from array_sorted_list import ArraySortedList
from sorted_list import ListItem
 
class PokeTeam(): 

    MAX_LIMIT = 6
    def __init__(self, trainer: str) -> None:
        """
        Initializes values
        :complexity: O(1)
        """
        self.name = trainer
        self.battle_mode = None
        self.team = None
        self.criterion = None 
        self.missing_exist = False

    def choose_team(self, battle_mode: int = 0, criterion: str = None) -> None:
        """
        Gets the input of battle mode and criterion from the user
        :pre: Battle mode must be {0,1,2}
                       Criterion must be {"lvl", "hp", "attack", "defence", "speed"} or None 
        :comp: 0(n), where n is the number of user inputs
        """ 
        # Exception for battle mode
        if battle_mode not in {0,1,2}:
            raise Exception("Value must be 0, 1, 2")
        self.battle_mode = battle_mode

        if criterion not in {"lvl", "hp", "attack", "defence", "speed",None}:
            raise Exception("Value must be one from: lvl, hp, attack, defence, speed")
        self.criterion = criterion
        
        # Exception for pokemon limit
        print("Howdy Trainer! Choose your team as C B S \nwhere C is the number of Charmanders \n \t  B is the number of Bulbasaurs \n \t  S is the number of Squirtles")
        WithinLimit = False         # Boolean to check if number of Pokemons are 6 or under and only a maximum of one MissingNo
        MissingExceeded = False     # Boolean to check if there is more than one MissingNo
        while not WithinLimit:    
            try: 
                user_input = input()
                c, b, s, m = [int(i) for i in user_input.split()]
                totalpokemons = c + b + s + m
                if m > 1:
                    raise Exception()
            except ValueError:
                try:
                    c, b, s = [int(i) for i in user_input.split()]
                    m = 0
                    totalpokemons = c + b + s + m
                except ValueError:
                    print("Invalid input, please follow c b s")
                    continue
            except Exception:     
                MissingExceeded = True            # to print error message when MissingNo is more than one
                
            if not MissingExceeded and totalpokemons <= 6 :   
                WithinLimit = True                # When all requirements are met
              
            elif MissingExceeded:
                print("Only one MissingNo allowed")
                MissingExceeded = False             # to reset the boolean for the next loop
              
            else:
                print("Exceeded the limit of 6 pokemons. Please enter a valid team")
              
        self.assign_team(c, b, s, m)

    def assign_team(self, charm: int, bulb: int, squir: int, missNo: int) -> None:
        """
        Pokemon assigned to a team according to the battle mode    
        :pre: Total number of pokemons must be 6 or less
        :complexity: O(n), where n is the total number of pokemons
        """  

        # Battle mode 0 = Stack ADT
        # Battle mode 1 = Circular Queue 
        # Battle mode 2 = Sorted List ADT     

        # Stack ADT used
        if self.battle_mode == 0:
            self.team = ArrayStack(PokeTeam.MAX_LIMIT) 
            # Stack follows LIFO. First item pushed is at the bottom
            for _ in range(missNo):
                self.team.push(MissingNo())
            for _ in range(squir):
                self.team.push(Squirtle())
            for _ in range(bulb):
                self.team.push(Bulbasaur())
            for _ in range(charm):
                self.team.push(Charmander())         # Last item pushed is at the top

        # Circular Queue used wait 
        if self.battle_mode == 1:
            self.team = CircularQueue(PokeTeam.MAX_LIMIT) 
            for _ in range(charm):
                self.team.append(Charmander())       # Queue follows FIFO. First item appended to the front of the queue
            for _ in range(bulb):
                self.team.append(Bulbasaur()) 
            for _ in range(squir):
                self.team.append(Squirtle())
            for _ in range(missNo):
                self.team.append(MissingNo())                   # Last item appended will be at the back of the queue


        if self.battle_mode == 2:
            self.team = ArraySortedList(PokeTeam.MAX_LIMIT)
          
            if missNo == 1:
                missNo_exists = True
            else:
                missNo_exists = False
              
            charm_list = [] 
            bulb_list = []
            squir_list = [] 
              
            # Arrange each pokemons to categorize into a new list 
            for _ in range(charm):
                charm_list.append(Charmander())
            for _ in range(bulb):
                bulb_list.append(Bulbasaur())
            for _ in range(squir):
                squir_list.append(Squirtle())
            

        # ArraySortedList [LIFO] --> In non-increasing order

            if self.criterion == "hp":
                # Arranged from lowest to highest hp
                for c in charm_list:
                    addPokemon = ListItem(c, c.get_hp())
                    self.team.add(addPokemon)
                for s in squir_list:
                    addPokemon = ListItem(s, s.get_hp())
                    self.team.add(addPokemon)
                for b in bulb_list:
                    addPokemon = ListItem(b, b.get_hp())
                    self.team.add(addPokemon)
                if missNo_exists:
                    self.missing_exist = True
                    
                    

            if self.criterion == "lvl":
                # All Levels Equal - Follow C B S
                for c in charm_list:
                    addPokemon = ListItem(c, c.get_level())
                    self.team.add(addPokemon)
                for b in bulb_list:
                    addPokemon = ListItem(b, b.get_level())
                    self.team.add(addPokemon)
                for s in squir_list:
                    addPokemon = ListItem(s, s.get_level())
                    self.team.add(addPokemon)
                if missNo_exists:
                    self.missing_exist = True
        

            if self.criterion == "attack":
                # Arranged from lowest to highest attack
                for s in squir_list:
                    addPokemon = ListItem(s, s.get_attack())
                    self.team.add(addPokemon)
                for b in bulb_list:
                    addPokemon = ListItem(b, b.get_attack())
                    self.team.add(addPokemon)
                for c in charm_list:
                    addPokemon = ListItem(c, c.get_attack())
                    self.team.add(addPokemon)
                if missNo_exists:
                    self.missing_exist = True

            if self.criterion == "defence":
                # Arranged from lowest to highest defence
                for c in charm_list:
                    addPokemon = ListItem(c, c.get_defence())
                    self.team.add(addPokemon)
                for b in bulb_list:
                    addPokemon = ListItem(b, b.get_defence())
                    self.team.add(addPokemon)
                for s in squir:
                    addPokemon = ListItem(s, s.get_defence())
                    self.team.add(addPokemon)
                if missNo_exists:
                    self.missing_exist = True

            if self.criterion == "speed":
                # Arranged from lowest to highest speed
                for b in bulb_list:
                    addPokemon = ListItem(b, b.get_speed())
                    self.team.add(addPokemon)
                for s in squir_list:
                    addPokemon = ListItem(s, s.get_speed())
                    self.team.add(addPokemon)
                for c in charm_list:
                    addPokemon = ListItem(c, c.get_speed())
                    self.team.add(addPokemon)
                if missNo_exists:
                    self.missing_exist = True
                        
    

    def __len__(self) -> int:
        """
        returns the length of the team (number of pokemons)
        :complexity: O(1)
        """
        return len(self.team)

    def __str__(self) -> str:
        """
        returns the level and hp for all the pokemons in the team 
        :complexity: = O(n), where n is the number of pokemons in the team
        """ 

        # For Stack
        if self.battle_mode == 0:
            string = ""
            for i in range(len(self) -1, -1, -1):
                if self.team.array[i].is_fainted() == False:
                    string += str(self.team.array[i])
                    if i != 0:
                        string += ", "
            return string

        # For Queue
        if self.battle_mode == 1:
            string = ""
            index = self.team.front

            for i in range(len(self)):
                string += str(self.team.array[index])
                if i != len(self) - 1:
                    string +=  ", "
                index = (index + 1) % len(self.team.array)     # to wrap around the queue
            return string

        # For Sorted List
        if self.battle_mode == 2:
            string = ""
            for i in range(len(self)-1 , -1, -1):
            
                string += str(self.team.array[i].value)
                if i != 0:
                    string += ", "
        return string
