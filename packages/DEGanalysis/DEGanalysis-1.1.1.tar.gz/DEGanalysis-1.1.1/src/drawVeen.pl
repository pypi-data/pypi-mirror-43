#!/usr/bin/perl
use strict;
use warnings;
use FileHandle;
use Getopt::Long;
use Data::Dumper;
use File::Basename qw(basename dirname);
use Cwd;
use FindBin qw($Bin $Script);

chomp $Bin;
#####时间和版本#######################################################################################################
my $BEGIN_TIME=time();
my $version="1.0";
########################################

####使用程序需要输入的参数############################################################################################
my ($in,$od,$indexs);
GetOptions(		
	"help|?" =>\&USAGE,
	"in:s"=>\$in,
	"od:s"=>\$od,
	"p:s"=>\$indexs,
) or &USAGE;
&USAGE unless ($in and $od and $indexs);
&MKDIR($od);
$od=ABSOLUTE_DIR($od);$in=ABSOLUTE_DIR($in);

#open (IN,$in) or die $!;
#open OUT,">$od/venn_draw.list";
#while (<IN>) {
#	my ($id,@info)=split /\s+/,$_;
#	my $info=join "\t",@info;
#	print OUT"$info\n";
#}
#close OUT;
#close IN;

open (IN,$in) or die $!;
my $head=<IN>;
my @headId=split /\s+/,$head;
my %headIdContent;
while (<IN>) {
	if (/^\#/) { next; }
	unless (/\w/) { next; }
	s/\s+$//g;
	chomp;
	foreach  my $arrayIndex (1..$#headId) {
		my $geneId=(split /\t/,$_)[$arrayIndex];
		if ($geneId ne "NA") {
			my $geneIdNew="\"$geneId\"";
			push @{$headIdContent{$headId[$arrayIndex]}},$geneIdNew;
		}
		
	}
}
close IN;
my @color = ("\"#E69F00\"", "\"#56B4E9\"", "\"#009E73\"", "\"#F0E442\"", "\"#0072B2\"", "\"#D55E00\"", "\"#CC79A7\"", "\"#E69F00\"", "\"#56B4E9\"", "\"#009E73\"", "\"#F0E442\"", "\"#CC6666\"", "\"#9999CC\"", "\"#66CC99\"", "\"#E69F00\"", "\"#56B4E9\"", "\"#009E73\"", "\"#F0E442\"", "\"#0072B2\"", "\"#D55E00\"", "\"#CC79A7\"","\"#E69F00", "\"#56B4E9\"", "\"#009E73\"", "\"#F0E442\"");
my %sampleColour;
foreach  (1..$#headId) {
	$sampleColour{$headId[$_]}=$color[$_];
}
shift @headId;
my @usecolour= values %sampleColour;
my $useColour=join",",@usecolour;
my @list;
foreach my $sampleName1 (sort @headId) {
	
	my $listname="$sampleName1\=$sampleName1";
	if($sampleName1=~/^\d+/){
		$listname="A_$sampleName1\=A_$sampleName1";
	}
	push @list,$listname;
}
my $list=join",",@list;

chomp $useColour;
chomp $list;


open (OUTR,">$od/$indexs.r") or die $!;
#my $Rscript=`which Rscript`;
print OUTR "#! Rscript\n";
print OUTR "library\(\"VennDiagram\"\)\n";
foreach my $sampleName (sort @headId) {
	my %count1;
	@{$headIdContent{$sampleName}} = grep { ++$count1{ $_ } < 2;} @{$headIdContent{$sampleName}};
	my $samplecontent=join",",@{$headIdContent{$sampleName}};
	if($sampleName=~/^\d+/){
        $sampleName=~ s/[-]/_/g;
		print OUTR "A_$sampleName \<\- c($samplecontent)\n";
	}else{
        $sampleName=~ s/[-]/_/g;
		print OUTR "$sampleName \<\- c($samplecontent)\n";
	}
}
my $sample_num=scalar @headId;
my $margin='margin=0.5';
my $height='height=3000';
my $width='width=3000';
my $resolution='resolution=200';
my $units="units='px'";
my $lwd='lwd=1';
my $cex=($sample_num==5)?'cex=0.4':'cex=0.7';
my $cat_cex='cat.cex=0.9';
my $scaled='scaled=0';
my $cat_pos=($sample_num==2)?'cat.pos=0':'';
my $cat_dist=($sample_num==3)?'cat.dist=c(0.05,0.05,0.05)':'';

$list=~ s/[-]/_/g;
print OUTR <<END;
venn.diagram(list($list),fill=c($useColour),$margin,$height,$width,$resolution,$units,$lwd,$cex,$cat_cex,$scaled,$cat_pos,$cat_dist,filename="$od/$indexs.tiff")

END
close OUTR ;

my $cmd;
$cmd = "Rscript $od/$indexs.r";
print "$cmd\n";
`$cmd `;
###################################################################################################################

sub MKDIR
{ # &MKDIR($out_dir);
	my ($dir)=@_;
	#rmdir($dir) if(-d $dir);
	mkdir($dir) if(!-d $dir);
}

#####输入说明子程序####################################################################################################
sub USAGE
{
my $usage=<<"USAGE";
Program: 
Version: $version
Description:

Usage:

	-in			input file

#ID	N1							T1
#C1	cdr1as_test_circ_007666	cdr1as_test_circ_007666
#C2	cdr1as_test_circ_001239	cdr1as_test_circ_001521
#C3	cdr1as_test_circ_000920	cdr1as_test_circ_000920
#C4	cdr1as_test_circ_003260	cdr1as_test_circ_005523
#C5	cdr1as_test_circ_004725	cdr1as_test_circ_003239
#C6	cdr1as_test_circ_000898	cdr1as_test_circ_006155
	-od			the output directory
	-p			output file prefix
#############################################
USAGE
	print $usage;
	exit;
}

#####获取文件绝对路径####################################################################################################
sub ABSOLUTE_DIR
{ #$pavfile=&ABSOLUTE_DIR($pavfile);
	my $cur_dir=`pwd`;chomp($cur_dir);
	my ($in)=@_;
	my $return="";
	
	if(-f $in)
	{
		my $dir=dirname($in);
		my $file=basename($in);
		chdir $dir;$dir=`pwd`;chomp $dir;
		$return="$dir/$file";
	}
	elsif(-d $in)
	{
		chdir $in;$return=`pwd`;chomp $return;
	}
	else
	{
		warn "Warning just for file and dir in [sub ABSOLUTE_DIR]\n";
		exit;
	}
	
	chdir $cur_dir;
	return $return;
}
