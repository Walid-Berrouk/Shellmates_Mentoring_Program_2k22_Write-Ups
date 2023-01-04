from pwn import xor


with open("chall", "rb") as f:
    byte = f.read(4)

print(byte)

# Output (magic byte) :
# b'\x7fELF'

cmp = b'\x3A\x09\x0A\x19\x12\x71\x0B\x67\x1C\x1A\x0E\x3F\x2B\x20\x3F\x19\x45\x01'

secret = xor (cmp, byte)

print(secret)

# Output
# b'ELF_m4G!c_ByTes_:D'