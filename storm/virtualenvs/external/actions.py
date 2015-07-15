# [\0]                                                               #
#                                                                    #
# This code is confidential and proprietary, All rights reserved.    #
#								     #
# Tamar Labs 2015.						     #
#								     #
# @author: Adam Lev-Libfeld (adam@tamarlabs.com)                     #
#								     #


class ActionDB(object):
    actions = [double,flip]
    
    def __init__(self):
        pass

    def double(self,input):
        a,b = input
        return 2*int(a) , 2*int(b)

    def flip(self,input):
        a,b = input
        return b,a
