#!/usr/bin/env python

def fun(flxid, card, l_links, phase = 1):
    l_elink_flx = []
    l_elink = []


    #  l_links = range(12)

    for link in l_links:
        # for sTGC, there are extra elinks for pFEB and sFEB GBTx2 
        # because I don't want ot map them in too much detail here.
        all_elinks = [8, 16, 24, 33]
        if phase == 2:
            all_elinks = [11, 19, 25, 33]
        if phase == 3:
            all_elinks = [11, 19, 27, 35]
        for i in all_elinks:
            l_elink_flx.append( card * 2 ** 11 + link * 2**6 + i)
            l_elink.append(     flxid * 2**16 + card * 2 ** 11 + link * 2**6 + i)

    l_elink_s = [str(i) for i in l_elink_flx]
    print "argument for felixcore, for FELIX to publish elinks"
    print ",".join(l_elink_s)
    print

    l_elink_s = [str(i) for i in l_elink]
    print "for netio_cat to grab data"
    print " -t " + " -t ".join(l_elink_s)
    print


# phase 1
#  fun(0, 0, range(12),     1)
#  fun(0, 1, [6, 7, 9, 10], 1)
#  fun(0, 3, range(4) + range(6, 10), 1)
#  fun(1, 0, range(12),     1)
#  fun(1, 1, [6, 7, 9, 10], 1)
#  fun(1, 3, range(4) + range(6, 10), 1)

# phase 2
#  fun(0, 0, range(12),     2)
#  fun(0, 1, [6, 7, 9, 10], 2)
#  fun(0, 3, range(4) + range(6, 10), 2)
#  fun(1, 0, range(12),     2)
#  fun(1, 1, [6, 7, 9, 10], 2)
#  fun(1, 3, range(4) + range(6, 10), 2)

fun(0, 0, range(12),     3)
