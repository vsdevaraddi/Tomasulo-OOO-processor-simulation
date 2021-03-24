import RAT
import RS
import ROB


def broadcast(result):
    ROB.set(result[0],result[1])
    RS.catch_tag_value(result[0],result[1])
    RAT.set(result[0],result[1])