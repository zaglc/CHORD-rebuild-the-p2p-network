import random
from utils import * 
from myclass import *
from simulate import execute_cmd
import sys

class exper(object):
    def __init__(self) -> None:
        pass

    def average_hop_exp(self, k = 12, q = int(1e5)):
        execute_cmd("clear")
        CHORD.verbose = True
        nodes = random.sample(range(1<<ID_LEN), 1 << k)
        for i in range(len(nodes)):
            cmd = "join {} 1".format(str(nodes[i]))
            execute_cmd(cmd)

        quiries = [random.randint(0, (1<<ID_LEN)-1) for _ in range(q)]
        CHORD.verbose = False
        for i in range(len(quiries)):
            cmd = "lookup {}".format(quiries[i])
            execute_cmd(cmd)
        execute_cmd("plot 1")

    def multi_hop_box(self, optimize = True, k = 4, rg = 10, q = int(3e4)):
        print("k:{}-{} to be process".format(k, k+rg))
        execute_cmd("clear")
        CHORD.optimize = optimize
        CHORD.verbose = False
        for j in range(k,k+rg):
            print("{} processing...".format(j))
            CHORD.verbose = True
            nodes = random.sample(range(1<<ID_LEN), 1 << j)
            for i in range(len(nodes)):
                cmd = "join {} 1".format(str(nodes[i]))
                execute_cmd(cmd)

            quiries = [random.randint(0, (1<<ID_LEN)-1) for _ in range(q)]
            CHORD.verbose = False
            for i in range(len(quiries)):
                cmd = "lookup {}".format(quiries[i])
                execute_cmd(cmd)
            execute_cmd("add_hop_entry {}".format(j))
        execute_cmd("plot 2")

    def modify_lookup(self):
        if not os.path.exists("./data/data_optm.npy"):
            print("please run <python experiment.py multihop 1> first")
            return
        if not os.path.exists("./data/data_orig.npy"):
            print("please run <python experiment.py multihop 0> first")
            return
        
        m1 = np.load("./data/data_optm.npy",allow_pickle=True)
        m2 = np.load("./data/data_orig.npy",allow_pickle=True)
        plt.figure(figsize=(8,6))
        k = list(range(2,100))
        plt.plot(k[:len(m2)],m2,label="old chord",marker='o', alpha=0.5)
        plt.plot(k[:len(m1)],m1,label="new chord",marker='^',linestyle='--')
        plt.legend()
        plt.xlabel("Logarithm of N")
        plt.ylabel("Average hops")
        plt.savefig("./figs/last.png")

if __name__ == "__main__":
    argv = sys.argv
    ex = exper()

    if argv[1] == "average":
        # 跳数pdf实验
        ex.average_hop_exp(int(argv[2]))

    elif argv[1] == "multihop":
        # 多网络跳数统计实验
        # print(bool(int(argv[2])))
        ex.multi_hop_box(bool(int(argv[2])), int(argv[3]), int(argv[4]))

    elif argv[1] == "modify":
        # 改进查询后画图，数据是提前利用multi_hop_box存储好的
        ex.modify_lookup()

    else:
        print("no corresponding experiment implemented, only: {}".format(["average", "multihop", "modify"]))


