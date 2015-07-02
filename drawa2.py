import matplotlib.pyplot as plt
import numpy as np
import powerlaw as pl
import itertools
import math
import geopy.distance

from constants import *
from lg import LG
from as_ import AS
from utility import JI


#TODO: 
#[+]   grouping by type, tier
#   pairs with 0 ji value(can be in writeup)
def draw_cdf_JI_lg_level(ases, mode=TYPE):#ALL may not be needed
    '''
    args:
        ases:
            list of AS objects
        mode:
            for grouping: ALL, TIER, or TYPE   #ALL may not be needed
    '''

    as_cands = []
    for as_ in ases:
        if len(as_) >= 2:
            as_cands.append(as_)
            #break

    if mode == ALL:#TODO: this will cause error for now
        ases_in_use = as_cands
        draw_cdf_JI_helper(ases_in_use, mode=mode, color='b', marker='x')

    elif mode == TYPE or mode == TIER:
        choice = 0
        if mode == TYPE:
            choice = 1
        elif mode == TIER:
            choice = 2
        s = set()
        for as_ in as_cands:
            s.add(as_.get_attr(INFO)[choice])
        print s
        colors = ['r','g','b','c','y']
        markers = ['x','+','*','^','v']
        assert (len(s)<=len(colors))
        assert (len(s)<=len(markers))

        lis_legend = []
        names = []
        d = dict()
        for k in s:
            d[k] = []
        for as_ in as_cands:
            k = as_.get_attr(INFO)[choice]
            d[k].append(as_)
        for i,k in enumerate(d):
            p = draw_cdf_JI_helper(d[k], mode=mode, color = colors[i], marker = markers[i])
            lis_legend.append(p)
            names.append(k)
        plt.legend(tuple(lis_legend),names,scatterpoints=1,loc="lower right")
    else:
        print "Wrong!"

    #plt.legend(tuple(lis_legend),names,scatterpoints=1,loc="lower right")
    plt.autoscale()
    plt.margins(0.03)
    plt.title("Jaccard index among LG pairs(" + mode + ")")
    plt.xlabel("J.I.")
    plt.ylabel("cdf")
    plt.savefig("J.I._LG_level("+mode+").eps")
    plt.clf()
    #plt.show()



def draw_cdf_JI_helper(ases_in_use, mode, color, marker): #mode is for title
    #plt.title(title)

    colors = ['b']
    lis_legend = []
    lis = []
    total_dots = 0
    #names = ("BGP","iBGP","eBGP")
    for count,as_ in enumerate(ases_in_use):
        print count,len(as_)
        #c2 = 0
        for lg1,lg2 in itertools.combinations(as_.get_attr(LGS),2):
            total_dots += 1
            #print c2
            #c2 += 1
            lg1.update_prefix_as_path()
            p1 = lg1.get_prefixes()
            lg2.update_prefix_as_path()
            p2 = lg2.get_prefixes()
            lis.append(JI(p1,p2))
            if JI(p1,p2) == 0:
                print lg1,lg2

            lg1.release()
            lg2.release()

    print "total dots",total_dots#658
    dist,prob = pl.cdf(lis)
    #plt.scatter(dist,prob,c='b',marker='x')
    return plt.scatter(dist,prob,c=color,marker=marker)

    '''
    #plt.legend(tuple(lis_legend),names,scatterpoints=1,loc="lower right")
    plt.autoscale()
    plt.margins(0.03)
    plt.title("Jaccard index among LG pairs (" + mode + ")")
    #plt.xlim(0,15000)
    #plt.ylim(0,1)
    plt.savefig("J.I._LG_level("+mode+").eps")
    plt.clf()
    #plt.show()
    '''


#TODO:asn set is a mixture if there are more than one as path for a prefix
#[+]     '?' should be removed when selecting from database
#     grouping
def draw_cdf_JI_prefix_level(ases, mode=TYPE):
    '''
    args:
        ases:
            list of AS objects
    '''
    ases_in_use = []
    ases = sorted(ases, key=len)#for testing purpose
    for as_ in ases:
        if len(as_) >= 2:
            ases_in_use.append(as_)
            if len(ases_in_use) > 3:
                break
    
    #ases_in_use = sorted(ases_in_use, key=len)
    choice = 0
    if mode == TYPE:
        ases_in_use = sorted(ases_in_use, key=lambda x:x.get_attr(INFO)[1])
        choice = 1
    elif mode == TIER:
        ases_in_use = sorted(ases_in_use, key=lambda x:x.get_attr(INFO)[2])
        choice = 2
    else:
        print "Wrong"
        return

    s = set()
    for as_ in ases_in_use:
        s.add(as_.get_attr(INFO)[choice])
    d = dict()
    for k in s:
        d[k] = []
    for as_ in ases_in_use:
        k = as_.get_attr(INFO)[choice]
        d[k].append(as_)

    for k in d:
        print mode,k,len(d[k])
        draw_cdf_JI_prefix_level_helper(d[k], mode=mode, kind = k)



