import numpy as np
import random
from utils import *
import matplotlib.pyplot as plt
from functools import reduce
import copy, math , os
import matplotlib.patches as mpatches
import matplotlib.lines as lines
import networkx as nx

# global nodelist
nodelist = dict()

class node(object):
    def __init__(self, key) -> None:
        self.key = key
        self.id = get_id(key)
        self.predecessor = None
        self.finger = list([{} for _ in range(ID_LEN)])
        self.storage = dict()

    def _set_prede(self, pred):
        self.predecessor = pred

    def _get_succ(self):
        return self.finger[0]['succ']

    def _set_finger(self, i, start, succ):
        st = self.finger[i]['start'] if start is None else start
        self.finger[i] = {'start':st, 'succ': succ}

    # lookup
    def find_successor(self, id, visual = False) -> int:
        # 统计跳数
        if not CHORD.verbose:
            CHORD.hd.count()
        
        # 存图
        if visual:
            CHORD.image_stat(
                hightlight_node_id = self.id,
                is_terminal = False,
                op = "lookup",
                target = id
                )
            
        '''改进'''
        if interval_cmp(id, mod(self.predecessor,1), mod(self.id,1)):
            ret = self.id
        
        elif not interval_cmp(id, mod(self.id,1), mod(self._get_succ(),1)):
            n_prede = self.find_predecessor(id, visual)
            ret = nodelist[n_prede]._get_succ()
        else:
            ret = self._get_succ()
        if not CHORD.verbose:
            CHORD.hd.node_stat(id)
        
        # 存图
        if visual:
            CHORD.image_stat(
                hightlight_node_id = ret,
                is_terminal = True,
                op = "lookup",
                target = id
                )
        return ret

    def find_predecessor(self, id, visual = False) -> int:
        n_prede = self.id
        while not interval_cmp(id, mod(n_prede,1), mod(nodelist[n_prede]._get_succ(),1)):
        # while id not in [nodelist[n_prede]._get_succ(), n_prede]:
            n_prede = nodelist[n_prede].closest_preceding_finger(id)
            
            # 存图
            if visual:
                CHORD.image_stat(
                    hightlight_node_id = n_prede,
                    is_terminal = False,
                    op = "lookup",
                    target = id
                    )
            
            # 统计跳数
            if not CHORD.verbose:
                CHORD.hd.count()
        return n_prede

    def closest_preceding_finger(self, id) -> int:
        for i in range(ID_LEN, 0, -1):
            if interval_cmp(self.finger[i-1]['succ'], mod(self.id,+1), id):
                return self.finger[i-1]['succ']
        return self.id
    
    # transfer
    # 从succ转移到self
    def trans_from(self, succ):
        if self.id == succ:
            return
        elms = list(nodelist[succ].storage.keys())
        for elm in elms:
            if interval_cmp(elm, self.predecessor+1, self.id+1):
                self.storage[elm] = nodelist[succ].storage[elm]
                del nodelist[succ].storage[elm]

    # 从self转移到succ
    def trans_to(self, succ):
        if self.id == succ:
            return
        for elm in self.storage:
            nodelist[succ].storage[elm] = self.storage[elm]
        self.storage = dict()

    # join
    def join(self, n_prede):
        # 是从某个节点加进去的
        if n_prede >= 0:
            self.init_finger_table(n_prede)
            self.update_others()
            self.trans_from(self._get_succ())
        
        # n_prede无效，就新建一个表
        else:
            for i in range(0, ID_LEN):
                self._set_finger(i, comp_id(self.id, i), self.id)
            self._set_prede(self.id)

    def init_finger_table(self, n_prede):
        nd = nodelist[n_prede].find_successor(comp_id(self.id, 0))

        self._set_finger(0, comp_id(self.id, 0), nd)
        self._set_prede(nodelist[nd].predecessor)
        nodelist[nd]._set_prede(self.id)

        for i in range(1, ID_LEN):
            new_start = comp_id(self.id, i)
            if interval_cmp(new_start, self.id, mod(self.finger[i-1]['succ'],1)):
                self._set_finger(i, new_start, self.finger[i-1]['succ'])
            else:
                ndd = nodelist[n_prede].find_successor(new_start)
                # 这个时候新点还没加到旧点的finger里面
                # 直接find，如果正确结果应当是新点，那肯定找不到
                if interval_cmp(self.id, new_start, ndd) and new_start != ndd:
                    ndd = self.id
                self._set_finger(i, new_start, ndd)
        # loggers.log_node(nodelist[self.id])

    def update_others(self):
        new_id = self.id
        for i in range(ID_LEN):
            idd = comp_id(self.id, i, -1)
            p = self.find_predecessor(idd)
            # CHORD.hd.node_stat(idd)
            
            # 如果idd正好是个node，那么它肯定要改
            if nodelist[p]._get_succ() == idd:
                p = idd
            #
            if p == new_id: continue
            #
            nodelist[p].update_finger_table(new_id, i+1)

    def update_finger_table(self, s, i):
        # 和论文不同
        if interval_cmp(s, self.finger[i-1]['start'], self.finger[i-1]['succ']) and self.finger[i-1]['start']!=self.finger[i-1]['succ']:
            self._set_finger(i-1, None, s)
            p = self.predecessor
            nodelist[p].update_finger_table(s, i)

    # leave
    def leave(self):
        nodelist[self._get_succ()]._set_prede(self.predecessor)
        self.update_others_leave()
        self.trans_to(self._get_succ())

    def update_others_leave(self):
        new_id = self._get_succ()
        
        # 最后一个点，不用更新
        if new_id == self.id: return

        for i in range(ID_LEN):
            idd = comp_id(self.id, i, -1)
            p = self.find_predecessor(idd)
            # CHORD.hd.node_stat(idd)
            ####
            if nodelist[p]._get_succ() == idd:
                p = idd
            ####
            nodelist[p].update_finger_table_leave(new_id, i+1, self.id)

    def update_finger_table_leave(self, s, i, del_id):
        if self.finger[i-1]['succ'] == del_id:
            self._set_finger(i-1, None, s)
            p = self.predecessor
            nodelist[p].update_finger_table_leave(s, i, del_id)

    # insert, 也可以modify
    def insert(self, id, val):
        nd = self.find_successor(get_id(id))
        nodelist[nd].storage[get_id(id)] = val

    # delete
    def delete(self, id):
        nd = self.find_successor(get_id(id))
        del nodelist[nd].storage[get_id(id)]


