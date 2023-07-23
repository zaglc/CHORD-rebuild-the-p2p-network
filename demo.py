from myclass import *
from utils import *
from simulate import run
import os
import matplotlib.animation as animation
import matplotlib.pyplot as plt
import sys

def main(argv):
    script = argv[1]#"./scripts.txt"
    ret = run(1, script)
    # base = argv[2]#"4_lookup_2"
    assert isinstance(ret, int)
    base = "{}_lookup_{}".format(ID_LEN, get_id(str(ret-1)))
    fig, ax = plt.subplots(1,1,figsize = (10,10))
    imglist = []

    if not os.path.exists("./visualize"):
        os.mkdir("./visualize")
    for i in os.listdir("./visualize/{}".format(base)):
        ax.set_axis_off()
        if i[0] == 't':
            continue
        pt = os.path.join("./visualize/{}".format(base),i)
        im = ax.imshow(plt.imread(pt), animated = True)
        imglist.append([im])

    ani = animation.ArtistAnimation(fig, imglist, interval=2000)
    ani.save("./visualize/{}/total.gif".format(base),dpi = 800)
if __name__ == '__main__':
    main(sys.argv)

