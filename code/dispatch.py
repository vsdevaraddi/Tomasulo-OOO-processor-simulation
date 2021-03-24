import RAT
import ROB
import RS
import ARF

instruction_arguments = { 'instruction': "", 'destination_tag': "tag", 'source_tag1':"tag", 'source_tag2':"tag", 'value1': 0, 'value2':0 }

'''
instruction_arguments = { 'instruction': "", 'destination_tag': "tag", 'source_tag1':"tag", 'source_tag2':"tag", 'value1': 0, 'value2':0 }
'''

def main(instruction):#instrution is dictionary from decode
    pc = instruction[1]
    instruction = instruction[0]
    rat_read1 = RAT.get(instruction['source1'])
    if(rat_read1['valid']==0):
        instruction_arguments['value1'] = ARF.read(instruction['source1'])
        instruction_arguments['source_tag1'] = None
    else:
        if(rat_read1['busy']==1):
            instruction_arguments['source_tag1'] = rat_read1['tag']
        else:
            instruction_arguments['value1'] = rat_read1['value']
            instruction_arguments['source_tag1'] = None
    if(instruction['source2'] == None):
        instruction_arguments['value2'] = instruction['source2_imm']
        instruction_arguments['source_tag2'] = None
    else:
        rat_read2 = RAT.get(instruction['source2'])
        if(rat_read2['valid']==0):
            instruction_arguments['value2'] = ARF.read(instruction['source2'])
            instruction_arguments['source_tag2'] = None
        else:
            if(rat_read1['busy']==1):
                instruction_arguments['source_tag2'] = rat_read2['tag']
            else:
                instruction_arguments['value2'] = rat_read2['value']
                instruction_arguments['source_tag2'] = None
    instruction_arguments['instruction'] = instruction['InstType']
    #destination rename
    free_tag = ROB.get_latest_free_tag()
    if(free_tag == -1):
        return -1        
    RAT.rename_reg(instruction['destination'],"rob"+str(free_tag+1))
    instruction_arguments['destination_tag'] = "rob"+str(free_tag+1)
    ROB.append(instruction_arguments['instruction'],instruction['destination'],pc)
    #add to reservation table    
    status = RS.append(instruction_arguments,pc)
    if(status == -1):
        return -1
    return pc