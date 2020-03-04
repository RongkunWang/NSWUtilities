#!/usr/bin/env python

import ROOT as R
import sys, os
R.gROOT.SetBatch(True) 

# for today's test
rundir = "20200131_TuneMoreLayers/"

l_board = {
	"sL1Q1":"linkId == 34816 || linkId == 34817",
	"sL1Q2":"linkId == 34824",
	"sL1Q3":"linkId == 34832",
	"pL1Q1":"linkId == 2048",
	"pL1Q2":"linkId == 2056",
	"pL1Q3":"linkId == 2064",

	"sL2Q1":"linkId == 34944 || linkId == 34945",
	"sL2Q2":"linkId == 34952",
	"sL2Q3":"linkId == 34960",
	"pL2Q1":"linkId == 2176",
	"pL2Q2":"linkId == 2184",
	"pL2Q3":"linkId == 2192",

	"sL3Q1":"linkId == 35072 || linkId == 35073",
	"sL3Q2":"linkId == 35080",
	"sL3Q3":"linkId == 35088",
	"pL3Q1":"linkId == 2304",
	"pL3Q2":"linkId == 2312",
	"pL3Q3":"linkId == 2320",

	"sL4Q1":"linkId == 35200 || linkId == 35201",
	"sL4Q2":"linkId == 35208",
	"sL4Q3":"linkId == 35216",
	"pL4Q1":"linkId == 2432",
	"pL4Q2":"linkId == 2440",
	"pL4Q3":"linkId == 2448",
}

basedir = "/afs/cern.ch/work/n/nswdaq/public/data_stgc/"

fn = sys.argv[1]
f = R.TFile(fn)
t = f.Get("nsw")


full_dir = basedir + rundir + fn + "/"
os.system("mkdir -p " + full_dir)

for b, linkCut in l_board.items():
	c = R.TCanvas(b, "canvas of board : " + b, 800, 600)
	t.Draw("vmmid * 64 + channel>>h(512, -0.5, 511.5)", linkCut)
	c.Print(full_dir + b + ".pdf")
	c.Print(full_dir + b + ".root")
