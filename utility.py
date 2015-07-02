from constants import *
import pickle

def parse(file_path):
    '''
    args:
    file_path:
        output_3a in section3/3a/
    return:
        d[as]->d[as-ip]->(set(neighbors), set(internal neighbors), set(external neighbors))
    
    '''
    f = open(file_path)
    d = dict()
    for line in f:
        parts = line.strip().split(" ")
        as1 = parts[0].split("-")[0][2:]
        lg1 = parts[0][2:-2]
        as2 = parts[1].split("-")[0][1:]
        lg2 = parts[1][1:-2]
        #print as1,lg1,as2,lg2

        if as1 not in d:
            d[as1] = dict()
        if lg1 not in d[as1]:
            d[as1][lg1] = (set(),set(),set())
        d[as1][lg1][0].add(lg2)

        if as1 == as2: #internal
            d[as1][lg1][1].add(lg2)
        if as1 != as2: #external
            d[as1][lg1][2].add(lg2)
    f.close()
    return d

def build_rel_dict(ucla_rel):
    '''
    args:
        ucla_rel:
            ucla relation file: section3/3a/ucla_rel
    return:
        d[(as1,as2)]->type
    '''
    #build a dictionary: d[(as1,as2)]->type
    f  = open(ucla_rel)
    d = dict()
    for line in f:
        parts = line.rstrip().split("|")
        as1 = parts[0]
        as2 = parts[1]
        type_ = parts[2]
        desc = parts[3]
        d[(as1,as2)] = type_
    f.close()
    return d


def get_num_rel(ases, d):
    '''
    args:
        ases:
            list of AS objects
        d:
            d[(as1,as2)]->type, built from build_rel_dict()
    effect:
        for all the LGs in ASes in ases, add the attr NUM_REL (#i, #unknown, #cp, #pc, #p2p)
    '''
    for as_ in ases:
        lgs = as_.get_attr(LGS)
        as1 = as_.get_attr(ASN)
        for lg_ in lgs:
            num_i = 0
            num_unknown = 0
            num_cp = 0
            num_pc = 0
            num_p2p = 0

            _, set_i, set_e = lg_.get_attr(NEI_SET)
            num_i = len(set_i) #number of ibgp neighbors
            for nei in set_e:
                as2 = nei.split("-")[0]
                if (as1,as2) in d:
                    if d[(as1,as2)] == UNKNOWN:
                        num_unknown += 1
                    elif d[(as1,as2)] == C2P:#c2p
                        num_cp += 1
                    elif d[(as1,as2)] == P2C:#p2c
                        num_pc += 1
                    elif d[(as1,as2)] == P2P:
                        num_p2p += 1
                    else:
                        print "this cannot be reached!"
                        sys.exit()
                else: #records not in the dictionary
                    num_unknown += 1
                    #print "not in dict",line,

            value = (num_i, num_unknown, num_cp, num_pc, num_p2p)
            lg_.set_attr(NUM_REL, value)


def build_num_prefix_d(file_path, d_rel):
    '''
    args:
        file_path:
            output_3a in section3/3a/
        d_rel:
            d[(as1,as2)]->type, built from build_rel_dict()
    return:
        d[rel_type]->d[as-ip]-> list of # of prefixes , rel_type can be UNKNOWN, INTERNAL, C2P, ect
    '''
    f = open(file_path)
    d = dict()
    d[UNKNOWN] = dict()
    d[C2P] = dict()
    d[P2C] = dict()
    d[P2P] = dict()
    d[INTERNAL] = dict()
    for line in f:
        parts = line.strip().split(" ")
        as1 = parts[0].split("-")[0][2:]
        lg1 = parts[0][2:-2]
        as2 = parts[1].split("-")[0][1:]
        lg2 = parts[1][1:-2]
        num = int(parts[2])
        #print as1,lg1,as2,lg2

        rel = None
        #since d_rel doesn't have INTERNAL relationship
        if as1 == as2:
            rel = INTERNAL
        elif (as1, as2) in d_rel:
            rel = d_rel[(as1,as2)]
        else:
            rel = UNKNOWN

        if lg1 not in d[rel]:
            d[rel][lg1] = [num]
        else:
            d[rel][lg1].append(num)
    f.close()
    return d

