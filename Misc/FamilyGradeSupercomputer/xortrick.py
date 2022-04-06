from Crypto.Util.number import getPrime
import time

def fastxor(n, m):
    #xor of all numbers between n and m inclusive
    
    if n == 1:
        if m % 4 == 0:
            return m
        elif m % 4 == 1:
            return 1
        elif m % 4 == 2:
            return m + 1
        elif m % 4 == 3:
            return 0

    else:
        return fastxor(1,m) ^ fastxor(1,n-1)


#you can work out the XOR of 1 to N in constant time - 
#it's always one of 4 results (if you want to verify this yourself, either look at how binary counting works or just test - it becomes obvious pretty soon)

#if N % 4 is 0, it's N
#if N % 4 is 1, it's 1
#if N % 4 is 2, it's N+1
#if N % 4 is 3, it's 0

#to find out the results of only N to M,
#XOR of N to M = (XOR of 1 to M) XOR (XOR of 1 to N-1)
#thus, this can be done in constant time

one = getPrime(1024)
two = getPrime(1024)

if one > two:
    M = one+1
    N = two
else:
    M = two+1
    N = one

correct = fastxor(N,M)
#print(correct)
assert M > N
#to stop this being trivial, I've chosen primes -
#these are all n%4 as 1 or 3
#by adding 1 to M, I guarantee they'll all be 0 or 2
#and by not adding 1 to N, I guarantee n-1 is 0 or 2
#meaning the answer won't be 0 or 1 (and therefore would be easily guessable)

time_limit = 0.2

flag = "WMG{more_like_supercopeuter}"


print("To prove you have a supercomputer, tell me this - ")


start = time.time()


response = int(input(f"What result do you get when XORing together all the numbers from {N} to {M} inclusive?\n> "))

if response == correct:
    taken = time.time() - start
    if taken > time_limit:
        print(f"You took {taken} seconds - way longer than {time_limit} seconds - so L + ratio + no supercomputer + O(n) complexity") 
    else:
        print(f"ok cope, you can have it - and I hope you didn't really use a supercomputer\n{flag}")

else:
    print("wrong 🗿")


