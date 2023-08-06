#!/usr/bin/env python
#coding:utf-8

import argparse
import os
import glob
import sys
import shutil
from rpy2.robjects import r
from deg import runDEG,parseDEG
from plot import picDEGnum,picDEGvolcano,picVeenExpression
from version import __version__
from util import mkdir,tab2xlsx
from subprocess import check_call

def parseArg():
    parser = argparse.ArgumentParser(description="For DEG analysis")
    parser.add_argument("-c","--countfile",type=str,help="The read-count table",required = True,metavar="<countfile>")
    parser.add_argument("-sg","--sg",type=str,help="The all samples and groups rep. like groupA=sample1,sample2,... groupB=sample3,sample4,...",required = True,nargs="+",metavar="<g1=s1,s2>")
    parser.add_argument("-o","--outdir",type=str,help="The output directory",required = True,metavar="<outdir>")
    parser.add_argument("-vs","--vs",type=str,help="the diff groups, like CasegroupA-VS-ControlgroupB ..., ", required = True,nargs="+",metavar="<g1-VS-g2>")
    parser.add_argument("-v","--version",action="version",version=__version__)
    parser.add_argument("-p","--pvalue",type=float,help="The pvalue threshold, default:0.05",default=0.05,metavar="<float>")
    parser.add_argument("-q","--qvalue",type=float,help="The padj value threshold, default:1",default=1,metavar="<float>")
    parser.add_argument("-fc","--fc",type=float,help="The fold change threshold, default:2",default=2,metavar="<float>")
    parser.add_argument("--padj",action="store_false",help="Used p-value or q-value for all deg parse output, default: p-value. if set, q-value will be used to instead",default=True)
    args = parser.parse_args()
    if not args.padj and args.qvalue >= 1:
        print "Used q-value for threads, qvalue must be set less then 1. 0.05 or 0.01 for recommend"
        sys.exit(os.EX_USAGE)
    return args

def totalGene(count):
    geneset = set()
    with open(count) as fi: 
        fi.next()
        for line in fi: 
            geneset.add(line.split("\t")[0])
    return geneset            
            
def main():
    args = parseArg()
    countab = os.path.abspath(args.countfile)
    if not os.path.exists(countab):
        print "%s file not exists!"%countab
        sys.exit(1)
    outdir = os.path.abspath(args.outdir)
    vs_list = args.vs
    mkdir(outdir,[i.split(",")[0] for i in vs_list])
    cmds = runDEG(countab,args.sg,vs_list,outdir)   
    for c in cmds:        
        r(c.strip())  
    degnumfile = []
    for vs in vs_list:
        g1 = vs.split("-")[0]
        g2 = vs.split("-")[-1]
        parseDEG(totalGene(countab),os.path.join(outdir,vs,vs+".txt"),fc=args.fc,pval=args.pvalue,padj=args.qvalue,pval_volcano=args.padj)
        degnumfile.append(os.path.join(outdir,vs,"deg.num.txt")) 
        picDEGvolcano(os.path.join(outdir,vs,vs+".plot_volcano.file"),os.path.join(outdir,vs,vs+".plot_volcano.file.png"))
        picVeenExpression(os.path.join(outdir,vs,vs+".diff.stat"),os.path.join(outdir,vs,vs+".venn"),g1,g2)
    check_call("cat %s > "%(" ".join(degnumfile)) + os.path.join(outdir,"deg.num.txt"),shell=True)
    picDEGnum(os.path.join(outdir,"deg.num.txt"),os.path.join(outdir,"deg.num"))
    check_call("perl %s -DC -sample_file %s -sample_file_head -od %s &> %s"%(os.path.join(os.path.dirname(__file__),"venn_stat_draw.pl")," ".join([vs+","+os.path.join(outdir,vs,"deg.up_down.txt") for vs in vs_list]),os.path.join(outdir,"venn_DEG"), os.path.join(outdir,"venn_DEG.log")),shell=True)
    check_call("perl %s -DC -sample_file %s -sample_file_head -od %s &> %s"%(os.path.join(os.path.dirname(__file__),"venn_stat_draw.pl")," ".join([vs+","+os.path.join(outdir,vs,"deg.up.txt") for vs in vs_list]),os.path.join(outdir,"venn_UP"), os.path.join(outdir,"venn_UP.log")),shell=True)
    check_call("perl %s -DC -sample_file %s -sample_file_head -od %s &> %s"%(os.path.join(os.path.dirname(__file__),"venn_stat_draw.pl")," ".join([vs+","+os.path.join(outdir,vs,"deg.down.txt") for vs in vs_list]),os.path.join(outdir,"venn_DOWN"), os.path.join(outdir,"venn_DOWN.log")),shell=True)
    results()
    return os.EX_OK
   
def results():
    args = parseArg()
    cpdict = {}
    results = os.path.abspath(os.path.join(args.outdir,"results"))
    outdir = os.path.abspath(args.outdir)
    mkdir(results,[v.split(",")[0] for v in args.vs]+["venn_DEG","venn_DOWN","venn_UP"])
    k = os.path.join(args.outdir,"deg.num.p*");v = results;cpdict[k] = v
    k = os.path.join(args.outdir,"count.normalized.txt");v = os.path.join(results,"count.normalized.xlsx");cpdict[k] = v 
    for i in [v.split(",")[0] for v in args.vs]:
        k = os.path.join(outdir,i,i+".txt");v = os.path.join(results,i,"deg.xlsx");cpdict[k]=v
        k = os.path.join(outdir,i,"deg.up.txt");v = os.path.join(results,i,"deg.up.xlsx");cpdict[k]=v
        k = os.path.join(outdir,i,"deg.down.txt");v = os.path.join(results,i,"deg.down.xlsx");cpdict[k]=v
        k = os.path.join(outdir,i,i+"*.png");v = os.path.join(results,i);cpdict[k]=v
    for i in ["venn_DEG","venn_DOWN","venn_UP"]:
        k = os.path.join(outdir,i,"list.txt");v= os.path.join(results,i,"list.xlsx");cpdict[k]=v
        k = os.path.join(outdir,i,"stat.txt");v= os.path.join(results,i,"stat.xlsx");cpdict[k]=v
        if len(args.vs) <= 5:
            k = os.path.join(outdir,i,"venn.tiff")
            v = os.path.join(results,i,"venn.tiff")
            cpdict[k]=v
    for k,v in cpdict.items():
        k = glob.glob(k)
        for i in k:
            if not i.endswith(".txt"):
                shutil.copy(i, v)
            else:
                tab2xlsx([i,],v,["sheet1",])
                    
if __name__ == "__main__":
    main()

