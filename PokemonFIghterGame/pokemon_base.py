__author__ = "T06G06"

from abc import ABC, abstractclassmethod, abstractmethod
import random

class PokemonBase(ABC):
    def __init__(self, hp : int, poke_type: str):
        """
        Initializes variables
        :pre: hp should be greater than 0 and poke_type should be one of {"Fire","Grass","Water","None"}
        :Complexity: O(1)
        """
        if hp > 0 and poke_type  in {"Fire","Grass","Water","None"}:
            self.level = 1
            self.hp = hp
            self.poke_type = poke_type
        else:
            raise TypeError("Invalid Input")
        
    def set_hp (self, newhp) -> bool:
        """
        sets hp into newhp
        :Complexity: O(1)
        """
        self.hp = newhp
        
    
    def set_level(self, newlevel) -> bool:
        """
        sets level into newlevel
        :Complexity: O(1)
        """
        self.level = newlevel
    
    def get_hp (self) -> int:
        """
        returns hp
        :Complexity: O(1)
        """

        return int(self.hp)

    def get_level (self) ->int:
        """
        returns level
        :Complexity: O(1)
        """
        return self.level
      
    def get_poke_type(self) -> str:
        """
        returns poke_type
        :Complexity: O(1)
        """
        return self.poke_type

    def is_fainted(self) -> bool:
        """
        returns hp when hp <= 0
        :Complexity: O(1)
        """
        return self.hp <= 0
        
    def level_up(self) -> None:
        """
        returns level+1
        :Complexity: O(1)
        """
        self.level += 1

    @abstractmethod
    def get_name (self) -> str:
        """
        returns name of pokemon
        :Complexity: O(1)
        """
        pass
    
    @abstractmethod
    def get_speed (self)-> int:
        """
        returns speed of pokemon 
        """
        pass
    
    @abstractmethod
    def get_attack(self)-> int:
        """
        returns attack of pokemon 
        """
        pass
    
    @abstractmethod
    def get_defence(self) -> int:
        """
        returns defence of pokemon 
        """
        pass

    @abstractmethod
    def damage_taken(self) -> None:
        """
        decrease hp according to attack damage
        """
        pass

    def __str__(self) -> str:
        """
        returns the string with pokemon name, hp and level
        :Complexity: O(1)
        """
        return "{}'s HP = {} and level = {}".format(self.get_name(), self.get_hp(), self.get_level())


class GlitchMon(PokemonBase):

    def __init__(self, hp : int, poke_type: str):
        """
        Initializes variables
        :Complexity: O(1)
        """
        PokemonBase.__init__(self, self.hp, None)

    def increase_hp(self) -> None:
        """
        returns hp+1
        :Complexity: O(1)
        """
        self.hp += 1
      
    def superpower(self) -> None:   
        """
        use superpower with the random chance to either 
        gain levle, gain hp or gain hp and level
        :Complexity: O(1)
        """
        power = random.randint(1, 3) #picks a random int from 1, 2, 3, meaning each number has a fair 33.33% chance
        
        if power == 1:
            self.level_up()
        elif power == 2:
            self.increase_hp()
        else:
            self.increase_hp()
            self.level_up()