def draw_cdf_JI_prefix_level_helper(ases_in_use, mode=TYPE, kind=""): #no need of ALL
    choice = 1# default to TYPE
    if mode == TYPE:
        choice = 1
    elif mode == TIER:
        choice = 2
    else:
        print "Wrong!"
        return

    f, axarr = plt.subplots(6, sharex=True)
    xticks = []
    y_max = []
    y_mean = []
    y_min = []
    #2nd figure
    ji_lg = []
    #1st figure
    num_p1 = []
    num_p2 = []
    num_overlap = []
    #distance figure
    distances = []

    type_tier_set = set() # to keep track of grouping
    asn_set = set() # to keep track of grouping
    for count,as_ in enumerate(ases_in_use):
        lg1_lg2_list_sorted = list()
        for lg1,lg2 in itertools.combinations(as_.get_attr(LGS),2):
            lg1_lg2_list_sorted.append((lg1,lg2))

        lg1_lg2_list_sorted = sorted(lg1_lg2_list_sorted,key=lambda x:x[0].distance(x[1]))#sort by distance

        for lg1, lg2 in lg1_lg2_list_sorted:
            lg1.update_prefix_as_path()
            p1 = lg1.get_prefixes()
            lg2.update_prefix_as_path()
            p2 = lg2.get_prefixes()
            overlap = p1 & p2
            if len(overlap) == 0:#no overlapping prefixes
                continue

            tmp = []
            ji_lg.append(JI(p1,p2))
            num_p1.append(len(p1))
            num_p2.append(len(p2))
            num_overlap.append(len(overlap))
            for p in overlap:
                s1 = lg1.get_as_paths_set(p)
                s2 = lg2.get_as_paths_set(p)
                tmp.append(JI(s1,s2))
            y_max.append(max(tmp))
            y_mean.append(np.mean(tmp))
            y_min.append(min(tmp))

            #xticks.append(lg1.get_attr(ID) + "--" + lg2.get_attr(ID))
            asn = as_.get_attr(ASN)
            tt = as_.get_attr(INFO)[choice]
            asntt = ""
            if tt not in type_tier_set:
                asntt  = tt+"--"+asn
            elif asn not in asn_set:
                asntt = asn
            type_tier_set.add(tt)
            asn_set.add(asn)

            #if asntt in xticks:
                #xticks.append("")
            #else:
                #xticks.append(asntt)
            xticks.append(asntt)
            distances.append(lg1.distance(lg2))
            
            lg1.release()
            lg2.release()
            print lg1,lg2
        #if count == 3:
        #    break

    xs = range(len(xticks))
    lis_legend = []
    prop_size = 7
    #J.I. AS path
    names = ["J.I. max", "J.I. mean", "J.I. min"]
    lis_legend.append(axarr[5].scatter(xs,y_max,c="r",marker='x'))
    lis_legend.append(axarr[5].scatter(xs,y_mean,c='b',marker='.'))
    axarr[5].plot(xs,y_mean,'b')
    lis_legend.append(axarr[5].scatter(xs,y_min,c='g',marker='x'))
    axarr[5].legend(tuple(lis_legend),names,scatterpoints=1,loc="lower right", prop={"size":prop_size})
    axarr[5].set_ylabel("J.I.(AS path)")
    axarr[5].set_xlabel("LG pair within each AS, with at least 1 overlapping prefix")

    #distance
    axarr[4].scatter(xs,distances,c='k',marker='x')
    axarr[4].plot(xs,distances,'k')
    axarr[4].set_ylabel("distance(km)")

    #J.I. prefix
    axarr[3].scatter(xs,ji_lg,c='y',marker='x')
    axarr[3].plot(xs,ji_lg,'y')
    axarr[3].set_ylabel("J.I. (prefix)")

    #overlap prefixes
    lis_legend = []
    #names = ["#p in LG1",  "#p overlap" , "#p in LG2"]
    names = [ "#p overlap" ]
    #lis_legend.append(axarr[2].scatter(xs,num_p1,c="r",marker='x'))
    lis_legend.append(axarr[2].scatter(xs,num_overlap,c='b',marker='.'))
    axarr[2].plot(xs,num_overlap,'b')
    #lis_legend.append(axarr[2].scatter(xs,num_p2,c='g',marker='x'))
    axarr[2].legend(tuple(lis_legend),names,scatterpoints=1,loc="lower right", prop={"size":prop_size})
    #axarr[2].set_ylabel("prefixes count")
    axarr[2].set_yscale('log')
    axarr[2].set_ylim((1e-1,1e6))
    #axarr[0].set_xlabel("LG pair within each AS, with at least 1 overlapping prefix")

    #prefixes in LG2
    lis_legend = []
    names = ["#p in LG2"]
    #lis_legend.append(axarr[1].scatter(xs,num_p1,c="r",marker='x'))
    #lis_legend.append(axarr[1].scatter(xs,num_overlap,c='b',marker='.'))
    #axarr[1].plot(xs,num_overlap,'b')
    lis_legend.append(axarr[1].scatter(xs,num_p2,c='g',marker='x'))
    axarr[1].plot(xs,num_p2,'g')
    axarr[1].legend(tuple(lis_legend),names,scatterpoints=1,loc="lower right", prop={"size":prop_size})
    axarr[1].set_ylabel("prefixes count")
    axarr[1].set_yscale('log')
    axarr[1].set_ylim((1e-1,1e6))

    #prefixes in LG1
    lis_legend = []
    names = ["#p in LG1"]
    lis_legend.append(axarr[0].scatter(xs,num_p1,c="r",marker='x'))
    axarr[0].plot(xs,num_p1,'r')
    #lis_legend.append(axarr[0].scatter(xs,num_overlap,c='b',marker='.'))
    #axarr[0].plot(xs,num_overlap,'b')
    #lis_legend.append(axarr[0].scatter(xs,num_p2,c='g',marker='x'))
    axarr[0].legend(tuple(lis_legend),names,scatterpoints=1,loc="lower right", prop={"size":prop_size})
    #axarr[0].set_ylabel("prefixes count")
    axarr[0].set_yscale('log')
    axarr[0].set_ylim((1e-1,1e6))
    axarr[0].set_title("prefixes count, J.I. prefixes, J.I. as path for LG pairs"+ "(" + mode + ")(" + kind + ")")

    plt.xticks(np.arange(len(xticks)),xticks,rotation='vertical',fontsize=5)#shift x-axis
    plt.autoscale()
    plt.grid()
    plt.margins(0.06)
    print "total_dots",len(xticks)#571
    plt.show()
    #plt.savefig("test.eps",dpi=196)


