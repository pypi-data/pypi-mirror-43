#!/usr/bin/env python
#coding:utf-8

import os, sys, time
from compiler.ast import flatten
from rpy2.robjects import r
from collections import OrderedDict
from math import log

def parseDEG(totalgene, filename, fc=2, pval=0.05, padj=1, pval_volcano=True):
    outdir = os.path.dirname(filename)
    key = os.path.basename(os.path.dirname(os.path.abspath(filename)))
    if '-VS-' not in key:
        key = os.path.splitext(os.path.basename(os.path.abspath(filename)))[0]
    if '-VS-' not in key:
        print 'Error: No vs infomation in you input file %s' % os.path.abspath(filename)
        sys.exit(1)
    g1, g2 = key.split('-VS-')
    with open(filename) as (fi):
        with open(os.path.join(outdir, key + '.plot_volcano.file'), 'w') as (volcano):
            with open(os.path.join(outdir, 'deg.up.txt'), 'w') as (up):
                with open(os.path.join(outdir, 'deg.down.txt'), 'w') as (down):
                    with open(os.path.join(outdir, 'deg.up_down.txt'), 'w') as (updown):
                        if pval_volcano:
                            volcano.write('ID\tlog2(fold change)\t-log10(p value)\t%s\n' % key)
                        else:
                            volcano.write('ID\tlog2(fold change)\t-log10(padj value)\t%s\n' % key)
                        header = fi.next()
                        up.write(header.strip() + '\tUP_DOWN\n')
                        down.write(header.strip() + '\tUP_DOWN\n')
                        if pval_volcano:
                            updown.write(header.strip().split()[0] + '\t' + 'Pvalue' + '\tUP_DOWN\n')
                        else:
                            updown.write(header.strip().split()[0] + '\t' + 'Qvalue' + '\tUP_DOWN\n')
                        up_num, down_num = (0, 0)
                        expg1 = set()
                        expg2 = set()
                        totaldiff = 0
                        for line in fi:
                            if not line.strip():
                                continue
                            totaldiff += 1
                            n = line.strip().split('\t')
                            if n[-2] == 'NA' or n[-1] == 'NA':
                                continue
                            n[1:] = map(float, n[1:])
                            group1, group2, log2fc, pvalue, qvalue = n[-5:]
                            if float(group1) > 0:
                                expg1.add(n[0])
                            if float(group2) > 0:
                                expg2.add(n[0])
                            if abs(log2fc) >= log(fc, 2) and pvalue <= pval and qvalue <= padj:
                                if log2fc > 0:
                                    up_num += 1
                                    up.write(('\t').join(map(str, n)) + '\tup\n')
                                    if pval_volcano:
                                        updown.write(n[0] + '\t' + str(pvalue) + '\tup\n')
                                        if pvalue > 0:
                                            volcano.write(n[0] + '\t' + str(log2fc) + '\t' + str(-log(pvalue, 10)) + '\tup\n')
                                        if pvalue == 0:
                                            print 'Warning: id %s gets a zero pvalue in %s file' % (n[0], filename)
                                            volcano.write(n[0] + '\t' + str(log2fc) + '\t' + 'inf' + '\tup\n')
                                    else:
                                        updown.write(n[0] + '\t' + str(qvalue) + '\tup\n')
                                        if qvalue > 0:
                                            volcano.write(n[0] + '\t' + str(log2fc) + '\t' + str(-log(qvalue, 10)) + '\tup\n')
                                        if qvalue == 0:
                                            print 'Warning: id %s gets a zero qvalue in %s file' % (n[0], filename)
                                            volcano.write(n[0] + '\t' + str(log2fc) + '\t' + 'inf' + '\tup\n')
                                else:
                                    down_num += 1
                                    down.write(('\t').join(map(str, n)) + '\tdown\n')
                                    if pval_volcano:
                                        updown.write(n[0] + '\t' + str(pvalue) + '\tdown\n')
                                        if pvalue > 0:
                                            volcano.write(n[0] + '\t' + str(log2fc) + '\t' + str(-log(pvalue, 10)) + '\tdown\n')
                                        if pvalue == 0:
                                            print 'Warning: id %s gets a zero pvalue in %s file' % (n[0], filename)
                                            volcano.write(n[0] + '\t' + str(log2fc) + '\t' + 'inf' + '\tdown\n')
                                    else:
                                        updown.write(n[0] + '\t' + str(qvalue) + '\tdown\n')
                                        if qvalue > 0:
                                            volcano.write(n[0] + '\t' + str(log2fc) + '\t' + str(-log(qvalue, 10)) + '\tdown\n')
                                        if qvalue == 0:
                                            print 'Warning: id %s gets a zero qvalue in %s file' % (n[0], filename)
                                            volcano.write(n[0] + '\t' + str(log2fc) + '\t' + 'inf' + '\tdown\n')
                            elif pval_volcano:
                                if pvalue > 0:
                                    volcano.write(n[0] + '\t' + str(log2fc) + '\t' + str(-log(pvalue, 10)) + '\t\n')
                                if pvalue == 0:
                                    print 'Warning: id %s gets a zero pvalue in %s file' % (n[0], filename)
                                    volcano.write(n[0] + '\t' + str(log2fc) + '\t' + 'inf' + '\t\n')
                            else:
                                if qvalue > 0:
                                    volcano.write(n[0] + '\t' + str(log2fc) + '\t' + str(-log(qvalue, 10)) + '\t\n')
                                if qvalue == 0:
                                    print 'Warning: id %s gets a zero qvalue in %s file' % (n[0], filename)
                                    volcano.write(n[0] + '\t' + str(log2fc) + '\t' + 'inf' + '\t\n')

    with open(outdir + '/deg.num.txt', 'w') as (deg_num):
        deg_num.write(key + '\tUP\t%d\n' % up_num)
        deg_num.write(key + '\tDOWN\t%d\n' % down_num)
    with open(os.path.join(outdir, key + '.diff.stat'), 'w') as (ds):
        ds.write('Discription\tNumber\tRatio(%)\n')
        Total_Genes = len(totalgene)
        Expressed_Genes = len(expg1.union(expg2))
        Expressed_In_g1 = len(expg1)
        Expressed_In_g2 = len(expg2)
        ExpressedBoth = len(expg1.intersection(expg2))
        TotalDiffGenes = totaldiff
        updiff = up_num
        downdiff = down_num
        ds.write('Total Genes\t%d\t100.00\n' % Total_Genes)
        ds.write('Expressed Genes\t%d\t%.2f\n' % (Expressed_Genes, float(Expressed_Genes) / Total_Genes * 100))
        ds.write('Expressed In %s\t%d\t%.2f\n' % (key.split('-')[0], Expressed_In_g1, float(Expressed_In_g1) / Total_Genes * 100))
        ds.write('Expressed In %s\t%d\t%.2f\n' % (key.split('-')[-1], Expressed_In_g2, float(Expressed_In_g2) / Total_Genes * 100))
        ds.write('Expressed In Both\t%d\t%.2f\n' % (ExpressedBoth, float(ExpressedBoth) / Total_Genes * 100))
        ds.write('Expressed Only In %s\t%d\t%.2f\n' % (key.split('-')[0], Expressed_In_g1 - ExpressedBoth, float(Expressed_In_g1 - ExpressedBoth) / Total_Genes * 100))
        ds.write('Expressed Only In %s\t%d\t%.2f\n' % (key.split('-')[-1], Expressed_In_g2 - ExpressedBoth, float(Expressed_In_g2 - ExpressedBoth) / Total_Genes * 100))
        ds.write('Total Diff Expressed Genes\t%d\t%.2f\n' % (TotalDiffGenes, float(TotalDiffGenes) / Total_Genes * 100))
        ds.write('Up Diff Expressed Genes\t%d\t%.2f\n' % (updiff, float(updiff) / Total_Genes * 100))
        ds.write('Down Diff Expressed Genes\t%d\t%.2f\n' % (downdiff, float(downdiff) / Total_Genes * 100))