class chord(object):
    def __init__(self, **kwargs) -> None:
        self.hd = node_handler(kwargs)
        self.verbose = True
        self.average_hop_storage = dict()
        self.visual_step = 0
        self.optimize = False

    def lookup(self, key, visual = False):
        if len(nodelist) == 0 and self.verbose:
            print("WARNING: no server, omit lookup\n")
            return
        
        if visual and ID_LEN > 5:
            print("Unable to visualize, max m :5")
            visual = False

        k = random.sample(nodelist.keys(), 1)[0]
        id = nodelist[k].find_successor(get_id(key), visual)
        if self.verbose:
            loggers.log_key(nodelist[id], key)
            if id == get_id(key):
                loggers.log_node(nodelist[id])

    def insert(self, key, val):
        if len(nodelist) == 0 and self.verbose:
            print("WARNING: no server, omit insert\n")
            return
        k = random.sample(nodelist.keys(), 1)[0]
        nodelist[k].insert(key, val)

    def delete(self, key):
        if len(nodelist) == 0 and self.verbose:
            print("WARNING: no server, omit delete\n")
            return
        k = random.sample(nodelist.keys(), 1)[0]
        nodelist[k].delete(key)

    def join(self, nkey, is_id = False):
        ndd = nkey if is_id else get_id(nkey)
        if ndd in nodelist.keys() and self.verbose:
            print("WARNING: the server {} exists, omit join\n".format(nkey))
            return
        
        k = -1 if len(nodelist) == 0 else random.sample(nodelist.keys(), 1)[0]
        new_node = node(nkey)
        nodelist[ndd] = new_node
        nodelist[ndd].join(k)

    def leave(self, nkey):
        if get_id(nkey) not in nodelist.keys() and self.verbose:
            print("WARNING: no found server:{}, omit leave\n".format(nkey))
            return 
        nodelist[get_id(nkey)].leave()
        del nodelist[get_id(nkey)]

    def clear(self):
        keys = list(nodelist.keys())
        for e in keys:
            del nodelist[e]

    def show(self):
        nodeid = nodelist.keys()
        if self.verbose:
            for id in nodeid:
                loggers.log_node(nodelist[id])

    def plot_hop_pdf(self):
        hop_cnt = reduce(lambda x,y:x+y, self.hd.hop_cnt.values())
        hop_cnt = sorted(hop_cnt)
        newd = dict()
        for e in hop_cnt:
            if e not in newd:
                newd[e] = 1
            else:
                newd[e] += 1
        sums = sum(list(newd.values()))
        plt.figure(figsize=(10,7))
        plt.plot(list(newd.keys()), [i/sums for i in list(newd.values())])
        plt.xlabel("Path len.")
        plt.ylabel("Probability")
        plt.savefig("./figs/pdf.png")

    def set_ahs(self,nds):
        d = reduce(lambda x,y:x+y, list(self.hd.hop_cnt.values()))
        d = sorted(d)
        per1 = d[int(len(d)/100*1)]
        per99 = d[int(len(d)/100*99)]
        mean = sum(d)/len(d)
        self.average_hop_storage[nds] = {"1":per1,"99":per99,"m":mean}

    def plot_muti_scale_hop_boxLine(self):
        stra = self.average_hop_storage
        labels = list(stra.keys())
        per1 = [i["1"] for i in list(stra.values())]
        per99 = [i["99"] for i in list(stra.values())]
        mean = [i["m"] for i in list(stra.values())]
        fig = plt.figure(figsize=(10,7))

        ax = fig.add_subplot(111)
        for i in range(len(labels)):
            ax.plot([labels[i], labels[i]],[per1[i], per99[i]], c='k')
        ax.scatter(labels, per1, marker="v",s=50,c = 'k')
        ax.scatter(labels, per99, marker="^",s=50,c = 'k')
        ax.scatter(labels, mean, marker="s",s=100,c = 'k')

        plt.xlabel("LOG(N)")
        plt.ylabel("HOP nums.")
        plt.savefig("./figs/box.png")
        np.save("./visualize/data.npy",np.array(mean))

    def image_stat(self, **kwargs):
        self.plot_once(step=self.visual_step, kwargs=kwargs)
        self.visual_step += 1
    
    def plot_once(self, **kwargs):
        hightlight_node_id = kwargs["kwargs"]["hightlight_node_id"]
        is_terminal = kwargs["kwargs"]["is_terminal"]
        op = kwargs["kwargs"]["op"]
        step = kwargs["step"]
        target = kwargs["kwargs"]["target"]
        st = 0.04
        G=nx.Graph()
        position, labeldict={}, {}
        ncolor, nsize=[], []
        num=2**ID_LEN
        keylist=list(range(num))
        for i in range (num):
            G.add_edge(i,(i+1)%num)
            position[i]=[math.cos(2*math.pi*i/num),math.sin(2*math.pi*i/num)+st/2]
            labeldict[i]=i
        for key in keylist:
            ncolor.append('k')
            nsize.append(80)
        for node in list(nodelist.values()):
            id=node.id
            if id==hightlight_node_id:
                if is_terminal:
                    ncolor[id]=('g')
                else:
                    ncolor[id]=('r')
            else:
                ncolor[id]=('b')
            nsize[id]=300

        plt.ion()
        plt.figure(figsize=(8,8))
        nx.draw(G,nodelist=keylist,pos=position,node_color=ncolor,node_size=nsize)
        idx = keylist.index(target)
        plt.scatter(position[idx][0],position[idx][1]+st/2,marker='^',s=1000,alpha=0.5)
        plt.text(-0.17,-0.13,str(step+1),fontsize=100)
        for i in range(num):
            plt.text(0.85*math.cos(2*math.pi*i/num)-st,0.85*math.sin(2*math.pi*i/num),str(i),fontsize=20)
        
        if not os.path.exists("./visualize/{}_{}_{}".format(ID_LEN, op, target)):
            os.mkdir("./visualize/{}_{}_{}".format(ID_LEN, op, target))
        plt.savefig("./visualize/{}_{}_{}/{}".format(ID_LEN, op, target, step))
        plt.close()

CHORD = chord()