#TODO:
#[+]   grouping in one figure
def draw_geo_fraction(ases, mode=ALL):
    '''
    args:
        ases:
            list of AS objects
    '''
    ases_in_use = []
    for as_ in ases:
        if len(as_) >= 2:
            ases_in_use.append(as_)
            #if len(ases_in_use) > 1:
            #    break
    
    #ases_in_use = sorted(ases_in_use, key=len)

    #for color handling
    d_type_ases = dict()
    d_tier_ases = dict()
    for as_ in ases_in_use:
        type_ = as_.get_attr(INFO)[1]
        tier = as_.get_attr(INFO)[2]
        if type_ in d_type_ases:
            d_type_ases[type_].append(as_)
        else:
            d_type_ases[type_] = [as_]

        if tier in d_tier_ases:
            d_tier_ases[tier].append(as_)
        else:
            d_tier_ases[tier] = [as_]
    colors = ['r','g','b','c','y']
    markers = ['x','+','*','^','v']
    assert (len(d_type_ases)<=len(colors))
    assert (len(d_tier_ases)<=len(colors))
    
    if mode == ALL:
        for t,ases in d_type_ases.items():
            draw_geo_fraction_helper(ases, "b", "x")
    elif mode == TYPE:
        lis_legend = []
        names = []
        for i,(t,ases) in enumerate(d_type_ases.items()):
            p, dis,fraction = draw_geo_fraction_helper(ases, colors[i], markers[i])
            if is_nan_list(dis) or is_nan_list(fraction): #the whole type has only nan values,so it's cannot be drawn
                print "invalid type",ases
                continue
            #print dis,fraction
            lis_legend.append(p)
            names.append(t)
        #print tuple(names),lis_legend
        plt.legend(tuple(lis_legend),names,scatterpoints=1,loc="lower right")
    elif mode == TIER:
        lis_legend = []
        names = []
        for i,(t,ases) in enumerate(d_tier_ases.items()):
            p, dis,fraction = draw_geo_fraction_helper(ases, colors[i], markers[i])
            if is_nan_list(dis) or is_nan_list(fraction): #the whole tier has only nan values,so it's cannot be drawn
                print "invalid tier",ases
                continue
            lis_legend.append(p)
            names.append(t)
        plt.legend(tuple(lis_legend),names,scatterpoints=1,loc="lower right")
    else:
        print "Wrong!"
        return

    plt.autoscale()
    plt.margins(0.03)
    plt.xlabel("distance(km)")
    plt.ylabel("fraction")
    plt.title("distance vs fraction of similar paths, among overlapping prefixes("+mode+")")
    plt.savefig("dis_vs_fraction("+mode+").eps")
    plt.clf()
    #plt.show()

