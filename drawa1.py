import matplotlib.pyplot as plt
import numpy as np

from constants import *
from lg import LG
from as_ import AS


def sumzip(*items):
    return [sum(values) for values in zip(*items)]

def autolabel(containers, len_, texts, ax):
    '''
    '''
    heights = []
    for i, rect in enumerate(containers[0]):
        height = sum([rects[i].get_height() for rects in containers])#not sure what happen when h is 0
        ax.text(rect.get_x()+rect.get_width()/2., 0.08+height, texts[i],
                ha='center', va='bottom', rotation='vertical')


def draw_one_page_figure(lgs, texts, title):
    '''
    '''
    f, axarr = plt.subplots(2, sharex=True)
    l_lg_ids = []
    l_internal = []
    l_unknown = []
    l_c2p = []
    l_p2c = []
    l_p2p = []
    colors = ['r','g','b','c','y']
    for lg_ in lgs:
        l_lg_ids.append(lg_.get_attr(ID))

        values = lg_.get_attr(NUM_REL)
        l_internal.append(values[0])
        l_unknown.append(values[1])
        l_c2p.append(values[2])
        l_p2c.append(values[3])
        l_p2p.append(values[4])

    xs = range(len(l_lg_ids)) #get the number of lgs involved
    width = 0.8 #default is 0.8
    p1 = axarr[1].bar(xs, l_p2p, width=width, color = colors[4])
    p2 = axarr[1].bar(xs, l_p2c, width=width, color = colors[3], bottom=sumzip(l_p2p))
    p3 = axarr[1].bar(xs, l_c2p, width=width, color = colors[2], bottom=sumzip(l_p2p, l_p2c))
    p4 = axarr[1].bar(xs, l_unknown, width=width, color = colors[1], bottom=sumzip(l_p2p, l_p2c, l_c2p))
    p5 = axarr[1].bar(xs, l_internal, width=width, color = colors[0], bottom=sumzip(l_p2p, l_p2c, l_c2p, l_unknown))
    axarr[1].legend((p5[0], p4[0], p3[0], p2[0], p1[0]), ("ibgp", "unknown", "c2p", "p2c", "p2p"))
    #plt.xticks(np.arange(len(l_lg_ids))+width/2,l_lg_ids,rotation='vertical',fontsize=3)#shift x-axis
    plt.xticks(np.arange(len(l_lg_ids)),l_lg_ids,rotation='vertical',fontsize=6)#shift x-axis


    autolabel((p1,p2,p3,p4,p5), len(l_lg_ids), texts, axarr[1])

    ##############part 2
    nan = float("NaN")
    means = [[] for i in range(5)]
    stds = [[] for i in range(5)]
    unit = 0.15
    for lg_ in lgs:
        rel_prefixes = lg_.get_attr(LIST_PREFIX)
        for i, nums in enumerate(rel_prefixes):
            if len(nums) == 0:
                means[i].append(nan)
                stds[i].append(nan)
            else:
                means[i].append(np.mean(nums))
                stds[i].append(np.std(nums))

    for i in range(5):
        #axarr[0].errorbar(np.arange(len(l_lg_ids))+width/2+unit*i,\
        axarr[0].errorbar(np.arange(len(l_lg_ids))+unit*i,\
                means[i],xerr=0, yerr=stds[i],fmt='o', color=colors[i])
                #means[i+2],xerr=0, yerr=stds[i+2],fmt='o', color=colors[i+2])
    #axarr[0].errorbar([0.55, 1.4, 2.55],[1, nan, 2],xerr=0, yerr=[0.5, nan, 0.3],fmt='o')
    axarr[0].set_yscale('log')
    axarr[0].set_ylim((1e-1,1e6))



    plt.subplots_adjust(hspace = 0.03)
    axarr[0].margins(0.02,0.3)
    #axarr[1].margins(0.03,0.4)

    #plt.tight_layout()
    #plt.savefig("test.eps")
    axarr[0].set_title(title)
    axarr[0].set_ylabel("mean of num of prefixes advertised")
    axarr[1].set_ylabel("number of neighbors")
    plt.show()

