import json

import settings

f1 = open('rs_addsub.txt','r+')
data = f1.read()
table_addsub = json.loads(data)
f2 = open('rs_muldiv.txt','r+')
data = f2.read()
table_muldiv = json.loads(data)
f3 = open('rs_lwsw.txt','r+')
data = f3.read()
table_lwsw = json.loads(data)

add_sub_station = settings.add_sub_station
mul_div_station = settings.mul_div_station
lw_sw_station = settings.lw_sw_station
add_sub_count = 0
mul_div_count = 0
lw_sw_count = 0

"""
table = { 1 : {'instruction':'', 'busy' : 1/0, 'destination_tag':'tag', 'source_tag1':'tag', 'source_tag2':'tag', 'value1': value, 'value2':value ,'pc':pc }, 2 : {} ...}

Initialise rs.txt with empty table
"""

def append(instruction_arguments,pc):
    global add_sub_count
    if(instruction_arguments['instruction']=='add' or instruction_arguments['instruction']=='sub'):
        if(add_sub_count == add_sub_station):
            return -1
        index = 0
        for i in table_addsub:
            if(table_addsub[i]['busy']==0):
                index = i
                break
        table_addsub[index]['instruction'] = instruction_arguments['instruction']
        table_addsub[index]['busy'] = 1
        table_addsub[index]['destination_tag'] = instruction_arguments['destination_tag']
        table_addsub[index]['source_tag1'] = instruction_arguments['source_tag1']
        table_addsub[index]['source_tag2'] = instruction_arguments['source_tag2']
        table_addsub[index]['value1'] = instruction_arguments['value1']
        table_addsub[index]['value2'] = instruction_arguments['value2']
        table_addsub[index]['pc'] = pc
        add_sub_count = add_sub_count + 1
        f1.seek(0)
        f1.truncate()
        json.dump(table_addsub,f1)
    elif(instruction_arguments['instruction']=='mul' or instruction_arguments['instruction']=='div'):
        global mul_div_count
        if(mul_div_count == mul_div_station):
            return -1
        index = 0
        for i in table_muldiv:
            if(table_muldiv[i]['busy']==0):
                index = i
                break
        table_muldiv[index]['instruction'] = instruction_arguments['instruction']
        table_muldiv[index]['busy'] = 1
        table_muldiv[index]['destination_tag'] = instruction_arguments['destination_tag']
        table_muldiv[index]['source_tag1'] = instruction_arguments['source_tag1']
        table_muldiv[index]['source_tag2'] = instruction_arguments['source_tag2']
        table_muldiv[index]['value1'] = instruction_arguments['value1']
        table_muldiv[index]['value2'] = instruction_arguments['value2']
        table_muldiv[index]['pc'] = pc
        mul_div_count = mul_div_count + 1
        f2.seek(0)
        f2.truncate()
        json.dump(table_muldiv,f2)
    elif(instruction_arguments['instruction']=='lw' or instruction_arguments['instruction']=='sw'):
        global lw_sw_count
        if(lw_sw_count == lw_sw_station):
            return -1
        index = 0
        for i in table_lwsw:
            if(table_lwsw[i]['busy']==0):
                index = i 
                break
        table_lwsw[index]['instruction'] = instruction_arguments['instruction']
        table_lwsw[index]['busy'] = 1
        table_lwsw[index]['destination_tag'] = instruction_arguments['destination_tag']
        table_lwsw[index]['address_offset'] = instruction_arguments['value2']
        table_lwsw[index]['source_register'] = instruction_arguments['source_tag1']
        table_lwsw[index]['source_register_value'] = instruction_arguments['value1']
        table_lwsw[index]['pc'] = pc
        lw_sw_count = lw_sw_count + 1
        f3.seek(0)
        f3.truncate()
        json.dump(table_lwsw,f3)
    else:
        print("ERROR:RS: wrong instruction type")

