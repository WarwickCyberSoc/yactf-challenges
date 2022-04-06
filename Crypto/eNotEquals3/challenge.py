#!/usr/bin/env python3
from Crypto.Util.number import bytes_to_long, getPrime

flag = bytes_to_long(b'WMG{fake_flag_for_testing}')

e = 4
p, q = getPrime(2048), getPrime(2048)

n = p * q

c = pow(flag, e, n)

print(f'n = {n}')
print(f'e = {e}')
print(f'c = {c}')