def one_page_figure_one_lg(ases):
    '''
    '''

    lgs = []
    ases_in_use = []
    for as_ in ases:
        if len(as_) == 1:
            lgs.append(as_.get_attr(LGS)[0])
            ases_in_use.append(as_)
    lgs_sorted = sorted(lgs, key=lambda x: x.size_nei(), reverse=True)
    title = "ASes with one LG"

    texts = []
    for as_ in ases_in_use:
        type_ = as_.get_attr(INFO)[1]
        tier = as_.get_attr(INFO)[2]
        if tier == "\\N": tier = "na"
        texts.append(type_+"--"+tier)

    draw_one_page_figure(lgs_sorted, texts, title)


def one_page_figure_two_lgs(ases):
    '''
    '''

    ases_in_use = []
    for as_ in ases:
        if len(as_)==2:
            ases_in_use.append(as_)
    ases_in_use = sorted(ases_in_use, key=lambda x:x.get_attr(LGS)[0].size_nei() + x.get_attr(LGS)[1].size_nei(), reverse=True )

    lgs = []
    for as_ in ases_in_use:
        lgs_tmp = sorted(as_.get_attr(LGS), key=lambda x:x.size_nei(), reverse=True)
        for lg_ in lgs_tmp:
            lgs.append(lg_)
        lgs.append(LG.dummy())    #dummy LG to separate ASes
    
    texts = []
    for as_ in ases_in_use:
        type_ = as_.get_attr(INFO)[1]
        tier = as_.get_attr(INFO)[2]
        if tier == "\\N": tier = "na"
        texts.append(type_+"--"+tier)
        texts += ["" for i in range(len(as_)-1 +1)]

    title = "ASes with two LGs"
    draw_one_page_figure(lgs, texts, title)

def one_page_figure_mul_lgs(ases):
    '''
    using LG.dummy() to control
    '''

    ases_in_use = []
    for as_ in ases:
        if len(as_)>2 and len(as_)<15:
            ases_in_use.append(as_)
    ases_in_use = sorted(ases_in_use, key=lambda x:len(x) )

    lgs = []
    for as_ in ases_in_use:
        lgs_tmp = sorted(as_.get_attr(LGS), key=lambda x:x.size_nei(), reverse=True)
        for lg_ in lgs_tmp:
            lgs.append(lg_)
        lgs.append(LG.dummy())    #dummy LG to separate ASes
    
    texts = []
    for as_ in ases_in_use:
        type_ = as_.get_attr(INFO)[1]
        tier = as_.get_attr(INFO)[2]
        if tier == "\\N": tier = "na"
        texts.append(type_+"--"+tier)
        texts += ["" for i in range(len(as_)-1 +1)]

    title = "ASes with multiple LGs"
    draw_one_page_figure(lgs, texts, title)

def one_page_figure_twenty_more_lgs(ases):
    '''
    using LG.dummy() to control
    '''

    ases_in_use = []
    for as_ in ases:
        if len(as_)>20:
            ases_in_use.append(as_)
    ases_in_use = sorted(ases_in_use, key=lambda x:len(x) )

    lgs = []
    for as_ in ases_in_use:
        lgs_tmp = sorted(as_.get_attr(LGS), key=lambda x:x.size_nei(), reverse=True)
        for lg_ in lgs_tmp:
            lgs.append(lg_)
        lgs.append(LG.dummy())    #dummy LG to separate ASes
    
    texts = []
    for as_ in ases_in_use:
        type_ = as_.get_attr(INFO)[1]
        tier = as_.get_attr(INFO)[2]
        if tier == "\\N": tier = "na"
        texts.append(type_+"--"+tier)
        texts += ["" for i in range(len(as_)-1 +1)]

    title = "ASes with twenty or more LGs"
    draw_one_page_figure(lgs, texts, title)
