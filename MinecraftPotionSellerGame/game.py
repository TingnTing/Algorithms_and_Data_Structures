from __future__ import annotations
from multiprocessing.sharedctypes import Value
# ^ In case you aren't on Python 3.10

from potion import Potion
from avl import AVLTree
from hash_table import LinearProbePotionTable
from node import AVLTreeNode
from random_gen import RandomGen


class Game:

    def __init__(self, seed=0) -> None:
        self.inventory = None
        self.pot_pricing_rank = None
        self.rand = RandomGen(seed=seed)

    def set_total_potion_data(self, potion_data: list) -> None:
        """
        A function sets the potion data into inventory which are: 
        potion name, potion type and potion price. 

        ADT : Hash table
        We used hash tables because it is better to store potions into a table and since they have unique hash keys, 
        it will be easier to access them. In short, to provide direct access to the potions.
        Best and Worst Case time Complexity for Searching, Insertion & Deletion in a Hash Table is O(1)

        :complexity: O(N) -> Where N is number of potions in potion_data
        """
        self.inventory = LinearProbePotionTable(len(potion_data))
        for potion in potion_data:
            pot_name, pot_type, pot_price = potion[0], potion[1], potion[2]
            # Add potion to Inventory
            self.inventory[pot_name] = Potion.create_empty(pot_type, pot_name, pot_price)

    def add_potions_to_inventory(self, potion_name_amount_pairs: list[tuple[str, float]]) -> None:
        """
        Adds 2 elements in tuple which are: potion name and amount in litres

        ADT: AVL Trees
        We used AVL trees because we want the potions to have an order in pricing.
        This will allow us to use the kth_largest function to easily access the most expensive Potion.

        :complexity: O(C * log(N)) -> Where C is the length of potion_name_amount_pairs, and N is the number of potions
                                      in set_total_potion_data.

                               C   -> Accessing all Potions in potion_name_amount_pairs
                            log(N) -> Inserting an AVLTreeNode
        """
        self.pot_pricing_rank = AVLTree()
        for potion in potion_name_amount_pairs:
            name, quantity = potion

            # Select Potion object and update stock quantity
            pot = self.inventory[name]
            pot.set_quantity(quantity)

            # Insert potion in AVL Tree
            self.pot_pricing_rank[pot.buy_price] = pot

    def choose_potions_for_vendors(self, num_vendors: int) -> list[list[str, int]]: 
        """
        Assign a potion for each vendor to sell.
        :pre: Number of vendors must be > 0
        :pre: Number of Potion choices must be enough for number of Vendors

        :complexity: O(C x log(N)) -> Where C is equal to num_vendors, and N is the number of potions in set_total_potion_data.
                                C  -> Looping through no_vendors times
                            log(N) -> Using function kth_largest & deletion of an AVLTreeNode
        """

        # Check Pre-conditions
        if num_vendors <= 0:
            raise ValueError("There has to be at least one vendor!")
        if num_vendors > len(self.inventory):
            raise ValueError("Too many vendors for available potions!")

        vendor_sales = []

        # Chooses random Potions to buy based on kth largest
        for no_vendors in range(num_vendors, 0, -1):
            p = self.rand.randint(no_vendors)
            chosen_potion = (self.pot_pricing_rank.kth_largest(p)).item

            # Delete the potion from inventory
            del self.pot_pricing_rank[chosen_potion.buy_price]
            # Store chosen potion in vendor_sales list
            vendor_sales.append((chosen_potion.name, chosen_potion.quantity))

        # Re-insert all potions back to inventory
        for vendor in vendor_sales:
            pot = self.inventory[vendor[0]]

            # Insert Potion to AVL Tree
            self.pot_pricing_rank[pot.buy_price] = pot
        return vendor_sales

    def solve_game(self, potion_valuations: list[tuple[str, float]], starting_money: list[int]) -> list[float]:
        """
        Playing the game in the most optimal way possible by maximizing vendor profits
        :pre: Number Potions that are to be sold be vendors must be > 0
        :pre: Starting allowance for each vendor must be > 0

        ADT: AVL Tree
        To allow potions to be ordered by price as previously mentioned.

        :complexity: O(N * log(N) + M * N) -> Where N is the length of potion_valuations, and M is the length of starting_money
                                        N  -> Accessing all Potions in potion_valuations
                                    log(N) -> Storing profitable Potions in the AVL Tree
                                        M  -> Accessing each vendor's individual money
                                        N  -> Traversing through the AVL Tree for buying Potions / transactions
        """
        # Check if there are Potions in stock
        if len(potion_valuations) == 0 or potion_valuations is None:
            raise ValueError("Invalid potion_valuation!")
        # Check if vendors have money
        if len(starting_money) == 0 or starting_money is None:
            raise ValueError("Invalid starting_money!")

        pot_price_rank = AVLTree()
        max_money = []

        for potion in potion_valuations:
            potion_name, sell_price = potion

            # Take the buying price of Potions
            buy_price = self.inventory[potion_name].buy_price
            # Calculate if Potion is profitable (if > 1)
            profit_ratio = sell_price / buy_price

            # Store Profitable Potions in the AVL Tree
            if profit_ratio > 1:
                pot_price_rank[profit_ratio] = self.inventory[potion_name]

        for money in starting_money:
            earnings = 0

            # Vendors buy Potions
            money, earnings = self.solve_game_aux(money, earnings, pot_price_rank.root)  # complexity: N, worst case traverse all node
            max_money.append(earnings)

        return max_money

    def solve_game_aux(self, money: int, earnings: int, root: AVLTreeNode) -> tuple[float, float]:
        if money >= 0:
            if root.right is None:
                # We are looking for root, if there is no right subtree
                money, earnings = self.buy_max_potions(money, earnings, root)
            elif root.right is not None:
                # Take right subtree
                money, earnings = self.solve_game_aux(money, earnings, root.right)
            if root.left is not None:
                # Take left subtree
                money, earnings = self.solve_game_aux(money, earnings, root.left)
        return money, earnings

    def buy_max_potions(self, money: int, earnings: int, root: AVLTreeNode) -> tuple[float, float]:
        """
        Function to buy maximum amount of potions possible from the vendor's money available
        Returns the updated earnings after vendor has sold their Potions and the updated 
        money the vendors have after purchasing their Potion inventory stock for the day

        :complexity: O(1) -> All operations are constant, mainly arithmetic calculations (+, -, *, /)
        """
        profit_ratio = root.key                 # Profit ratio of the Potion (> 1 means profit)
        potion_quantity = root.item.quantity    # Potion quantity available
        buy_price = root.item.buy_price         # Potion buying price

        # Calculate Selling Price of Potion
        sell_price = profit_ratio * buy_price            # Potion selling price
        # Calculate Price for whole stock
        total_stock_price = potion_quantity * buy_price  # Price to buy whole stock of Potion

        # Buying the max amount of Potions
        if money > total_stock_price:
            earnings += potion_quantity * sell_price        # Calculate individual Potion earnings
            money -= potion_quantity * buy_price            # Reduce money for buying
        # Buying max amount of Potions with vendor's money
        else:
            earnings += money / buy_price * sell_price
            money -= money
        return money, earnings
