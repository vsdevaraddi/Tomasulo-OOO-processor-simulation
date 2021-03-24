import json

import ARF
import settings

ROB_LENGTH = settings.ROB_LENGTH

f = open(r'rob.txt',"r+")
data = f.read()
table = json.loads(data)
head = 0
tail = -1
"""
table = {'tag' : {'InstType' : 'add/sub/mul/div/lw/sw', 'destination' : 'ARF_reg', 'valid' : 1/0, 'value' : 'tag_value_from_CDB', 'pc': pc}}
InstType  = None means that the row is empty.

Intialize rob.txt with empty table
"""
def get_latest_free_tag():
    if((tail+1 == ROB_LENGTH and head == 0) or (tail < head and tail+1 == head and tail != -1)):
        return -1
    return (tail+1)%8 

def set(tag,value):
    table[tag]['valid'] = 1
    table[tag]['value'] = value
    f.seek(0)
    f.truncate()
    json.dump(table,f)

def append(InstType,Destination,pc):
    tag = get_latest_free_tag()
    if(tag == -1):
        return -1
    table[list(table.keys())[tag]]['InstType'] = InstType
    table[list(table.keys())[tag]]['destination'] = Destination
    table[list(table.keys())[tag]]['valid'] = 0
    table[list(table.keys())[tag]]['pc'] = pc
    global tail
    tail = tag
    f.seek(0)
    f.truncate()
    json.dump(table,f)
    return 0

def save_entry_to_ARF():
    global head
    top = list(table.keys())[head]
    if(table[top]['InstType'] == None):
        return -2 #empty table
    if(table[top]['valid'] == 0):
        return -1 #has got no value
    ARF.write(table[top]['destination'],table[top]['value'])
    table[top]['destination'] = None
    head = (head+1)%8
    f.seek(0)
    f.truncate()
    json.dump(table,f)
    return table[top]['pc']