def runDEG(countable, samplesgroups, vs_list, outdir):
    header = os.popen('head -1 %s' % countable).read().strip().split()
    table_col = header[1:]
    group_dict = OrderedDict()
    for rep in samplesgroups:
        k = rep.split('=')[0]
        v = rep.split('=')[-1].strip().strip(',').split(',')
        group_dict[k] = v

    samples = set(flatten(group_dict.values()))
    s = str(table_col).strip('[]')
    rcmd = []
    rcmd.append('suppressMessages(library("DESeq2"))\nsuppressMessages(library("edgeR"))')
    rcmd.append('mydata <- read.table("%s",sep="\\t",row.names=1,header=T,as.is=T)' % countable)
    rcmd.append('mydata[is.na(mydata)] <- 0')
    rcmd.append('colnames(mydata) <- c(%s)' % str(table_col).strip('[]'))
    rcmd.append('rnaseqMatrix <- round(as.matrix(mydata))')
    rcmd.append('condition <- factor(c(%s))' % s)
    rcmd.append('coldata <- data.frame(row.names = colnames(rnaseqMatrix), condition)')
    rcmd.append('dds <- DESeqDataSetFromMatrix(rnaseqMatrix,colData = coldata,design=~condition)')
    rcmd.append('dds <- estimateSizeFactors(dds)\nnorcounts <- counts(dds, normalized=T)')
    rcmd.append('write.table(cbind(data.frame(%s=rownames(norcounts)),norcounts),file="%s",quote=F,sep = "\\t",row.names=F)' % (header[0], os.path.join(outdir, os.path.splitext(os.path.basename(countable))[0] + '.normalized' + os.path.splitext(os.path.basename(countable))[-1])))
    for vs in vs_list:
        if ',' in vs:
            if vs.endswith('paired'):
                rcmd.append('# diff gene of paired group %s' % vs.split(',')[0])
            else:
                print "'paired' string must after the 'vs' info"
                sys.exit(1)
        else:
            rcmd.append('# diff gene of group %s' % vs)
        case = vs.split(',')[0].split('-VS-')[0]
        control = vs.split(',')[0].split('-VS-')[-1]
        casestr = str(group_dict[case]).strip('[]')
        constr = str(group_dict[control]).strip('[]')
        g = []
        for i in table_col:
            if i in group_dict[case]:
                g.append(case)
            elif i in group_dict[control]:
                g.append(control)
            else:
                g.append(i)

        g = str(g).strip('[]')
        if ',' in vs:
            vs = vs.split(',')[0]
            if len(group_dict[case]) != len(group_dict[control]):
                print 'number of sample must be paired if paired analysis'
                sys.exit(1)
            rcmd.append('suppressMessages(library("limma"))')
            rcmd.append('limmaMatrix <- mydata[,c(%s)]' % str(group_dict[case] + group_dict[control]).strip('[]'))
            rcmd.append('paired <- factor(rep(seq(1,%d),2))' % len(group_dict[case]))
            rcmd.append('condition <- factor(c(rep(2,%d),rep(1,%d)))' % (len(group_dict[case]), len(group_dict[control])))
            rcmd.append('design <- model.matrix(~paired+condition)')
            rcmd.append('v1 <- voom(limmaMatrix,design,plot=TRUE,normalize="quantile")')
            rcmd.append('fit <- lmFit(v1,design,method="ls")')
            rcmd.append('fit2 <- eBayes(fit)')
            rcmd.append('Output <- topTable(fit2, coef=ncol(design), adjust.method="BH", n=Inf)')
            ncstr = []
            for sss in group_dict[case] + group_dict[control]:
                ncstr.append(sss + '=' + 'norcounts[rownames(Output),i"%s"]' % sss)

            rcmd.append('res <- data.frame(id=rownames(Output),%s,%s=rowMeans(norcounts[rownames(Output),c(%s)]),%s=rowMeans(norcounts[rownames(Output),c(%s)]),log2FoldChange=Output$logFC,pval=Output$P.Value,padj=Output$adj.P.Val,row.names=rownames(Output))' % ((',').join(ncstr), case, casestr, control, constr))
            rcmd.append('res <- res[order(res$pval),]')
            rcmd.append('write.table(res,file="%s",quote=F,sep = "\\t",row.names=F)' % os.path.join(outdir, vs, vs + '.txt'))
            continue
        rcmd.append('condition <- factor(c(%s))' % g)
        if len(group_dict[case]) == len(group_dict[control]) == 1:
            rcmd.append('suppressMessages(library("DESeq"))')
            rcmd.append('dds <- newCountDataSet(rnaseqMatrix, condition)')
            rcmd.append('dds <- estimateSizeFactors(dds)')
            rcmd.append('keep <- rowSums(rnaseqMatrix)>0')
            rcmd.append('dds <- dds[keep,]')
            rcmd.append('dds <- estimateSizeFactors(dds)')
            rcmd.append('dds <- estimateDispersions(dds, method="blind", sharingMode="fit-only", fitType="local")')
            rcmd.append('res <- nbinomTest(dds, "%s", "%s")' % (control, case))
            rcmd.append('res <- res[order(res$pval),-5]')
            rcmd.append('res[3:4] <- res[4:3]')
            rcmd.append('colnames(res)[3:4] <- c("baseMean_%s","baseMean_%s")' % (case, control))
            rcmd.append('res$baseMean <- rowMeans(norcounts[res$id,])')
            rcmd.append('res <- subset(res,baseMean_%s > 0 | baseMean_%s > 0)' % (case, control))
            rcmd.append('write.table(res,file="%s",quote=F,sep = "\\t",row.names=F)' % os.path.join(outdir, vs, vs + '.txt'))
        else:
            rcmd.append('coldata <- data.frame(row.names = colnames(rnaseqMatrix), condition)')
            rcmd.append('dds <- DESeqDataSetFromMatrix(rnaseqMatrix,colData = coldata,design=~condition)')
            rcmd.append('dds <- estimateSizeFactors(dds)\nnorcounts <- counts(dds, normalized=T)')
            rcmd.append('keep <- rowSums(counts(dds,normalized=T)>0)>=2')
            rcmd.append('dds <- dds[keep,]')
            rcmd.append('dds2 <- DESeq(dds)')
            rcmd.append('diff_gene_deseq2 <- results(dds2,contrast = c("condition","%s","%s"))' % (case, control))
            rcmd.append('diff_gene_deseq2 <- diff_gene_deseq2[order(diff_gene_deseq2$pvalue),]')
            ncstr = []
            for sss in group_dict[case] + group_dict[control]:
                ncstr.append(sss + '=' + 'norcounts[rownames(diff_gene_deseq2),"%s"]' % sss)

            rcmd.append('diff_info <- data.frame(id=rownames(diff_gene_deseq2),%s,%s=rowMeans(norcounts[rownames(diff_gene_deseq2),c(%s)]),%s=rowMeans(norcounts[rownames(diff_gene_deseq2),c(%s)]),log2FoldChange=diff_gene_deseq2$log2FoldChange,pval=diff_gene_deseq2$pvalue,padj=diff_gene_deseq2$padj,row.names=rownames(diff_gene_deseq2))' % ((',').join(ncstr), case, casestr, control, constr))
            rcmd.append('diff_info <- subset(diff_info,%s > 0 | %s > 0)' % (case, control))
            rcmd.append('write.table(diff_info,file="%s",quote=F,sep = "\\t",row.names=F)' % os.path.join(outdir, vs, vs + '.txt'))

    return flatten([ i.split('\n') for i in rcmd ])

