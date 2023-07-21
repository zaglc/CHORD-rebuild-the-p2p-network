import random
from utils import * 
from myclass import *
from simulate import execute_cmd

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

    def multi_hop_box(self, k = 4, q = int(3e4)):
        execute_cmd("clear")
        CHORD.verbose = False
        for j in range(k,k+10):
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
        m1 = np.load("./visualize/data_optm.npy",allow_pickle=True)
        m2 = np.load("./visualize/data_orig.npy",allow_pickle=True)
        plt.figure(figsize=(8,6))
        print("pre:",m2)
        print("after:",m1)
        k = list(range(2,10))
        plt.plot(k,m2,label="old chord",marker='o', alpha=0.5)
        plt.plot(k,m1,label="new chord",marker='^',linestyle='--')
        plt.legend()
        plt.xlabel("Logarithm of N")
        plt.ylabel("Average hops")
        plt.savefig("./visualize/last.png")

if __name__ == "__main__":
    ex = exper()

    # 跳数pdf实验
    ex.average_hop_exp()

    # 多网络跳数统计实验
    # ex.multi_hop_box()

    # 改进查询后画图，数据是提前利用multi_hop_box存储好的
    # ex.modify_lookup()


