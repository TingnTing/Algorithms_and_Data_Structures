__author__ = "T06G06"

import unittest
from tester_base import TesterBase, captured_output
from pokemon_base import PokemonBase
from pokemon import Charmander, Bulbasaur, Squirtle, MissingNo
from poke_team import PokeTeam
from battle import Battle

class TestPokeTeam(unittest.TestCase):
    def test_choose_team(self):
        team = PokeTeam("Alder")

        # test Exception when battle mode not in {0,1,2}
        with self.assertRaises(Exception):
            team.choose_team(4)

        # test Exception when criterion not in {"lvl", "hp", "attack", "defence", "speed",None}:
        with self.assertRaises(Exception):
            team.choose_team(4)

        # test Exception for pokemon limit
        with captured_output("1 1 1 1") as (inp, out, err):
                team.choose_team(0)


    def test_assign_team(self):

        # testing for battle mode 0 team assignment
        team = PokeTeam("Alder")
        with captured_output("0 3 1") as (inp, out, err):
            team.choose_team(0)
        team.assign_team(0,3,1,0)
        self.assertEqual(str(team),"Bulbasaur's HP = 9 and level = 1, Bulbasaur's HP = 9 and level = 1, Bulbasaur's HP = 9 and level = 1, Squirtle's HP = 8 and level = 1")

        # testing for battle mode 1 team assignment
        team1 = PokeTeam("May")
        with captured_output("1 1 0") as (inp, out, err):
            team1.choose_team(1)
        team1.assign_team(1,1,0,0)
        self.assertEqual(str(team1),"Charmander's HP = 7 and level = 1, Bulbasaur's HP = 9 and level = 1")

        # !! battle mode 2 not tested
        team2 = PokeTeam("May")
        
        with captured_output("2 1 3") as (inp, out, err):
            team2.choose_team(2,"hp")
        team2.assign_team(2,1,0,0)
        self.assertEqual(str(team2),"Bulbasaur's HP = 9 and level = 1, Charmander's HP = 7 and level = 1, Charmander's HP = 7 and level = 1")


    def test__len__(self):
        team = PokeTeam("Jane")
        with captured_output("1 2 0") as (inp, out, err):
            team.choose_team(1)
        team.assign_team(1,2,0,0)
        self.assertEqual(team.__len__(), 3)

    def test__str__(self):
        team = PokeTeam("Matt")
        with captured_output("1 3 0") as (inp, out, err):
            team.choose_team(1)
        team.assign_team(1,3,0,0)
        self.assertEqual(team.__str__(), "Charmander's HP = 7 and level = 1, Bulbasaur's HP = 9 and level = 1, Bulbasaur's HP = 9 and level = 1, Bulbasaur's HP = 9 and level = 1")


if __name__ == '__main__':
    unittest.main()
          
    
  
