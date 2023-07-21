from hashlib import sha1
ID_LEN = 30

def mod(val, addr):
    return (val+addr) % (1 << ID_LEN)

def get_id(key: str):
    hash = sha1()
    hash.update(key.encode())
    hash = int(hash.hexdigest(), 16) % (1 << ID_LEN)
    return hash

def comp_id(base, i, s = 1):
    return (base + (1 << i)*s) % (1 << ID_LEN)

def interval_cmp(val, left, right) -> bool:
    if right <= left:
        if val < right:
            val += (1 << ID_LEN)
        right += (1 << ID_LEN)
    return val >= left and val < right


class logger(object):
    def __init__(self) -> None:
        pass

    def log_key(self, node, key):
        print("KEY-VALUE INFO:")
        id = get_id(key)
        if id not in node.storage.keys():
            print("\tkey {} not found".format(key))
        else:
            print("\tkey {} found".format(key))
            print("\tSERVER:\t{}".format(node.id))
            print("\tIDENTIFIER:\t{}".format(id))
            print("\tVALUE:\t{}".format(node.storage[id]))

    def log_node(self, node):
        print("SERVER NODE INFO:")
        print("\tIDENTIFIER:\t{}".format(node.id))
        print("\tIP ADDR:\t{}".format(node.key))
        print("\tFINGER TABLE:")
        print("\t\tSTART\tINTERVAL\tSUCCESSOR")
        st = node.finger[0]['start']
        fi = node.finger
        for i in range(ID_LEN-1):
            print("\t\t{}\t[{}-{})\t\t{}".format(fi[i]['start'], fi[i]['start'], fi[i+1]['start'], fi[i]['succ']))
        print("\t\t{}\t[{}-{})\t\t{}\n".format(fi[ID_LEN-1]['start'], fi[ID_LEN-1]['start'], mod(st,-1), fi[ID_LEN-1]['succ']))


loggers = logger()

class node_handler(object):
    def __init__(self, hop = True,**kwargs) -> None:
        self.cur_hop_cnt = 0
        # self.hop = hop
        self.hop_cnt = dict()

    def reset(self, item = None):
        if item:
            if item in self.hop_cnt.keys():
                del self.hop_cnt[item]
            else:
                print("WARNING: {} do not exists".format(item))
        else:
            self.hop_cnt = dict()

    def count(self):
        self.cur_hop_cnt += 1

    def node_stat(self, id):
        if id not in self.hop_cnt.keys():
            self.hop_cnt[id] = list()
        self.hop_cnt[id].append(self.cur_hop_cnt)
        self.cur_hop_cnt = 0