#TODO:
#   writeup: some overlap not shown because dis or fraction is all nan
def draw_geo_fraction_helper(ases_in_use, color, marker):
    '''
    args:
        ases_in_use:
            list of ases to be drawn
        color:
            the color in the figure
    return:
        (scatter object, dis, fraction)# as path for this is based on string comparison
    '''
    dis = []
    fraction = []
    for count,as_ in enumerate(ases_in_use):
        print count,len(as_)
        for lg1,lg2 in itertools.combinations(as_.get_attr(LGS),2):

            lg1.update_prefix_as_path()
            p1 = lg1.get_prefixes()
            lg2.update_prefix_as_path()
            p2 = lg2.get_prefixes()
            overlap = p1 & p2
            if len(overlap) == 0:#no overlapping prefixes
                continue

            #get fraction:
            num_all = len(overlap)
            num_same = 0
            for p in overlap:
                ap1 = lg1.get_as_paths(p)
                ap2 = lg2.get_as_paths(p)
                if ap1 == ap2:
                    num_same += 1
            fraction.append(1.0 * num_same / num_all)
            dis.append(lg1.distance(lg2))
            #print lg1, lg2
            #print fraction, dis

            lg1.release()
            lg2.release()

    return plt.scatter(dis,fraction,c=color,marker=marker), dis, fraction


def draw_avg_geo_as_dist(ases, d, mode=GEODIST):
    '''
    args:
        ases:
            list of AS objects
        d: 
            d[prefix in the dataset] -> (lat,lon)
    '''
    ases_in_use = []
    for as_ in ases:
        #if getattr(as_,ASN) != "57629":continue
        if len(as_) >= 2:
            ases_in_use.append(as_)

    lis_legend = []
    le_point5_pairs = []
    larger_point5_pairs  = []

    for count,as_ in enumerate(ases_in_use):
        print count,len(as_)
        for lg1,lg2 in itertools.combinations(as_.get_attr(LGS),2):
            print lg1,lg2
            mean_ji = lg1.mean_ji_aspath(lg2) 
            if math.isnan(mean_ji):#if there is no overlap, then the pair is not used
                continue
            if mean_ji <= 0.5:
                le_point5_pairs.append((lg1,lg2))
            else:
                larger_point5_pairs.append((lg1,lg2))



    print len(le_point5_pairs)
    print len(larger_point5_pairs)
    names = ("J.I.(AS path)<=0.5","J.I.(AS path)>0.5")
    lis_legend.append(draw_avg_geo_as_dist_helper(le_point5_pairs, d, 'b', mode))
    lis_legend.append(draw_avg_geo_as_dist_helper(larger_point5_pairs, d, 'r', mode))

    plt.xlabel("avg "+ mode)
    plt.ylabel("cdf")
    plt.legend(tuple(lis_legend),names,scatterpoints=1,loc="lower right")
    plt.autoscale()
    plt.margins(0.03)
    #plt.show()
    plt.savefig("cdf("+mode+").eps")
    plt.clf()



def draw_avg_geo_as_dist_helper(lg_pairs, d, color, mode):

    values = []
    for lg1,lg2 in lg_pairs:
        lg1.update_prefix_as_path()
        p1 = lg1.get_prefixes()
        lg2.update_prefix_as_path()
        p2 = lg2.get_prefixes()
        overlap = p1 & p2
        if len(overlap) == 0:#no overlapping prefixes
            continue

        if mode == GEODIST:
            for p in overlap:
                coord_p = d[p]
                coord_lg1 = getattr(lg1,LAT_LON)
                coord_lg2 = getattr(lg2,LAT_LON)
                if coord_lg1 == (0.0, 0.0) or coord_lg2 == (0.0, 0.0) or coord_p == (0.0 , 0.0):#if one of the location is unknown
                    continue
                dist1 = geopy.distance.great_circle(coord_lg1,coord_p).km
                dist2 = geopy.distance.great_circle(coord_lg2,coord_p).km
                avg_dist = (dist1+dist2) / 2.0
                #print lg1,lg2,p,avg_dist

                values.append(avg_dist)

        elif mode == ASDIST:
            for p in overlap:
                s1 = lg1.get_as_paths_set(p)
                s2 = lg2.get_as_paths_set(p)
                len1 = len(s1)
                len2 = len(s2)

                avg_asdist = (len1+len2) / 2.0
                #print lg1,lg2,p,avg_asdist

                values.append(avg_asdist)
        else:
            print "wrong!"
            return

        lg1.release()
        lg2.release()

    dist,prob = pl.cdf(values)
    return plt.scatter(dist,prob,c=color,marker='x')



def is_nan_list(l):
    for i in l:
        if not math.isnan(i):
            return False
    return True


