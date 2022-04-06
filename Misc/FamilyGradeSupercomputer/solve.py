from pwn import *

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

doit = remote("localhost", "11111")
r = doit.recvuntil(b"> ").split(b"\n")[1]
N = int(r.split(b" ")[-4])
M = int(r.split(b" ")[-2])

res = fastxor(N,M)
doit.sendline(str(res).encode())

doit.interactive()
