__author__ = "T06G06"

from pokemon_base import PokemonBase, GlitchMon
import random

class Charmander(PokemonBase):
    POKE_NAME:str = "Charmander" 
    POKE_TYPE:str = "Fire"
    HP:int = 7
    POKE_ATTACK:int = 6
    POKE_DEFENCE:int = 4
    POKE_SPEED:int = 7   

    def __init__(self) :
        """
        Initializes hp and poke_type
        :Complexity: O(1)
        """
        PokemonBase.__init__(self, self.HP, self.POKE_TYPE)

      
    def get_name(self) -> str:
        """
        return name of pokemon
        :complexity: O(1)
        """
        return self.POKE_NAME

    def get_attack(self) -> int:
        """
        returns attack (attack + level)
        :complexity: O(1) 

        """
        return self.POKE_ATTACK + self.level

    def get_speed(self) -> int:
        """
        returns speed (speed + level)
        :Complexity: O(1) 
        """
        return self.POKE_SPEED + self.level

    def get_defence(self) -> int:
        """
        returns defence 
        :complexity: O(1) 
        """
        return self.POKE_DEFENCE

    def effective_damage(self, otherPokemon: PokemonBase) -> int:
        """
        returns effective damage when other poke_type attacks
        :complexity: O(1) 
        """  
      
        effective_damage = 0
        if otherPokemon.poke_type == self.get_poke_type:
            effective_damage = otherPokemon.get_attack() 
        elif otherPokemon.poke_type == "Grass":
            effective_damage = otherPokemon.get_attack() / 2
        elif otherPokemon.poke_type == "Water":
            effective_damage = otherPokemon.get_attack() * 2    
        else:
            effective_damage = otherPokemon.get_attack()          
        return effective_damage

    def damage_taken(self, otherPokemon: PokemonBase) -> None:
        """
        decrease hp according to attack damage
        :Complexity: O(1) 
        """
        damage = self.effective_damage(otherPokemon)
        if damage > self.get_defence():
            self.set_hp(self.get_hp()- damage)
        else:
            damage = damage // 2
            self.set_hp(self.get_hp()- (damage)) 
    

