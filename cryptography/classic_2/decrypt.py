import string

f = open('enc', 'r')

key = 45
flag = f.read()

possible_chars = string.ascii_letters + string.digits
n = len(possible_chars)
dec = ''

for c in flag :
    if c in possible_chars :
        i =  possible_chars.index(c)
        dec += possible_chars[(i + key) % n]
    else :
        dec += c

print(dec)

# Output : 
# shellmates{bRutEF0rc3_MaY_com3_h4Ndy}