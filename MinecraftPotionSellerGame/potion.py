class Potion:
    
    def __init__(self, potion_type: str, name: str, buy_price: float, quantity: float) -> None:
        self.potion_type = potion_type
        self.name = name
        self.buy_price = buy_price
        self.quantity = quantity

    def set_quantity(self, quantity):
        """
        added method to change quantity of a potion
        :complexity: O(1)
        """
        self.quantity = quantity

    @classmethod
    def create_empty(cls, potion_type: str, name: str, buy_price: float) -> 'Potion':
        """
        creates a new potion object
        :complexity: O(1)
        """
        return cls(potion_type, name, buy_price, 0)

    @classmethod
    def good_hash(cls, name: str, tablesize: int) -> int:
        """
        a good hash function where base changes for each position
        :complexity: O(n), where n is len(name)
        """
        value = 0
        for char in name:
            value = (ord(char) + 31 * value) % tablesize  # ord() returns ASCII integer value of char
        return value

    @classmethod
    def bad_hash(cls, name: str, tablesize: int) -> int:
        """
        a bad hash function that only looks what characters it contains, causing many collisions
        :complexity: O(n), where n is len(name)
        """
        value = 0
        for char in name:
            value += ord(char)
        return value % tablesize
