def largest_prime(k: int) -> int:
    """
    approach taken: used Sieve of Eratosthenes's approach to find the largest prime number by changing the maximum
                     prime (max_p) whenever a new prime number is True
    :complexity: (n*log(log(n)))
    """

    # Create a boolean array of "prime[0..n]" and initialize for all entries it as true.
    # A value in prime[i] will finally be false if i is not a prime, else true.
    prime = [True for i in range(k + 1)]
    p = 2
    max_p = 0
    while p * p <= k:

        # If prime[p] is not changed, then it is a prime
        if prime[p] == True:

            # Update all multiples of p
            for i in range(p * p, k + 1, p):
                prime[i] = False
        p += 1

    # Print the greatest prime number in list
    for p in range(2, k + 1):
        if prime[p] and p < k:
            max_p = p
    return max_p
