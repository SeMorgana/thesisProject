#drawing for methdology section
import matplotlib.pyplot as plt
import numpy as np
import powerlaw as pl

from constants import *
from lg import LG
from as_ import AS
from drawa1 import sumzip

def draw_as_count(ases, mode):
    '''
    args:
        ases:
            list of AS objects
        mode:
            1-type
            2-tier
    '''
    assert (mode == 1 or mode ==2)
    kinds = set()
    d = dict()#d[kinds]->list of numbers
    for as_ in ases:
        kind = as_.get_attr(INFO)[mode]
        if kind in d:
            d[kind].append(len(as_))
        else:
            d[kind] = [len(as_)]
    bins = len(max(ases, key=len))
    #print bins
    xs = range(bins+1)
    legends = []
    rets = []
    used = []
    width=0.8
    colors = ['r','g','b','c','y','k','w']
    assert (len(d) <= len(colors))
    for i,t in enumerate(d):
        legends.append(t)
        ys,_ = np.histogram(d[t],range(bins+2))
        ret = plt.bar(xs, ys, width=width, bottom=sumzip(*used) or None, color=colors[i])
        rets.append(ret[0])
        used.append(list(ys))

    plt.legend(tuple(rets), tuple(legends))
    kind = ''
    if mode == 1:
        kind = "type"
    elif mode == 2:
        kind = "tier"
    #plt.title('AS cout based on number of LGs contained, with '+ kind)
    plt.xlabel('number of LGs')
    plt.ylabel('number of ASes having corrsponding number of LGs')
    plt.show()

def draw_as_count_by_type(ases):
    '''
    '''
    draw_as_count(ases, 1)
    types = set()
    return


def draw_as_count_by_tier(ases):
    '''
    '''
    draw_as_count(ases, 2)
    types = set()
    return



def draw_cdf(ases, title, lower=-1, upper=100):
    '''
    args:
        ases:
            list of AS objects
        title:
            title of the figure
        lower:
            lower bound of num of LGs in the ASes to be selected
        upper:
            upper bound of num of LGs in the ASes to be selected
    '''

    ases_in_use = []
    for as_ in ases:
        if len(as_) >= lower and len(as_) <= upper:
            ases_in_use.append(as_)

    #plt.title(title)
    plt.xlabel("number of neighbors")
    plt.ylabel("cdf")

    colors = ['r','b','g']
    lis_legend = []
    names = ("BGP","iBGP","eBGP")
    lgs = []
    for as_ in ases_in_use:
        lgs += as_.get_attr(LGS)

    for i in range(len(names)):
        lis = []
        for lg in lgs:
            n = len(lg.get_attr(NEI_SET)[i])
            lis.append(float(n))
        dist,prob = pl.cdf(lis)

        lis_legend.append(plt.scatter(dist,prob,c=colors[i],marker='x'))

    plt.legend(tuple(lis_legend),names,scatterpoints=1,loc="lower right")
    plt.autoscale()
    plt.margins(0.03)
    #plt.title("Degree distribution based on BGP, eBGP, and iBGP neighbors")
    #plt.xlim(0,15000)
    #plt.ylim(0,1)
    plt.show()







def test():
    plt.hist([1,2,3,1], np.arange(5) - 0.5)
    plt.hist([1,1,3,3], np.arange(5) - 0.5, bottom = 3)
    plt.axis([0, 4+1, 0, 9+1])
    plt.show()

if __name__ == "__main__":
    test()
