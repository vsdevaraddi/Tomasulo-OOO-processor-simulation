import time

import settings
import fetch
import decode
import dispatch
import execute
import cdb
import ROB
import issue_to_execution
import RS

status_recorder = {}
for i in range(settings.Number_of_instructions):
    status_recorder[i] = {'issue':0,'execute_start':0,'execute_complete':0,'write_cdb':0,'commit':0}
'''
status_recorder = {0:{'issue':0,'execute_start':0,'execute_complete':0,'write_cdb':0,'commit':0},
1:{'issue':0,'execute_start':0,'execute_complete':0,'write_cdb':0,'commit':0},
2:{'issue':0,'execute_start':0,'execute_complete':0,'write_cdb':0,'commit':0},
3:{'issue':0,'execute_start':0,'execute_complete':0,'write_cdb':0,'commit':0},
4:{'issue':0,'execute_start':0,'execute_complete':0,'write_cdb':0,'commit':0},
5:{'issue':0,'execute_start':0,'execute_complete':0,'write_cdb':0,'commit':0},
6:{'issue':0,'execute_start':0,'execute_complete':0,'write_cdb':0,'commit':0} }
'''
pc = 0
clock = 2
instruction_raw = fetch.fetch(pc)
instruction_arguments = decode.decode(instruction_raw)
stat = dispatch.main(instruction_arguments)
status_recorder[pc]['issue'] = 1
pc = pc + 1
lw_sw_list = []
mul_div_list = []
add_sub_list = []
while True:
    s = ROB.save_entry_to_ARF()
    if(s != -1 and s != -2):
        status_recorder[s]['commit'] = clock
        if(s == settings.Number_of_instructions - 1):
            break        
    result0 = issue_to_execution.issue_to_execution_lw_sw()
    result1 = issue_to_execution.issue_to_execution_add_sub()
    result2 = issue_to_execution.issue_to_execution_mul_div()
    if(result0 != -1 ):
        lw_sw_list.append([settings.lw_latency,result0])
    broadcast0 = -1
    for i in range(len(lw_sw_list)):
        if(lw_sw_list[i][0] == 0):
            broadcast0 = i
    if(broadcast0 != -1):
        broad0 = lw_sw_list[broadcast0][1]
        cdb.broadcast(broad0[0])
        status_recorder[broad0[1]]['execute_start'] = clock-settings.lw_latency
        status_recorder[broad0[1]]['execute_complete'] = clock-1
        status_recorder[broad0[1]]['write_cdb'] = clock
    if(result1 != -1):
        add_sub_list.append([settings.add_sub_latency,result1])
    broadcast1 = -1
    for i in range(len(add_sub_list)):
        if(add_sub_list[i][0]==0):
            broadcast1 = i
    if(broadcast1 != -1):
        broad1 = add_sub_list[broadcast1][1]
        cdb.broadcast(broad1[0])
        status_recorder[broad1[1]]['execute_start'] = clock-settings.add_sub_latency
        status_recorder[broad1[1]]['execute_complete'] = clock-1
        status_recorder[broad1[1]]['write_cdb'] = clock
    if(result2 != -1):
        itype = result2[1]
        if(itype == 'mul'):
            mul_div_list.append([settings.mul_latency,result2])
        if(itype == 'div'):
            mul_div_list.append([settings.div_latency,result2])
    broadcast2 = -1
    for i in range(len(mul_div_list)):
        if(mul_div_list[i][0] == 0):
            broadcast2 = i
    if(broadcast2 != -1):
        broad2 = mul_div_list[broadcast2][1]
        cdb.broadcast(broad2[0])
        itype = broad2[1]
        status_recorder[broad2[2]]['execute_complete'] = clock-1
        status_recorder[broad2[2]]['write_cdb'] = clock      
        if(itype == 'mul'):
            status_recorder[broad2[2]]['execute_start'] = clock-settings.mul_latency
        if(itype == 'div'):
            status_recorder[broad2[2]]['execute_start'] = clock-settings.div_latency        
    if(pc<settings.Number_of_instructions):
        instruction_raw = fetch.fetch(pc)
        instruction_arguments = decode.decode(instruction_raw)
        stat = dispatch.main(instruction_arguments)
    if(stat != -1):
        if(pc < settings.Number_of_instructions):
            status_recorder[pc]['issue'] = clock  
        pc = pc+1
    clock = clock + 1
    for i in range(len(lw_sw_list)):
        lw_sw_list[i][0] = lw_sw_list[i][0] - 1 
    for i in range(len(add_sub_list)):
        add_sub_list[i][0] = add_sub_list[i][0] - 1
    for i in range(len(mul_div_list)):
        mul_div_list[i][0] = mul_div_list[i][0] - 1
    time.sleep(settings.Clock_duration)
for i in status_recorder:
    print(i," --> ",status_recorder[i])