def catch_tag_value(tag,value):
    for i in table_addsub:
        if(table_addsub[i]['source_tag1'] == tag and table_addsub[i]['busy']==1):
            table_addsub[i]['source_tag1'] = None
            table_addsub[i]['value1'] = value
        if(table_addsub[i]['source_tag2'] == tag and table_addsub[i]['busy']==1):
            table_addsub[i]['source_tag2'] = None
            table_addsub[i]['value2'] = value
    for i in table_muldiv:
        if(table_muldiv[i]['source_tag1'] == tag and table_muldiv[i]['busy']==1):
            table_muldiv[i]['source_tag1'] = None
            table_muldiv[i]['value1'] = value
        if(table_muldiv[i]['source_tag2'] == tag and table_muldiv[i]['busy']==1):
            table_muldiv[i]['source_tag2'] = None
            table_muldiv[i]['value2'] = value
    for i in table_lwsw:
        if(table_lwsw[i]['source_register'] == tag and table_lwsw[i]['busy']==1):
            table_lwsw[i]['source_register'] = None
            table_lwsw[i]['source_register_value'] = value
    f1.seek(0)
    f2.seek(0)
    f3.seek(0)
    f1.truncate()
    f2.truncate()
    f3.truncate()
    json.dump(table_addsub,f1)
    json.dump(table_muldiv,f2)
    json.dump(table_lwsw,f3)

def get_latest_add_sub():
    for i in table_addsub:
        if(table_addsub[i]['source_tag1'] == None and table_addsub[i]['source_tag2'] == None and table_addsub[i]['busy'] == 1):
            Itype=table_addsub[i]['instruction']
            destination_tag =table_addsub[i]['destination_tag']
            value1 =  table_addsub[i]['value1']
            value2 = table_addsub[i]['value2']
            pc = table_addsub[i]['pc']
            table_addsub[i]['instruction'] = None
            table_addsub[i]['busy'] = 0
            table_addsub[i]['destination_tag'] = None
            table_addsub[i]['source_tag1'] = None
            table_addsub[i]['source_tag2'] = None
            global add_sub_count
            add_sub_count = add_sub_count - 1
            f1.seek(0)
            f1.truncate()
            json.dump(table_addsub,f1)
            return ((Itype,destination_tag,value1,value2),pc)
    return -1

def get_latest_mul_div():
    for i in table_muldiv:
        if(table_muldiv[i]['source_tag1'] == None and table_muldiv[i]['source_tag2'] == None and table_muldiv[i]['busy'] == 1):
            Itype=table_muldiv[i]['instruction']
            destination_tag =table_muldiv[i]['destination_tag']
            value1 =  table_muldiv[i]['value1']
            value2 = table_muldiv[i]['value2']
            pc = table_muldiv[i]['pc']
            table_muldiv[i]['instruction'] = None
            table_muldiv[i]['busy'] = 0
            table_muldiv[i]['destination_tag'] = None
            table_muldiv[i]['source_tag1'] = None
            table_muldiv[i]['source_tag2'] = None
            global mul_div_count
            mul_div_count = mul_div_count - 1 
            f2.seek(0)
            f2.truncate()
            json.dump(table_muldiv,f2)
            return ((Itype,destination_tag,value1,value2),pc)
    return -1

def get_latest_lw_sw():
    for i in table_lwsw:
        if(table_lwsw[i]['source_register'] == None  and table_lwsw[i]['busy'] == 1):
            Itype=table_lwsw[i]['instruction']
            destination_tag =table_lwsw[i]['destination_tag']
            address_off =  table_lwsw[i]['address_offset']
            base = table_lwsw[i]['source_register_value']
            pc = table_lwsw[i]['pc']
            table_lwsw[i]['instruction'] = None
            table_lwsw[i]['busy'] = 0
            table_lwsw[i]['destination_tag'] = None
            table_lwsw[i]['source_register'] = None
            f3.seek(0)
            f3.truncate()
            json.dump(table_lwsw,f3)
            global lw_sw_count
            lw_sw_count = lw_sw_count - 1
            return ((Itype,destination_tag,base,address_off),pc)
    return -1