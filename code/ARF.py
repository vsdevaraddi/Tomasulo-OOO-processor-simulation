import json

f = open('arf.txt','r+')
data = f.read()
table = json.loads(data)
"""
table = {'destination' : value}

"""

def read(reg):
    return table[reg]

def write(destination,value):
    table[destination] = value
    f.seek(0)
    f.truncate()
    json.dump(table,f)