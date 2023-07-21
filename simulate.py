from myclass import *
from utils import *
import os

def execute_cmd(cmd: str, mode=1):
    cd_lst = cmd.split(' ')
    # print(cd_lst)
    if cd_lst[0] == "lookup":
        if len(cd_lst) == 3 and mode == 1:
            CHORD.lookup(cd_lst[1], True)
            return int(cd_lst[1])+1
        elif cd_lst[1]:
            # print(cd_lst[1])
            CHORD.lookup(cd_lst[1])
        else:
            print("MISSING ONE ARGMENT: key")
        
    elif cd_lst[0] == "insert":
        if cd_lst[1] and cd_lst[2]:
            CHORD.insert(cd_lst[1], cd_lst[2])
        else:
            print("MISSING TWO ARGMENT: key, val")
    
    elif cd_lst[0] == "delete":
        if cd_lst[1]:
            CHORD.delete(cd_lst[1])
        else:
            print("MISSING ONE ARGMENT: key")
    
    elif cd_lst[0] == "join":
        # if len(cd_lst) == 3:
        #     # print(cd_lst)
        #     CHORD.join(cd_lst[1], True)
        if cd_lst[1]:
            # print(cd_lst[1])
            CHORD.join(cd_lst[1])
        else:
            print("MISSING ONE ARGMENT: key")

    elif cd_lst[0] == "leave":
        if cd_lst[1]:
            CHORD.leave(cd_lst[1])
        else:
            print("MISSING ONE ARGMENT: key")

    elif cd_lst[0] == "add_hop_entry":
        CHORD.set_ahs(int(cd_lst[1]))

    elif cd_lst[0] == "plot" and mode == 1:
        if cd_lst[1] == '1':
            CHORD.plot_hop_pdf()
        elif cd_lst[1] == '2':
            CHORD.plot_muti_scale_hop_boxLine()

    elif cd_lst[0] == "clear":
        CHORD.clear()

    elif cd_lst[0] == "show":
        CHORD.show()
    
    elif cd_lst[0][0] == "q":
        print("end simulation")
        return False

    else:
        print("INSTRUCTION {} NO FOUND\nOnly {} allowed".format\
              (cd_lst[0],["lookup","insert""delete","join","leave","clear","show","q"]))
    return True

def run(mode = 0, path = ""):
    file = 0
    if mode == 1:
        try:
            cmd_reader = open(path, 'r')
        except:
            exit("NO INSTRUCTIONS")
        cd_lst = cmd_reader.readline()
        while cd_lst:
            cd_lst = cmd_reader.readline()
            ret = execute_cmd(cd_lst)
            if not ret:
                break
            if isinstance(ret, int):
                file = ret
    else:
        while True:
            cmd = input("*"*80+"\nenter command:\n")
            ret = execute_cmd(cmd,mode)
            if not ret:
                break

    if file != 0: return file


if __name__ == '__main__':
    run(0)
'''
join 255.255.255.255
lookup 255.255.255.255
'''

'''
123
98273
29386
2327
0438785t03457304
'''