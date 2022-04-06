from Crypto.Cipher import AES
import binascii
import os

# key = b"AAAAAAAAAAAAAAAA"
# iv = b"BBBBBBBBBBBBBBBB"
key = os.urandom(16)
iv = os.urandom(16)
password = b"n0_imp0sters_0n_the_sh1p_p1ea5e!"

ciph = AES.new(key, AES.MODE_CBC, iv)

encrypted = ciph.encrypt(password)
print("Password:", password.hex())
print("Key:", key.hex())
print("IV:", iv.hex())
print("Encrypted password:", encrypted.hex())

print("""
	uint8_t iv[16] = {{ {} }};
	uint8_t key[16] = {{ {} }};
	uint8_t correct[] = {{ {} }};
""".format(
    ",".join([str(int(b)) for b in iv]),
    ",".join([str(int(b)) for b in key]),
    ",".join([str(int(b)) for b in encrypted])
))
# key = binascii.unhexlify("10a58869d74be5a374cf867cfb473859")
# iv = binascii.unhexlify(16*"00")

# plaintext = binascii.unhexlify(16*"00")
# ciphertext = binascii.unhexlify("6d251e9044b051e04eaa6fb4dbf78465")

# ciph = AES.new(key, AES.MODE_CBC, iv)

# test1 = ciph.encrypt(plaintext)
# print("The ciphertext is what we expected:", test1==ciphertext)    

# #We need to reset the cipher to get the correct IV
# ciph = AES.new(key, AES.MODE_CBC, iv)

# test2 = ciph.decrypt(ciphertext)
# print("The recovered plaintext is what we expected:", test2 == plaintext)
