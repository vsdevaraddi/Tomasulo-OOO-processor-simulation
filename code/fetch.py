#This fetch block
Instructions = open(r"InstMem.txt",'r')
table = Instructions.readlines()
def fetch(pc):
    line = table[pc]
    return (line,pc)