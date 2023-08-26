__author__ = "T06G06"

import unittest
import random
from pokemon_base import PokemonBase
from pokemon import Charmander, Bulbasaur, Squirtle, MissingNo

class TestPokeBase(unittest.TestCase):

    # abstract classes aren't tested here
    
    def test_set_hp(self):
        char1 = Charmander()
        char1.set_hp(8)
        self.assertEqual(char1.get_hp(),8)

    def test_set_level(self):
        char1 = Charmander()
        char1.set_level(3)
        self.assertEqual(char1.get_level(),3)

    def test_get_hp(self):
        char1 = Charmander()
        self.assertEqual(char1.get_hp(),7)

    def test_get_level(self):
        char1 = Charmander()
        self.assertEqual(char1.get_level(),1)

    def test_get_poke_type(self):
        char1 = Charmander()
        self.assertEqual(char1.get_poke_type(),"Fire")

    def test_is_fainted(self):
        char1 = Charmander()
        char1.set_hp(0)
        self.assertEqual(char1.is_fainted(),True)

    def test_level_up(self):
        char1 = Charmander()
        char1.set_level(3)
        self.assertEqual(char1.get_level(),3)
        char1.level_up()
        self.assertEqual(char1.get_level(),4)
        
    def test__str__(self):
        char1 = Charmander()
        self.assertEqual(char1.__str__(),"Charmander's HP = 7 and level = 1")

class TestGlitchMon(unittest.TestCase):

    def test_increase_hp(self):
        miss1 = MissingNo()
        prev = miss1.get_hp()
        miss1.increase_hp()
        self.assertEqual(miss1.get_hp(), prev+ 1)

    def test_superpower(self):
        miss1 = MissingNo()
        random.seed(10)         # this seed will always generate randint() to be 3
        prevHP = miss1.get_hp()
        prevLvl = miss1.get_level()
        miss1.superpower()
        self.assertEqual(miss1.get_hp(), prevHP + 1)      # HP increases by 1  
        self.assertEqual(miss1.get_level(), prevLvl + 1)  # Level increases by 1  
        
if __name__ == '__main__':
        unittest.main()
