import RS

def add_sub(Itype,destination_tag,value1,value2):
    if(Itype == 'add'):
        return (destination_tag,(value1+value2)%2**32) 
    elif(Itype == 'sub'):
        return (destination_tag,(value1-value2)%2**32)
    else:
        print("ERROR: Execution: wrong Instruction type")

def mul_div(Itype,destination_tag,value1,value2):
    if(Itype == 'mul'):
        return (destination_tag,(value1*value2)%2**32)
    elif(Itype == 'div'):
        return (destination_tag,float(value1/value2)%2**32)
    else:
        print("ERROR: Execution: wrong instruction type")
