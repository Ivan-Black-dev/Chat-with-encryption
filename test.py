import math

def isPrime(n):
    for i in range(2, int(math.sqrt(n))+1):
        if n % i == 0:
            return False
    return True

with open('prime.txt', 'w') as file:
    for i in range(10, 10**3):
        if isPrime(i):
            file.write(str(i) + '\n')