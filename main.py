import sys

from constants import *
from lg import LG
from as_ import AS
import utility
import drawa1
import drawa2
import drawm


def test():
    lg1 = LG("1.1.1.1")
    lg2 = LG("1.1.1.1")
    lg3 = LG.dummy()
    print lg3
    print lg3.get_attr(NUM_REL)
    print lg3.get_attr(LIST_PREFIX)
    #print lg1 == lg2
    s = set()
    s.add(lg1)
    s.add(lg2)
    #print s


def main():
    if len(sys.argv) != 6: #
        print "input files: output_3a, ucla_rel, as_name_type_tier_rank, ip_to_coords, prefix_to_coords_dict"
        sys.exit()

    output_3a = sys.argv[1]
    ucla_rel = sys.argv[2]
    as_nttr = sys.argv[3]
    ip_coords = sys.argv[4]
    prefix_to_coords_dict = sys.argv[5]

    #get (set(neighbors), set(internal neighbors), set(external neighbors)) for each LG
    d_as_lg_set = utility.parse(output_3a)
    ases = []
    for asn in d_as_lg_set:
        lgs = []
        for as_lg_str in d_as_lg_set[asn]:
            lg_ = LG(as_lg_str)
            lg_.set_attr(NEI_SET, d_as_lg_set[asn][as_lg_str])
            lgs.append(lg_)
        
        as_  = AS(asn, lgs=lgs)
        ases.append(as_)

    #get (#i, #unknown, #cp, #pc, #p2p) for each LG
    d_as_pair_type = utility.build_rel_dict(ucla_rel)
    utility.get_num_rel(ases, d_as_pair_type)


    #get ([],[],[],[],[])
    d_type_ip_num_prefix = utility.build_num_prefix_d(output_3a, d_as_pair_type)
    utility.get_num_prefix_per_type(ases,d_type_ip_num_prefix)

    #get (name, type, tier, rank) for each AS
    d_nttr = utility.build_as_name_type_tier_rank_d(as_nttr)
    utility.get_nttr(ases,d_nttr)

    #get (lat,lon) for each LG
    d_iill = utility.build_ipint_lat_lon_d(ip_coords)
    utility.get_lat_lon(ases, d_iill)

    #build dictionary mapping prefixes in use to (lat,lon)
    d_prefix_lat_lon = utility.build_prefix_lat_lon_d(prefix_to_coords_dict)




    #test cases
    #as_ = ases[0]
    as_ = find_as("28929", ases)[0]
    lg_ = as_.get_attr(LGS)[0]
    #lg__ = as_.get_attr(LGS)[1]
    t1 =  lg_.get_attr(NEI_SET)[2]
    t2 =  lg_.get_attr(NUM_REL)
    t3 = lg_.get_attr(LIST_PREFIX)
    t4 = as_.get_attr(INFO)
    t5 = lg_.get_attr(LAT_LON)
    print lg_.get_attr(ID)
    print lg_.distance(lg_)
    #lg_.update_prefix_as_path()
    #print lg_.get_prefixes(),len(lg_.get_prefixes())
    #print lg_.get_as_paths("1.0.64.0/18")
    #print lg_.get_as_paths_set("1.0.64.0/18")
    #print t1
    #print t2
    #print t4
    #validate(ases)

    ###########################
    #drawing for analysis part#
    ###########################
    #drawa1.one_page_figure_one_lg(ases) 
    #drawa1.one_page_figure_two_lgs(ases) 
    #drawa1.one_page_figure_mul_lgs(ases) 
    #drawa1.one_page_figure_twenty_more_lgs(ases) 


    #############################
    #drawing for methdology part#
    #############################
    #drawm.draw_as_count_by_type(ases)
    #drawm.draw_as_count_by_tier(ases)


    ##################################
    #drawing for methdology part: cdf#
    ##################################
    #drawm.draw_cdf(ases,"Degree distribution based on BGP, eBGP, and iBGP neighbors")
    #drawm.draw_cdf(ases,"Degree distribution based on BGP, eBGP, and iBGP neighbors(ASes with 1 or 2 LGs)", 1, 2)
    #drawm.draw_cdf(ases,"Degree distribution based on BGP, eBGP, and iBGP neighbors(ASes with >=3 LGs)", 3)


    
    ########################################
    #drawing for analysis part2: J.I indexes#
    ########################################
    #drawa2.draw_cdf_JI_lg_level(ases,ALL) 
    #drawa2.draw_cdf_JI_lg_level(ases,TYPE) 
    #drawa2.draw_cdf_JI_lg_level(ases,TIER) 

    drawa2.draw_cdf_JI_prefix_level(ases, TYPE) 
    #drawa2.draw_cdf_JI_prefix_level(ases, TIER) 


    ######################################################
    #drawing for analysis part2: geo distance vs fraction#
    ######################################################
    #drawa2.draw_geo_fraction(ases) 
    #drawa2.draw_geo_fraction(ases,TYPE) 
    #drawa2.draw_geo_fraction(ases,TIER) 

    #############################################
    #drawing for analysis part2: AS/geo distance#
    #############################################
    #drawa2.draw_avg_geo_as_dist(ases, d_prefix_lat_lon, GEODIST)
    #drawa2.draw_avg_geo_as_dist(ases, d_prefix_lat_lon, ASDIST)


    #for checking particular LGs for Figure 8 - Figure 11
    '''
    as_ = find_as("8402",ases)[0]
    for lg_ in sorted(getattr(as_,LGS),key=lambda x: len(getattr(x,NEI_SET)[0]), reverse=True):
        print ''
        print lg_,getattr(lg_, NUM_REL)
        print "unknown:", getattr(lg_,LIST_PREFIX)[1]
        print "c2p:", getattr(lg_,LIST_PREFIX)[2]
        print "p2c:", getattr(lg_,LIST_PREFIX)[3]
        print "p2p:", getattr(lg_,LIST_PREFIX)[4]
        print ''
    '''

    '''
    slg = set()
    sas = set()
    for i,as_ in enumerate(ases):
        print i
        for lg_ in as_.get_attr(LGS):
            lg_.update_prefix_as_path()
            for p in lg_.get_prefixes():
                ap = lg_.get_as_paths(p)
                if len(ap) >= 2:
                    sas.add(as_)
                    slg.add(lg_)
                    #print lg_.get_attr(ID),len(ap)
            lg_.release()
    print len(slg),len(sas)
    '''

    '''
    #print ASes' info
    tmp = sorted(ases, key = lambda x:x.get_attr(INFO)[1])
    for a in tmp:
        info = a.get_attr(INFO)
        name = info[0]
        type_ = info[1]
        tier = info[2]
        asn = a.get_attr(ASN)
        num_lgs = len(a)
        print "%s,%s,%s,%s,%s" % (asn,name,num_lgs,type_,tier)
    '''



        

def validate(ases):
    for as_ in ases:
        as_.validate()

def find_as(asn, ases):
    return filter(lambda x: x.get_attr(ASN)==asn, ases)

def print_lg(ases):
    for as_ in ases:
        for lg_ in as_.get_attr(LGS):
            print lg_,
            print lg_.get_ip_int()


if __name__ == "__main__":
    main()
    #test()
