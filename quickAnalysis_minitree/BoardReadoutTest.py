#!/usr/bin/env python

import ROOT as R
import sys, os
R.gStyle.SetOptStat(0)
R.gROOT.SetBatch(True) 

"""
v1

Rongkun
"""

def board_check_hit( 
        fin,
        fout = "",
        out_dir = "",
        l_board = [ 
            ("L1Q1", [8, 16]),
            ("L1Q2", [24]),
            ("L1Q3", [33]), 
            ],
        expected_count = -1,
        print_msg = True,
    ):
    """
    fin: file name
    l_board: list
    return 0 if successful
    return 1 if failed
    """

    do = R.RDataFrame("nsw", fin)

    l_histo = []
    l_name = []

    if out_dir != "":
        os.system("mkdir -p " + out_dir)

    if fout != "":
        try:
            f = open(fout, "w")
        except IOError:
            print "could not open file ", fout
            return 1

    output_str = ""

    for bname, links in l_board:
        linkCut = ""
        for ilink, link in zip(range(len(links)), links):
            if ilink != 0:
                linkCut += " || "
            linkCut += "linkId == {0}".format(link)

        d = do.Define("channelIDB", "(vmmid * 64 + channel)[{0}]".format(linkCut))
        h = d.Histo1D( ("x", "", 512, -0.5, 511.5), "channelIDB")
        l_histo.append((bname, h))
        l_name.append("hit")

    for pltname, tup in zip(l_name, l_histo):
        bname, h = tup[0], tup[1]
        c = R.TCanvas(bname+pltname, "{0} canvas of board : ".format(pltname) + bname , 800, 600)
        h.Draw()
        pass

        output_str += "========= "+ pltname + " " + bname + "=========\n"
        if pltname == "hit":
            for ibin in range(h.GetNbinsX()):
                if h.GetBinContent(ibin+1) == 0:
                    output_str += "channel {0} dead".format(ibin+1) + "\n"
                elif expected_count > 0 and h.GetBinContent(ibin+1) < expected_count:
                    output_str += "channel {0} low hit".format(ibin+1) + "\n"

                if h.GetBinContent(ibin+1) < h.GetMaximum() * 0.99:
                    output_str += "channel {0} low hit".format(ibin+1) + "\n"

                pass
            if out_dir != "":
                c.Print(out_dir + "/" + bname + "_" + pltname + ".pdf")
                pass
            pass
        pass

    if print_msg:
        print output_str

    f.write(output_str)
    f.close()

    return 0


if __name__ == "__main__":
    board_check_hit(
        "/afs/cern.ch/user/s/stgcic/public/wedge4.root",
        l_board = [ 
            ("L1Q1", [8, 16]),
            ("L1Q2", [24]),
            ("L1Q3", [33]), 
            ],
        expected_count = 100,
        out_dir = "test_out",
        fout = "test.out"
        )

#  for b, linkCut in l_board.items():
	#  d = do.Define("channelIDB", "(vmmid * 64 + channel)[{0}]".format(linkCut))
	#  h = d.Define( "ChRelbcid", "relbcid[{0}]".format(linkCut) ).Histo2D( 
		#  ("x", "", 512, -0.5, 511.5, 8, -0.5, 7.5), "channelIDB", "ChRelbcid")
	#  l_histo.append((b, h))
	#  l_name.append("relbcid_vs_hit")

#  for b, linkCut in l_board.items():
	#  d = do.Define("channelIDB", "(vmmid * 64 + channel)[{0}]".format(linkCut))
	#  h = d.Define( "ChPdo", "pdo[{0}]".format(linkCut) ).Histo2D( 
		#  ("x", "", 512, -0.5, 511.5, 512, -0.5, 1023.5), "channelIDB", "ChPdo")
	#  l_histo.append((b, h))
	#  l_name.append("pdo_vs_hit")


#  for name, tup in zip(l_name, l_histo):
	#  b, h = tup[0], tup[1]
	#  c = R.TCanvas(b, "canvas of board : " + b, 800, 600)
	#  h.Draw()
	#  c.Print(full_dir + b + "_" + name + ".pdf")
	#  c.Print(full_dir + b + "_" + name + ".root")
