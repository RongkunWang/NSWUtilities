#!/usr/bin/env python

import ROOT as R
import sys, os
R.gROOT.SetBatch(True) 

# for today's test
basedir = "/eos/atlas/atlascerngroupdisk/det-nsw-stgc/b191/A12/"
rundir = "20200212_DAQ/"

l_board_A12 = {
	"sL1Q1":"linkId == 44032 || linkId == 44033",
	"sL1Q2":"linkId == 44040",
	"sL1Q3":"linkId == 44048",
	"pL1Q1":"linkId == 11264",
	"pL1Q2":"linkId == 11272",
	"pL1Q3":"linkId == 11280",

	"sL2Q1":"linkId == 44160 || linkId == 44161",
	"sL2Q2":"linkId == 44168",
	"sL2Q3":"linkId == 44176",
	"pL2Q1":"linkId == 11392",
	"pL2Q2":"linkId == 11400",
	"pL2Q3":"linkId == 11408",

	"sL3Q1":"linkId == 44288 || linkId == 44289",
	"sL3Q2":"linkId == 44296",
	"sL3Q3":"linkId == 44304",
	"pL3Q1":"linkId == 11520",
	"pL3Q2":"linkId == 11528",
	# typo!!
	#"pL3Q3":"linkId == 2320",
	"pL3Q3":"linkId == 11536",

	"sL4Q1":"linkId == 44416 || linkId == 44417",
	"sL4Q2":"linkId == 44424",
	"sL4Q3":"linkId == 44432",
	"pL4Q1":"linkId == 11648",
	"pL4Q2":"linkId == 11656",
	"pL4Q3":"linkId == 11664",



# HO

	"sL5Q1":"linkId == 44544 || linkId == 44545",
	"sL5Q2":"linkId == 44552",
	"sL5Q3":"linkId == 44560",
	"pL5Q1":"linkId == 11776",
	"pL5Q2":"linkId == 11784",
	"pL5Q3":"linkId == 11792",

	"sL6Q1":"linkId == 44672 || linkId == 44673",
	"sL6Q2":"linkId == 44680",
	"sL6Q3":"linkId == 44688",
	"pL6Q1":"linkId == 11904",
	"pL6Q2":"linkId == 11912",
	"pL6Q3":"linkId == 11920",

	"sL7Q1":"linkId == 44800 || linkId == 44801",
	"sL7Q2":"linkId == 44808",
	"sL7Q3":"linkId == 44816",
	"pL7Q1":"linkId == 12032",
	"pL7Q2":"linkId == 12040",
	"pL7Q3":"linkId == 12048",

	"sL8Q1":"linkId == 44928 || linkId == 44929",
	"sL8Q2":"linkId == 44936",
	"sL8Q3":"linkId == 44944",
	"pL8Q1":"linkId == 12160",
	"pL8Q2":"linkId == 12168",
	"pL8Q3":"linkId == 12176",

}




l_board = l_board_A12


fn = sys.argv[1]
# f = R.TFile(fn)
# t = f.Get("nsw")

do = R.RDataFrame("nsw", fn)

full_dir = basedir + rundir + fn + "/"
os.system("mkdir -p " + full_dir)

l_histo = []
l_name = []

for b, linkCut in l_board.items():
	d = do.Define("channelIDB", "(vmmid * 64 + channel)[{0}]".format(linkCut))
	h = d.Histo1D( ("x", "", 512, -0.5, 511.5), "channelIDB")
	l_histo.append((b, h))
	l_name.append("hit")

for b, linkCut in l_board.items():
	d = do.Define("channelIDB", "(vmmid * 64 + channel)[{0}]".format(linkCut))
	h = d.Define( "ChRelbcid", "relbcid[{0}]".format(linkCut) ).Histo2D( 
		("x", "", 512, -0.5, 511.5, 8, -0.5, 7.5), "channelIDB", "ChRelbcid")
	l_histo.append((b, h))
	l_name.append("relbcid_vs_hit")

for b, linkCut in l_board.items():
	d = do.Define("channelIDB", "(vmmid * 64 + channel)[{0}]".format(linkCut))
	h = d.Define( "ChPdo", "pdo[{0}]".format(linkCut) ).Histo2D( 
		("x", "", 512, -0.5, 511.5, 512, -0.5, 1023.5), "channelIDB", "ChPdo")
	l_histo.append((b, h))
	l_name.append("pdo_vs_hit")


for name, tup in zip(l_name, l_histo):
	b, h = tup[0], tup[1]
	c = R.TCanvas(b, "canvas of board : " + b, 800, 600)
	h.Draw()
	c.Print(full_dir + b + "_" + name + ".pdf")
	c.Print(full_dir + b + "_" + name + ".root")
