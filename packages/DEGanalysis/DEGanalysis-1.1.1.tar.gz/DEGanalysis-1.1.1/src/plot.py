import os
from rpy2.robjects import r

def picDEGnum(numfile,outprefix):
    r('suppressMessages(library(ggplot2))')
    r('data <- read.table("%s",sep="\t",header=FALSE)'%numfile)
    r('type=factor(data$V2, levels=c("UP","DOWN"))')
    r('pic <- ggplot(data,aes(x=data$V1,y=data$V3,fill=type)) + geom_bar(stat="identity", position=position_dodge(width = 0.9)) + scale_fill_manual(values=c("#cc2424", "#00a651")) + xlab("Samples") + ylab("Numbers") + ggtitle("DEG stat") + geom_text(aes(label = data$V3, vjust = 0.5, hjust = 0, angle=90), show.legend = FALSE , position=position_dodge(width = 0.9)) + ylim(min(data$V3, 0)*1.1, max(data$V3)*1.1) + theme_bw()+theme( plot.title = element_text(hjust = 0.5), panel.background=element_rect(fill="transparent", color="black"),panel.border=element_rect(fill="transparent", color="transparent"),panel.grid=element_blank(),axis.text.x=element_text(angle=30,vjust=0.5))')
    r("ggsave(pic,file='%s')"%(outprefix+".png"))
    r("ggsave(pic,file='%s')"%(outprefix+".pdf"))
    
def picDEGvolcano(dataFile,outputPngFile):
    r('png("%s",width =1480, height = 1480)'%outputPngFile)
    r('par(mar=c(7,6,6,4))')
    r('datafile<-read.table("%s",header=FALSE,sep="\t")'%dataFile)
    r('header<-subset(datafile[1,])')
    rc = '''
    xlab<-header$V2
    ylab<-header$V3
    main<-header$V4
    datafile<-datafile[-1,]
    datafile<-datafile[order(factor(datafile$V4,levels = c("","up","down"))),]
    datafile<-as.matrix(datafile)
    col1=datafile[,4]
    col1[col1=="up"]="#cc2424"
    col1[col1=="down"]="#00a651"
    col1[col1==""]="#000000"
    plot(datafile[,2],datafile[,3],pch=20,cex=3,xlab=xlab,
     ylab=ylab,main=main,col=as.vector(col1),cex.axis=2.25,cex.lab=2.7,cex.main=4,log="")
    legend("topleft",pch=20,col=c("#cc2424","#00a651","#000000"),legend=c("Up regulated genes","Down regulated genes","Non-regulated genes"),
       bty="n",xpd=TRUE,cex=2)
    dev.off()
    '''
    r(rc)   
    
def picVeenExpression(infofile,outprefix,g1,g2):
    lines = os.popen("grep 'Expressed In' %s"%infofile).read().strip().split("\n")
    n1,n2,n3 = [i.split("\t")[1] for i in lines]
    r('suppressMessages(library(VennDiagram))')
    r("cols<-c('#5da5da','#decf3f')")
    r('draw<-function() {draw.pairwise.venn(area1=%s,area2=%s,cross.area=%s,category=c("%s","%s"),lwd=rep(1,1),lty=rep(2,2), col=cols,fill=cols,cat.col=cols )}'%(n1,n2,n3,g1,g2))
    r('png("%s")'%(outprefix+".png"))
    r('draw()')
    r('dev.off()')    
    r('pdf("%s")'%(outprefix+".pdf"))
    r('draw()')
    r('dev.off()') 
