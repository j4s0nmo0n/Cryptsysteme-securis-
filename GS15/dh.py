#!/usr/bin/python

from random import randrange, getrandbits
def is_prime(n, k=128):
    """ Test if a number is prime
        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do
        return True if n is prime
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    
    return True
def generate_prime_candidate(length):
    """ Generate an odd integer randomly
        Args:
            length -- int -- the length of the number to generate, in bits
        return a integer
    """
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p
def generate_prime_number(length=1024):
    """ Generate a prime
        Args:
            length -- int -- length of the prime to generate, in bits
        return a prime
    """
    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p
#print(generate_prime_number())
#return (generate_prime_number())

def generate_g(p):
    g = p - 2
    while not is_prime(g,148):
        g = g - 2
    return g


def find_g_order(p,g):
    k = 1
    while pow(g, k, p) != 1:
        k = k+1
    #print k
    return k

def generate_shared_keys(p,g,a,b):
        # Variables Used
    sharedPrime = p    # p
    sharedBase = g     # g
     
    aliceSecret = a     # a
    bobSecret = b     # b
    
    #Begin
    print "......... veuillez patienter un petit instant ... " 
    #print( "********************** generation de secrets partages ************************")

    #print( "Publicly Shared Variables:")
    #print( "    Publicly Shared Prime: " , sharedPrime )
    #print( "    Publicly Shared Base:  " , sharedBase )
     
    # Alice Sends Bob A = g^a mod p
    A = pow(sharedBase, aliceSecret, sharedPrime)
    #print( "\n  Alice Sends Over Public Chanel: " , A )
     
    # Bob Sends Alice B = g^b mod p
    B = pow(sharedBase, bobSecret, sharedPrime)
    #print( "\n  Bob Sends Over Public Chanel: " , B ) 
    #print( "\n------------\n" )
    #print( "Privately Calculated Shared Secret:" )
    # Alice Computes Shared Secret: s = B^a mod p
    aliceSharedSecret = pow(B, aliceSecret, sharedPrime)
    #aliceSharedSecret = bin(aliceSharedSecret) 
    print ""
    print ""
    #print (aliceSharedSecret)
    print( "    Secret partage de Alice : ", aliceSharedSecret)
     
    # Bob Computes Shared Secret: s = A^b mod p
    bobSharedSecret = pow(A, bobSecret, sharedPrime)
    print ""
    print ""
    #print (bobSharedSecret)
    print ""
    print ""
    #bobSharedSecret = bin(bobSharedSecret)
    print(  "   Secret partage de Bob: ",bobSharedSecret)
    return bobSharedSecret


def main():
    #generate_prime_candidate(1024)
    print "......... veuillez patienter un petit instant ... " 
    p = generate_prime_number(1024)
    a = generate_prime_number(1024)
    b = generate_prime_number(1024)
    #print p
    g = generate_g(p)
    print g
    #resultat = is_prime(nb,128)
    #print resultat
    generate_shared_keys(p,g,a,b)
    #find_g_order(p,g)



if __name__ == "__main__":
    main()



