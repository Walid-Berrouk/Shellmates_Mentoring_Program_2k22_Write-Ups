#! /usr/bin/python3


import json
from hexdump import hexdump
  
# Opening JSON file
with open('packets.json') as j:
    j = open('packets.json')
  
# returns JSON object as 
# a dictionary
packets = json.load(j)
  
# Iterating through the json list

# for packet in packets:
#     print(list(packet["_source"]["layers"]["dns"]["Queries"].values())[0]["dns.qry.name"])


dns_names = [list(packet["_source"]["layers"]["dns"]["Queries"].values())[0]["dns.qry.name"] for packet in packets]

# print(dns_names)

dns_subs = [dns_name.split(".")[0] for dns_name in dns_names]

# print(dns_subs)

# Closing file
j.close()

with open('data', 'w') as g:
    for lis in dns_subs[::2]:
        g.write(lis)
        g.write('\n')
    print('Written in data.')