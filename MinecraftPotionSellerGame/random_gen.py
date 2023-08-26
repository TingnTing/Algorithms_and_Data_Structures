from typing import Generator

def lcg(modulus: int, a: int, c: int, seed: int) -> Generator[int, None, None]:
    """
    Linear congruential generator.
    :time complexity: O(1)
    """
    while True:
        seed = (a * seed + c) % modulus
        yield seed

def check1bits(numbers: list) -> bool:
    """
    :time complexity: O(1)
    """
    oneBit = 0
    for i in range(5):
        if numbers[i] % 2 == 1:
            oneBit += 1
        numbers[i] //= 2
    if oneBit >= 3:
        return True


class RandomGen:

    def __init__(self, seed: int = 0) -> None:
        """
        Initialize variable
        """
        self.random_gen = lcg(pow(2, 32), 134775813, 1, seed)

    def randint(self, k: int) -> int:
        """
        Generates a random number
        :time complexity: O(n)
        """
        numbers = []
        res = 0
        factor = 1
        for value in self.random_gen:
            value = value >> 16
            numbers.append(value)
            if len(numbers) == 5:
                break
        for i in range(16):
            if check1bits(numbers):
                res += factor
            factor *= 2
        return (res % k) + 1

if __name__ == "__main__":
    Random_gen = lcg(pow(2,32), 134775813, 1, 0)
    r = RandomGen(seed = 0)
    print(r.randint(100))
