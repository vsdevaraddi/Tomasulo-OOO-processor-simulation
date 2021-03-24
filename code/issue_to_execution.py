import RS
import execute
import mem

def issue_to_execution_add_sub():
    arg = RS.get_latest_add_sub()
    if(arg == -1):
        return -1
    pc = arg[1]
    arg = arg[0]
    return (execute.add_sub(arg[0],arg[1],arg[2],arg[3]),pc)

def issue_to_execution_mul_div():
    arg = RS.get_latest_mul_div()
    
    if(arg == -1):
        return -1
    pc = arg[1]
    arg = arg[0]
    return (execute.mul_div(arg[0],arg[1],arg[2],arg[3]),arg[0],pc)

def issue_to_execution_lw_sw():
    arg = RS.get_latest_lw_sw()
    if(arg == -1):
        return -1
    pc = arg[1]
    arg = arg[0]
    return (( arg[1],mem.get(arg[2]+arg[3])),pc)