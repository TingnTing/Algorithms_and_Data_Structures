__author__ = "T06G06"

import unittest
from pokemon import Charmander, Bulbasaur, Squirtle, MissingNo


class TestCharmander(unittest.TestCase):
    # Charmander test
    def test_ch_get_name(self):
        char1 = Charmander() 
        self.assertEqual(char1.get_name(), 'Charmander' )
        
    def test_ch_get_attack(self): 
        char1 = Charmander() 
        self.assertEqual(char1.get_attack(), 7 )

    def test_ch_get_speed(self): 
        char1 = Charmander() 
        self.assertEqual(char1.get_speed(), 8 )
    
    def test_ch_get_defence(self): 
        char1 = Charmander() 
        self.assertEqual(char1.get_defence(), 4 )

    def test_ch_effective_damage(self):
        bul1 = Bulbasaur()
        char1 = Charmander()
        self.assertEqual(char1.effective_damage(bul1),2.5)

    def test_ch_damage_taken(self):
        bul1 = Bulbasaur()
        char1 = Charmander()
        char1.damage_taken(bul1)
        self.assertEqual(char1.get_hp(),6)

class TestMissingNo(unittest.TestCase):
    def test_get_name(self):  
        miss1 = MissingNo() 
        self.assertEqual(miss1.get_name(), 'MissingNo' )

    def test_get_attack(self): 
        miss1 = MissingNo() 
        self.assertEqual(miss1.get_attack(), 6 ) 

    def test_get_speed(self): 
        miss1 = MissingNo() 
        self.assertEqual(miss1.get_speed(), 8 ) 

    def test_get_defence(self): 
        miss1 = MissingNo()
        self.assertEqual(miss1.get_defence(), 6 )

    def test_effective_damage(self):
        char1 = Charmander()
        miss1 = MissingNo()
        self.assertEqual(miss1.effective_damage(char1),7) 

    def test_damage_taken(self):
        bul1 = Bulbasaur()
        miss1 = MissingNo()
        miss1.damage_taken(bul1)
        self.assertEqual(miss1.get_hp(),6)
        
if __name__ == '__main__':
    unittest.main()
