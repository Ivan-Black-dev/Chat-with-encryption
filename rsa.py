from math import gcd
from random import randint

class RSA:

    e = 0
    d = 0
    n = 0

    def __init__(this):
        this.genKey()

    def genKey(this):
        p, q = RSA.genRandomPrimeNum(), RSA.genRandomPrimeNum()
        this.n = p*q
        phi = (p-1)*(q-1)
        for i in range(2, phi):
            if gcd(i, phi) == 1:
                this.e = i
                break
        this.d = 0
        i = 2
        while this.d == 0:
            if (this.e*i)%phi == 1:
                this.d = i
            i += 1

    def setTargetKeys(this, e, n):
        this.e = e
        this.targetN = n

    def getYourKeys(this):
        return (this.e, this.n)


    def encodeChar(this, m):
        return RSA.optimizePow(ord(m), this.e) % this.targetN
    
    def encodeString(this, s):
        rez = []
        for i in s:
            rez.append(this.encodeChar(i))
        return rez

    def decodeChar(this, c):
        return RSA.optimizePow(c, this.d) % this.n
    
    def decodeString(this, s):
        rez = ""
        for i in s:
            rez += chr(this.decodeChar(i))
        return rez
    
    @staticmethod
    def optimizePow(val, power):
        result = pow(val, power//2)
        result = result * result
        if power % 2 != 0:
            result = result * val
        return result
    
    @staticmethod
    def genRandomPrimeNum():
        with open('prime.txt') as file:
            nums = file.readlines()
        n = randint(0, len(nums)-1)
        return int(nums[n])
    

if __name__ == "__main__":
    a = RSA()
    s = input()
    s = a.encodeString(s)
    print(s)
    print(a.decodeString(s))