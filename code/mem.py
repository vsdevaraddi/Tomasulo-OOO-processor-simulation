import json

import settings

f = open('mem.txt','r+')
table = f.readlines()

def get(address):
    string = table[address]
    return int(string[0:len(string)-1])
            

    
