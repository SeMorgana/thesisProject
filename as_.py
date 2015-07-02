from constants import *

class AS(object):
    def __init__(self, asn, lgs=None, info=None):
        '''
        args:
            asn:
                as number string
            lgs:
                a list of LGs
            info:
                (name, type, tier, rank)
        '''

        d_attr = dict()
        d_attr[ASN] = asn
        d_attr[LGS] = lgs
        d_attr[INFO] = info
        self.__dict__.update(d_attr)

    #def add_LG(self, lg):
    #    '''
    #    args:
    #        lg:
    #            a LG object
    #    '''
    #    self.__dict__[LGS].append(lg)

    def __str__(self):
        '''
        '''
        return self.get_attr(ASN) + ":\n" + "\n".join([str(lg) for lg in self.get_attr(LGS)])
    def __repr__(self):
        '''
        '''
        return "(" + self.get_attr(ASN) + ":\n" + "\n".join([str(lg) for lg in self.get_attr(LGS)]) +")"

    def __len__(self):
        '''
        return:
            the number of LGs in this AS
        '''
        return len(self.get_attr(LGS))


    def get_attr(self, attr):
        '''
        '''
        assert(attr in self.__dict__.keys())
        return self.__dict__[attr]
    

    def set_attr(self, attr, value):
        '''
        '''
        assert(attr in self.__dict__.keys())
        self.__dict__[attr] = value

    def validate(self):
        for lg_ in self.get_attr(LGS):
            print lg_
            lg_.validate()
