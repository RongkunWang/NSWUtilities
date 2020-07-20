#!/usr/bin/env python

def fun(flxid, card, l_links):
    l_elink_flx = []
    l_elink = []


    #  l_links = range(12)

    for link in l_links:
        # for sTGC..
        for i in [8, 16, 24, 33]:
            l_elink_flx.append( card * 2 ** 11 + link * 2**6 + i)
            l_elink.append(     flxid * 2**16 + card * 2 ** 11 + link * 2**6 + i)

    l_elink_s = [str(i) for i in l_elink_flx]
    print "for FELIX to publish elinks"
    print ",".join(l_elink_s)
    print

    l_elink_s = [str(i) for i in l_elink]
    print "for netio_cat to grab data"
    print " -t " + " -t ".join(l_elink_s)
    print


fun(0, 0, range(12))
fun(0, 1, [6, 7, 9, 10])
fun(1, 0, range(12))
fun(1, 1, [6, 7, 9, 10])
