__author__ = "T06G06"

from poke_team import PokeTeam
from pokemon import Charmander, Bulbasaur, Squirtle, MissingNo
from array_sorted_list import *
from pokemon_base import PokemonBase


class Battle():
    def __init__(self, trainer_one_name: str, trainer_two_name: str):
        """
        Initialize values
        :Complexity: O(1)
        """
        self.trainer_one_name = trainer_one_name
        self.trainer_two_name = trainer_two_name
        self.battlemode = None

        # Create 2 empty teams
        self.team1 = PokeTeam(trainer_one_name)
        self.team2 = PokeTeam(trainer_two_name)


    def set_mode_battle(self) -> str:
        """
        Task 3
        Sets the battle mode to 0 which is 'set mode battle'.
        The pokemons fight until it faints and returns the name of the
        winner or 'Draw' after the battle
        
        Complexity: Best Case: O(1)     Worst Case O(N)
        [Where N = len(team1) + len(team2)]
        """

        def first_battle_phase(p1, p2):
            """
            FIRST BATTLE PHASE
            :Complexity: O(1)
            """  

            # If the speed of unit P1 is greater than that of P2, P1 attacks and P2 defends
            if p1.get_speed() > p2.get_speed():
                # P1 attacks and P2 defends (First Attacker)
                p2.damage_taken(p1)

                # If defending Pokemon has not fainted, then retort with their own attack to the first Pokemon
                if p2.hp > 0:
                    # P2 attacks and P1 defends (Second Attacker)
                    p1.damage_taken(p2)
            
            # If the speed of unit P2 is greater than that of P1, P2 attacks and P1 defends
            elif p2.get_speed() > p1.get_speed():
                # P2 attacks and P1 defends
                p1.damage_taken(p2)

                # If defending Pokemon has not fainted, then retort with their own attack to the first Pokemon
                if p1.hp > 0:
                    # P1 attacks and P2 defends (Second Attacker)
                    p2.damage_taken(p1)

            # If the speeds of P1 and P2 are identical, then both attack and defend simultaneously 
            else:
                # Both attack and defend simultaneously
                p2.damage_taken(p1)
                p1.damage_taken(p2)

        def second_battle_phase(p1, p2):
            """
            SECOND BATTLE PHASE
            :Complexity: O(1)
            """  

            # (Scenario 1) One of the two Pokemon faints. Other Pokemon gains 1 level then goes back to the team.
                # p1 ALIVE; p2 FAINTED
            if (p1.hp > 0 and not p2.hp > 0):
                p1.level += 1
                self.team1.team.push(p1)

                # p2 ALIVE; p1 FAINTED
            elif (p2.hp > 0 and not p1.hp > 0):
                p2.level += 1
                self.team2.team.push(p2)

            # (Scenario 2) Both Pokemon faint. In this case, we just leave their carcasses on the battlefield and move on.
                # NOTHING HAPPENS HERE (p1 & p2 Already Popped from Team/Stack)

            # (Scenario 3) Both Pokemon are still alive after they have attacked each other. 
            # Both lose 1 HP. If still alive after losing this 1 HP, sent back to their own teams. 
            # If a Pokemon faints due to losing 1 HP and the other Pokemon is alive, such Pokemon gains 1 level.

                # p1 ALIVE; p2 ALIVE
            elif (p1.hp > 0 and p2.hp > 0):
                p1.hp -= 1
                p2.hp -= 1

                if p1.hp > 0:
                    self.team1.team.push(p1)
                    if (p1.hp > 0 and not p2.hp > 0):
                        p1.level += 1

                if p2.hp > 0:
                    self.team2.team.push(p2)
                    if (p2.hp > 0 and not p1.hp > 0):
                        p2.level += 1

        def ending_phase():
            """
            Ending phase 
            :Complexity: O(1)
            """
            # Return options
            t1_win = self.trainer_one_name
            t2_win = self.trainer_two_name
            draw = "Draw"

            # ENDING PHASE
            # The game ends when at least one of the teams is empty (i.e., it has no usable Pokemon).

                # Team 1 WINS --> Team 2 EMPTY and Team 1 NOT EMPTY
            if not self.team1.team.is_empty() and self.team2.team.is_empty():
                return t1_win
        
                # Team 2 WINS --> Team 1 EMPTY and Team 2 NOT EMPTY
            elif self.team1.team.is_empty() and not self.team2.team.is_empty():
                return t2_win

                # DRAW --> Team 1 & Team 2 EMPTY
            else:
                return draw


        # BATTLE MODE 0
        # Sets up Teams 
            # Team 1
        self.team1.choose_team(0, None)
            # Team 2
        self.team2.choose_team(0, None)

        ### BATTLE SEQUENCE ###
        while not self.team1.team.is_empty() and not self.team2.team.is_empty():
            
            # Battle begins with the first Pokemon of each team
            ## Pop a Pokemon from each team
            p1 = self.team1.team.pop()
            p2 = self.team2.team.pop()

            # Commence First Battle Phase
            first_battle_phase(p1, p2)

            # Commence Second Battle Phase
            second_battle_phase(p1, p2)

            # Commence Ending Phase
        return ending_phase()


    def rotating_mode_battle(self) -> str:
        """
        Task 4
        Sets the battle mode to 1 which is 'roatating mode battle'.
        Pokemon fights one round and then gets back to its team and
        returns the name of the player of the winner or 'Draw'.
        
        Complexity: Best Case: O(1)     Worst Case O(N)
        [Where N = len(team1) + len(team2)]
        """

        def first_battle_phase(p1, p2):
            """
            FIRST BATTLE PHASE
            :Complexity: O(1)
            """ 

            # If the speed of unit P1 is greater than that of P2, P1 attacks and P2 defends
            if p1.get_speed() > p2.get_speed():
                # P1 attacks and P2 defends (First Attacker)
                p2.damage_taken(p1)

                # If defending Pokemon has not fainted, then retort with their own attack to the first Pokemon
                if p2.hp > 0:
                    # P2 attacks and P1 defends (Second Attacker)
                    p1.damage_taken(p2)
            

            # If the speed of unit P2 is greater than that of P1, P2 attacks and P1 defends
            elif p2.get_speed() > p1.get_speed():
                # P2 attacks and P1 defends
                p1.damage_taken(p2)

                # If defending Pokemon has not fainted, then retort with their own attack to the first Pokemon
                if p1.hp > 0:
                    # P1 attacks and P2 defends (Second Attacker)
                    p2.damage_taken(p1)

            # If the speeds of P1 and P2 are identical, then both attack and defend simultaneously 
            else:
                # Both attack and defend simultaneously
                p2.damage_taken(p1)
                p1.damage_taken(p2)

        def second_battle_phase(p1, p2):
            """
            SECOND BATTLE PHASE
            :Complexity: O(1)
            """  

            # (Scenario 1) One of the two Pokemon faints. # Other Pokemon gains 1 level, then goes back to the team.
                # p1 ALIVE; p2 FAINTED
            if (p1.hp > 0 and not p2.hp > 0):
                p1.level += 1
                self.team1.team.append(p1)

                # p2 ALIVE; p1 FAINTED
            elif (p2.hp > 0 and not p1.hp > 0):
                p2.level += 1
                self.team2.team.append(p2)


            # (Scenario 2) Both Pokemon faint. In this case, we just leave their carcasses on the battlefield and move on.
                # NOTHING HAPPENS HERE (p1 & p2 Already Popped from Team/Stack)

            # (Scenario 3) Both Pokemon are still alive after they have attacked each other. 
            # Both lose 1 HP. If still alive after losing 1 HP, sent back to their own teams. 
            # If a Pokemon faints due to losing 1 HP and other Pokemon is alive, such Pokemon gains 1 level.

                # p1 ALIVE; p2 ALIVE
            elif (p1.hp > 0 and p2.hp > 0):
                p1.hp -= 1
                p2.hp -= 1

                if p1.hp > 0:
                    self.team1.team.append(p1)
                    if (p1.hp > 0 and not p2.hp > 0):
                        p1.level += 1

                if p2.hp > 0:
                    self.team2.team.append(p2)
                    if (p2.hp > 0 and not p1.hp > 0):
                        p2.level += 1

        def ending_phase():
            """
            ENDING PHASE
            :Complexity: O(1)
            """  

            # Return options
            t1_win = self.trainer_one_name
            t2_win = self.trainer_two_name
            draw = "Draw"

        # The game ends when at least one of the teams is empty (i.e., it has no usable Pokemon).
            # Team 1 WINS --> Team 2 EMPTY and Team 1 NOT EMPTY
            if not self.team1.team.is_empty() and self.team2.team.is_empty():
                return t1_win
        
            # Team 2 WINS --> Team 1 EMPTY and Team 2 NOT EMPTY
            elif self.team1.team.is_empty() and not self.team2.team.is_empty():
                return t2_win

            # DRAW --> Team 1 & Team 2 EMPTY
            else:
                return draw
    

        # BATTLE MODE 1
        # Sets up Teams (BATTLE MODE 1)
            # Team 1
        self.team1.choose_team(1, None)
            # Team 2
        self.team2.choose_team(1, None)

        ### BATTLE SEQUENCE ###
        while not self.team1.team.is_empty() and not self.team2.team.is_empty():
            
            # Battle begins with the first Pokemon of each team
            ## Pop a Pokemon from each team
            p1 = self.team1.team.serve()
            p2 = self.team2.team.serve()

            # Commence First Battle Phase
            first_battle_phase(p1, p2)

            # Commence Second Battle Phase
            second_battle_phase(p1, p2)

        # Commence Ending Phase
        return ending_phase()



    def optimised_mode_battle(self, criterion_team1: str, criterion_team2: str) -> str:
        """
        Task 5
        Sets the battle mode to 2 which is 'optimised mode battle'.
        Pokemons are arranged into non-descending order according to the user's choice
        of criterion and returns the name of the player of the winner or 'Draw'.

        Complexity: Best Case: O(1)     Worst Case O(N)
        [Where N = len(team1) + len(team2)]
        """
        self.criterion_team1 = criterion_team1
        self.criterion_team2 = criterion_team2
    
        # Sets up Teams (BATTLE MODE 2)
            # Team 1
        self.team1.choose_team(2, self.criterion_team1)
            # Team 2
        self.team2.choose_team(2, self.criterion_team2)

         # Return options
        t1_win = self.trainer_one_name
        t2_win = self.trainer_two_name
        draw = "Draw"

        def criterion_to_key(self, team: int, team_criterion: str) -> int:
            """
            Checks criterion of team and gets the key of the current pokemon of that team
            :complexity: O(1)
            """
            if team_criterion == "hp":
                if team == 1:
                    return p1.value.get_hp()
                else:
                    return p2.value.get_hp()
            if team_criterion == "lvl":
                if team == 1:
                    return p1.value.get_level()
                else:
                    return p2.value.get_level()
            if team_criterion == "defence":
                if team == 1:
                    return p1.value.get_defence()
                else:
                    return p1.value.get_defence()
            if team_criterion == "speed":
                if team == 1:
                    return p1.value.get_speed()
                else:
                    return p2.value.get_speed()
                
                
        ### BATTLE SEQUENCE ###
        while not self.team1.team.is_empty() and not self.team2.team.is_empty():
            
            # Battle begins with the first Pokemon of each team
            ## Takes the pokemon at the end of the list because it is arranged in ascending but they are battling in descending
            index=len(self.team1.team)-1
            p1 = self.team1.team.delete_at_index(index)
            index2=len(self.team2.team)-1
            p2 = self.team2.team.delete_at_index(index2)

            prev = criterion_to_key(self,1,self.team1.criterion)
            prev2 = criterion_to_key(self,2,self.team2.criterion) 


            ## FIRST BATTLE PHASE

            # If the speed of unit P1 is greater than that of P2, P1 attacks and P2 defends
            if p1.value.get_speed() > p2.value.get_speed():
                # P1 attacks and P2 defends (First Attacker)
                p2.value.damage_taken(p1.value)

                # If defending Pokemon has not fainted, then retort with their own attack to the first Pokemon
                if p2.value.get_hp() > 0:
                    # P2 attacks and P1 defends (Second Attacker)
                    p1.value.damage_taken(p2.value)
            

            # If the speed of unit P2 is greater than that of P1, P2 attacks and P1 defends
            elif p2.value.get_speed() > p1.value.get_speed():
                # P2 attacks and P1 defends
                p1.value.damage_taken(p2.value)

                # If defending Pokemon has not fainted, then retort with their own attack to the first Pokemon
                if p1.value.get_hp() > 0:
                    # P1 attacks and P2 defends (Second Attacker)
                    p2.value.damage_taken(p1.value)


            # If the speeds of P1 and P2 are identical, then both attack and defend simultaneously 
            else:
                # Both attack and defend simultaneously
                p2.value.damage_taken(p1.value)
                p1.value.damage_taken(p2.value)


            ## SECOND BATTLE PHASE
    
            # (Scenario 1) One of the two Pokemon faints. # Other Pokemon gains 1 level, then goes back to the team.
            
                # p1 ALIVE; p2 FAINTED
            if (p1.value.get_hp() > 0 and not p2.value.get_hp() > 0):
            
                p1.value.level +=1
                key = criterion_to_key(self, 1, self.team1.criterion)

                # if key stays the same, the pokemon returns back to the team in it's original position
                if key == prev:
                    if self.team1.team.is_full():
                        self.team1.team.resize()

                    self.team1.team[self.team1.team.length] = p1
                    self.team1.team.length += 1

                # else it would arrange itself in the team according to the key
                else:
                    addplace = ListItem(p1.value,key)
                    self.team1.team.add(addplace)
                  

                # p2 ALIVE; p1 FAINTED
            elif (p2.value.get_hp() > 0 and not p1.value.get_hp() > 0):
                p2.value.level += 1
                key = criterion_to_key(self, 2, self.team2.criterion)

                # if key stays the same, the pokemon returns back to the team in it's original position
                if key == prev2:
                    if self.team2.team.is_full():
                        self.team2.team.resize()

                    self.team2.team[self.team2.team.length] = p2
                    self.team2.team.length += 1

                # else it would arrange itself in the team according to the key
                else:
                    addplace = ListItem(p2.value,key)
                    self.team2.team.add(addplace)

        
            # (Scenario 2) Both Pokemon faint. In this case, we just leave their carcasses on the battlefield and move on.
                # NOTHING HAPPENS HERE (p1 & p2 Already Popped from Team/Stack)


            # (Scenario 3) Both Pokemon are still alive after they have attacked each other. 
            # Both lose 1 HP. If they are still alive after losing this 1 HP, sent back to their own teams. 
            # If a Pokemon faints here due to losing 1 HP and other Pokemon is alive, such Pokemon gains 1 level.

                # p1 ALIVE; p2 ALIVE
            # elif (p1.hp > 0 and p2.hp > 0):
            elif (p1.value.get_hp() > 0 and p2.value.get_hp() > 0):
                p1.value.hp -= 1
                p2.value.hp -= 1

                if p1.value.get_hp() > 0:
                    key = criterion_to_key(self, 1, self.team1.criterion)

                    if key == prev:

                        if self.team1.team.is_full():
                            self.team1.team.resize()

                        self.team1.team[self.team1.team.length] = p1
                        self.team1.team.length += 1

                    else:
                        addplace = ListItem(p1.value,key)
                        self.team1.team.add(addplace)


                    if (p1.value.get_hp() > 0 and not p2.value.get_hp() > 0):
                        p1.value.level += 1

                if p2.value.get_hp() > 0:
        
                    key = criterion_to_key(self, 2, self.team2.criterion)

                    if key == prev2:
                
                        if self.team2.team.is_full():
                            self.team2.team.resize()

                        self.team2.team[self.team2.team.length] = p2
                        self.team2.team.length += 1

                    else:
                        addplace = ListItem(p2.value,key)
                        self.team2.team.add(addplace)

                if (p2.value.get_hp() > 0 and not p1.value.get_hp() > 0):
                    p2.value.level += 1

            # Appends MissingNo into the list if it exists for it to battle as the last pokemon
            if self.team1.team.is_empty() and self.team1.missing_exist:
                    MissingNoPokemon = MissingNo()
                    addPokemon = ListItem(MissingNoPokemon, MissingNoPokemon.get_hp())
         
                    self.team1.team.add(addPokemon)
                    self.team1.missing_exist = False
              
            if self.team2.team.is_empty() and self.team2.missing_exist:
                    MissingNoPokemon = MissingNo()
                    addPokemon = ListItem(MissingNoPokemon, MissingNoPokemon.get_hp())
         
                    self.team2.team.add(addPokemon)
                    self.team2.missing_exist = False
 
        # ENDING PHASE
        # The game ends when at least one of the teams is empty (i.e., it has no usable Pokemon).

        # Check if missingNo exists

            # Team 1 WINS --> Team 2 EMPTY and Team 1 NOT EMPTY
        if not self.team1.team.is_empty() and self.team2.team.is_empty():
            return t1_win
        
            # Team 2 WINS --> Team 1 EMPTY and Team 2 NOT EMPTY
        elif self.team1.team.is_empty() and not self.team2.team.is_empty():
            return t2_win

            # DRAW --> Team 1 & Team 2 EMPTY
        else:
            return draw
