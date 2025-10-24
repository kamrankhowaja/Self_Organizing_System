import time

def sieve_highest_prime(n):
    # Step 1: Initialize the array
    is_prime = [True] * (n + 1)
    is_prime[0] = False
    is_prime[1] = False

    # Step 2: Sieve of Eratosthenes
    p = 2
    while p * p <= n:
        if is_prime[p]:
            for multiple in range(p * p, n + 1, p):
                is_prime[multiple] = False
        p += 1

    # Step 3: Find the highest prime
    for i in range(n, 1, -1):
        if is_prime[i]:
            return i

    return None  # in case no primes found


# Example usage
if __name__ == "__main__":
    n = 1_000_000  # same as your C code
    start = time.time()
    highest_prime = sieve_highest_prime(n)
    if highest_prime:
        print(f"Highest prime number up to {n} is: {highest_prime}")
    else:
        print(f"No primes found up to {n}.")

    end = time.time()
    print(f"Time taken: {end - start:.6f} seconds") 