class Bulbasaur(PokemonBase):
    POKE_NAME:str = "Bulbasaur" 
    POKE_TYPE:str = "Grass"
    HP:int = 9
    POKE_ATTACK:int = 5
    POKE_DEFENCE:int = 5
    POKE_SPEED:int = 7 

    def __init__(self):
        """
        Initializes hp and poke_type
        :complexity: O(1)
        """
        PokemonBase.__init__(self, self.HP, self.POKE_TYPE)

    def get_name(self) -> str:
        """
        return name of pokemon
        :complexity: O(1)
        """
        return self.POKE_NAME

    def get_attack(self) -> int:
        """
        returns attack (attack)
        :complexity: O(1) 

        """
        return self.POKE_ATTACK
    
    def get_defence(self) -> int:
        """
        returns defence 
        :complexity: O(1) 

        """
        return self.POKE_DEFENCE

    def get_speed(self) -> int:
        """
        returns speed (speed + level//2)
        :complexity: O(1) 

        """
        return self.POKE_SPEED + (self.level//2)

    def effective_damage(self, otherPokemon: PokemonBase) -> int:
        """
        returns effective damage when other poke_type attacks
        :complexity: O(1) 
        """
        effective_damage = 0
        if otherPokemon.poke_type == self.get_poke_type:
            effective_damage = otherPokemon.get_attack() 
        elif otherPokemon.poke_type == "Water":
            effective_damage = otherPokemon.get_attack() / 2
        elif otherPokemon.poke_type == "Fire":
            effective_damage = otherPokemon.get_attack() * 2
        else:
            effective_damage = otherPokemon.get_attack()
        return effective_damage

    def damage_taken(self, otherPokemon: PokemonBase) -> None:
        """
        decrease hp according to attack damage
        :complexity: O(1) 
        """
        damage = self.effective_damage(otherPokemon)
        if damage > (self.get_defence() + 5):
            self.set_hp(self.get_hp()- damage)
        else:
            damage = damage // 2
            self.set_hp(self.get_hp()- (damage))

class Squirtle(PokemonBase):
    POKE_NAME:str = "Squirtle" 
    POKE_TYPE:str = "Water"
    HP:int = 8
    POKE_ATTACK:int = 4
    POKE_DEFENCE:int = 6
    POKE_SPEED:int = 7
    

    def __init__(self):
        """
        Initializes hp and poke_type
        :complexity: O(1)
        """
        PokemonBase.__init__(self, self.HP, self.POKE_TYPE)

    def get_name(self) -> str:
        """
        return name of pokemon
        :complexity: O(1)
        """
        return Squirtle.POKE_NAME

    def get_attack(self) -> int:
        """
        returns attack (attack + level//2)
        :complexity: O(1) 

        """
        return Squirtle.POKE_ATTACK + (self.level//2)

    def get_defence(self) -> int:
        """
        returns defence (defence + level)
        :complexity: O(1) 

        """
        return self.POKE_DEFENCE + self.level

    def get_speed(self) -> int:
        """
        returns speed
        :complexity: O(1) 

        """
        return Squirtle.POKE_SPEED
    

    def effective_damage(self, otherPokemon: PokemonBase) -> int:
        """
        returns effective damage when other poke_type attacks
        :complexity: O(1) 
        """
        effective_damage = 0
        if otherPokemon.poke_type == self.get_poke_type:
            effective_damage = otherPokemon.get_attack() 
        elif otherPokemon.poke_type == "Fire":
            effective_damage = otherPokemon.get_attack() / 2
        elif otherPokemon.poke_type == "Grass":
            effective_damage = otherPokemon.get_attack() * 2
        else:
            effective_damage = otherPokemon.get_attack()
        return effective_damage

    def damage_taken(self, OtherPokemon: PokemonBase) -> None:
        """
        decrease hp according to attack damage
        :complexity: O(1) 
        """
        damage = self.effective_damage(OtherPokemon)
        if damage > (self.get_defence() * 2):
            self.set_hp(self.get_hp()- damage)
        else:
            damage = damage // 2
            self.set_hp(self.get_hp()- (damage))

class MissingNo(GlitchMon, PokemonBase):
    #average stats of prev 3 pokemons
    POKE_NAME:str = "MissingNo" 
    POKE_TYPE:str = "None"
    HP:int = int(( 7 + 9 + 8) / 3)
    POKE_ATTACK:int = int((7 + 5 + 4 + 1//2) / 3 )
    POKE_DEFENCE:int = int((4 + 5 + 7) / 3)
    POKE_SPEED:int = int((8 + 7 + 1//2 + 7) / 3)


    def __init__(self) :
        """
        Initializes hp and poke_type
        :complexity: O(1)
        """
        PokemonBase.__init__(self, self.HP, self.POKE_TYPE)

    def get_name(self) -> str:
        """
        return name of pokemon
        :complexity: O(1)
        """
        return MissingNo.POKE_NAME

    def get_attack(self) -> int:
        """
        returns attack (attack)
        :complexity: O(1) 

        """
        return MissingNo.POKE_ATTACK + self.level  

    def get_defence(self) -> int:
        """
        returns defence 
        :complexity: O(1) 

        """
        return MissingNo.POKE_DEFENCE + self.level

    def get_speed(self) -> int:
        """
        returns speed
        :complexity: O(1) 

        """
        return MissingNo.POKE_SPEED + self.level  

    def effective_damage(self, otherPokemon: PokemonBase) -> int: 
        """
        returns effective damage
        :complexity: O(1)
        """
        return otherPokemon.get_attack()

    def damage_taken(self, otherPokemon: PokemonBase) -> None:  
        """
        decrease hp according to attack damage
        :complexity: O(1) 
        """
        chances = random.randint(0,100)   # 100 is inclusive
        if chances < 25:                  # 25% chance of it generating a number less than 25
            self.superpower()
          
        else:
            rand = random.randint(1,3) 
            if rand == 1:
                # Charmander
                damage = self.effective_damage(otherPokemon)
                if damage > self.get_defence():
                    self.set_hp(self.get_hp()- damage)
                else:
                    damage = damage // 2
                    self.set_hp(self.get_hp()- (damage))
    
            if rand == 2:
                # Bulbasaur
                damage = self.effective_damage(otherPokemon)
                if damage > (self.get_defence() + 5):
                    self.set_hp(self.get_hp()- damage)
                else:
                    damage = damage // 2
                    self.set_hp(self.get_hp()- (damage))
                  
            if rand == 3:
                # Squirtle
                damage = self.effective_damage(otherPokemon)
                if damage > (self.get_defence() * 2):
                    self.set_hp(self.get_hp()- damage)
                else:
                    damage = damage // 2
                    self.set_hp(self.get_hp()- (damage))
