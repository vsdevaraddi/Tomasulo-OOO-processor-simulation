instruc = {'InstType' : 'add/sub/mul/div/lw/sw', 'destination' : 'reg','source1' : 'register', 'source2' : 'register','source2_imm':'value'}
"""
if source2 == None, then instruction includes inmmediate value
"""

def decode(instruction):
    pc = instruction[1]
    instruction = instruction[0]
    opcode = int(instruction[25:32])
    if(opcode==10011):#immediate format
        if(int(instruction[17:20])==0):
            instruc['InstType'] = 'add'
        else:
            print("Current processor does not support the given function1")
        instruc['destination'] = "r"+str(int(instruction[20:25],2))
        instruc['source1'] = "r"+str(int(intinstruction[12:17],2))
        instruc['source2'] = None
        instruc['source2_imm'] = -int(instruction[0])*2**11 + int(instruction[1:12],2)
    elif(opcode == 110011):
        if(int(instruction[17:20]) == 0):
            if(int(instruction[0:7],2) == 0):
                instruc['InstType'] = 'add'
            elif(int(instruction[0:7],2) == 32):
                instruc['InstType'] = 'sub'
            elif(int(instruction[0:7],2) == 1):
                instruc['InstType'] = 'mul'
            else:
                print("Current processor does not support the given function2")
            instruc['destination'] = "r"+str(int(instruction[20:25],2))
            instruc['source1'] = "r"+str(int(instruction[12:17],2))
            instruc['source2'] = "r"+str(int(instruction[7:12],2))
        elif(int(instruction[17:20],2) == 4):
            if(int(instruction[0:7],2) == 1):
                instruc['InstType'] = 'div'
                instruc['destination'] = "r"+str(int(instruction[20:25],2))
                instruc['source1'] = "r"+str(int(instruction[12:17],2))
                instruc['source2'] = "r"+str(int(instruction[7:12],2))
            else:
                print("Current processor does not support the given function3")
        else:
            print("Current processor does not support the given function4")
    elif(opcode == 11):
        if(int(instruction[17:20],2) == 2):
            instruc['InstType'] = 'lw'
            instruc['destination'] = "r"+str(int(instruction[20:25],2))
            instruc['source1'] = "r"+str(int(instruction[12:17],2))
            instruc['source2'] = None
            instruc['source2_imm'] = -int(instruction[0])*2**11 + int(instruction[1:12],2)            
        else:
            print("Current processor does not support the given function5")
    elif(opcode == 100011):
        if(int(instruction[17,20],2) == 2):
            instruc['InstType'] = 'sw'
            instruc['destination'] = -int(instruction[0])*2^11 + int(instruction[1,7]+instruction[20:25],2)
            instruc['source1'] = "r"+str(int(instruction[12:17],2))
            instruc['source2'] = "r"+str(int(instruction[7:12],2))
        else:
            print("Current processor does not support the given function6")
    return (instruc,pc)
         
