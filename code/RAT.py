import json

import ROB

f = open("rat.txt",'r+')
data = f.read()
table = json.loads(data)
"""
table format : 
{ 'reg' : {'valid' : 1/0, 'busy' : 1/0, 'value' : number , 'tag' : 'rename_reg', 'pc': pc} , next register.....}

Initialise rat.txt with an empty table
"""
def get(reg):
    return table[reg]

def rename_reg(reg,free_tag):
    table[reg]['valid'] = 1
    table[reg]['busy'] = 1
    table[reg]['tag'] = free_tag
    f.seek(0)
    f.truncate()
    json.dump(table,f)

def set(tag,value):
    for i in table:
        if(table[i]['tag'] == tag):
            table[i]['value'] = value
            table[i]['busy'] = 0
            f.seek(0)
            f.truncate()
            json.dump(table,f)
            break