def get_num_prefix_per_type(ases, d):
    '''
    args:
        ases:
            list of AS objects
        d:
            d[rel_type]->d[as-ip]-> list of # of prefixes , rel_type can be UNKNOWN, INTERNAL, C2P, ect
    effect:
        for all the LGs in ASes in ases, add the attr LIST_PREFIX ([i1,i2,..in],[unknow1,...],..[..])
    '''
    for as_ in ases:
        lgs = as_.get_attr(LGS)
        for lg_ in lgs:
            lg_id = lg_.get_attr(ID)

            d_tmp = dict()
            d_tmp[INTERNAL] = None
            d_tmp[UNKNOWN] = None
            d_tmp[C2P] = None
            d_tmp[P2C] = None
            d_tmp[P2P] = None
            for rel in d:
                if lg_id in d[rel]:
                    d_tmp[rel] = d[rel][lg_id]
                else:
                    d_tmp[rel] = []

            value = (d_tmp[INTERNAL], d_tmp[UNKNOWN], d_tmp[C2P], d_tmp[P2C], d_tmp[P2P])
            lg_.set_attr(LIST_PREFIX, value)



def build_as_name_type_tier_rank_d(as_nttr):
    '''
    "\N" is converted to "na"
    args:
        as_nttr:
            as type tier.. file: ./as_name_type_tier_rank
    return:
        d[as]-> (name, type, tier, rank)
    '''
    #build a dictionary: d[(as1,as2)]->type
    f  = open(as_nttr)
    d = dict()
    for line in f:
        parts = line.rstrip().split("|")
        asn = parts[0] or "na"
        name = parts[1] or "na"
        type_ = parts[2] or "na"
        if type_ == "\\N": type_ = "na"
        tier = parts[3] or "na"
        if tier == "\\N": tier = "na"
        rank = parts[4] or "na"
        d[(asn)] = (name, type_, tier, rank)
    f.close()
    return d

def get_nttr(ases, d):
    '''
    args:
        ases:
            list of AS objects
        d:
            d[as]-> (name, type, tier, rank)
    effect:
        for all the ASes in ases, add the attr INFO (name, type, tier, rank)
    '''
    for as_ in ases:
        asn = as_.get_attr(ASN)
        #assert (asn in d)
        #name, type_, tier, rank = d[asn]
        if asn in d:
            as_.set_attr(INFO,d[asn])
        else:   #not in caika, manully checked
            #print asn
            as_.set_attr(INFO, ("na","na","na","na"))


def build_ipint_lat_lon_d(ip_coords):
    '''
    args:
        ip_coords:
            ip_int|lat|long file: ./ip_to_coords
    return:
        d[ipint]-> (lat, lon), key is type int, values are float
    '''
    d = dict()
    f = open(ip_coords)
    for line in f:
        if "latitude" in line: #skip the first line
            continue
        parts = line.rstrip().split("|")
        ipint = int(parts[0])
        lat = float(parts[1])
        lon = float(parts[2])
        d[ipint] = (lat,lon)
    f.close()
    return d

def get_lat_lon(ases, d):
    '''
    args:
        ases:
            list of AS objects
        d:
            d[ipint]-> (lat, lon), key is type int, values are float
    effect:
        for all the lgs in ases, add the attr LAT_LON (lat, lon), both lat and lon are float
        if ipint is not found in d, then lat and lon are set to 0s
    '''
    for as_ in ases:
        for lg_ in as_.get_attr(LGS):
            ipint = lg_.get_ip_int()
            if ipint in d:
                lat,lon = d[ipint]
                lg_.set_attr(LAT_LON, (lat,lon))
            else:
                lg_.set_attr(LAT_LON, (0.0,0.0))

def build_prefix_lat_lon_d(file_path):
    '''
    d[prefix in our files] -> (lat,lon) in float
    '''
    f = open(file_path)
    d = pickle.load(f)
    return d


def JI(s1,s2):
    inter = s1 & s2
    union = s1 | s2
    if len(union) == 0:#according to definition
        return 1.0

    return 1.0*len(inter) / len(union)


if __name__ == "__main__":
    import sys
    #print parse(sys.argv[1])
    d_rel = build_rel_dict(sys.argv[2])#ucla_rel
    d =  build_num_prefix_d(sys.argv[1], d_rel)
    print d[INTERNAL]["31133-10.222.254.98"]
