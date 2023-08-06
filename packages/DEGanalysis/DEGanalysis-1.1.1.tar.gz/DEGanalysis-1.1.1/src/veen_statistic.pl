#!usr/bin/perl -w
use strict;
use FindBin qw($Bin $Script);
use File::Basename qw(basename dirname);
use Getopt::Long;

my (@files,$sample_file_head,$out_dir);
GetOptions(
	"help|?"=>\&USAGE,
	"f:s{,}"=>\@files,
	"od:s"=>\$out_dir,
	"head!"=>\$sample_file_head,
)|| die &USAGE;
&USAGE unless (@files);
$out_dir||=".";
mkdir $out_dir unless -d $out_dir;

my $out_list;
my $out_stat;
	my %list;
		foreach(@files)
		{
			my ($sign,$file)=$_=~/(\S+),(\S+)/;$list{$sign}=$file;
		}

	my @sample_name=sort keys %list;
	my $sample_num=scalar(@sample_name);
	my (%sample_ids,%total_ids);
		for(my $i=0;$i<$sample_num;$i++)
		{
			%{$sample_ids{$i}}=&read_list($list{$sample_name[$i]},\%total_ids);
		}

	$out_list="$out_dir/list.txt";

	open (OUT,">",$out_list)||die "Check your output file!\n";
	my $list_header="#ID\t".(join "\t",@sample_name);
	print OUT "$list_header\n";
		my %com_num;
		my %com_info;
		foreach my $id(keys %total_ids)
		{
			my $mark=10**$sample_num;
			for(my $i=0;$i<$sample_num;$i++)
			{
				if(exists $sample_ids{$i}{$id})
				{
					$mark+=10**$i;
				}
			}
			my @marks=split //,(reverse $mark);

			my (@com_samples,@infos);
			for(my $i=0;$i<$sample_num;$i++)
			{
				if($marks[$i])
				{
					push @com_samples,$sample_name[$i];
				}
				my $info=($marks[$i])?$id:"NA";       push @infos,$info;
			}
			my $com_samples=join ",",@com_samples;    
			$com_num{$com_samples}++;
			push @{$com_info{$com_samples}},$id;
			my $infos=join "\t",@infos;
			my $out_info=join "\t",($id,$infos);      
			print OUT $out_info."\n";
		}
	close OUT;

	$out_stat="$out_dir/stat.txt";
	open (OUT1,">",$out_stat)||die "Check your output file!\n";

	foreach(sort keys %com_num)
	{
		my $com_samples=$_;
		my $num=$com_num{$com_samples};
		my $info=join ",",@{$com_info{$com_samples}};
		my $out_info=join "\t",($com_samples,$num,$info);   print OUT1"$out_info\n";
	}
	close OUT1;



## sub functions
## read_list
sub read_list
{
	my ($file,$in_hash)=@_;
	my %hash;
	open IN,$file;
	if ($sample_file_head) {
		my $head_temp=<IN>;
	}
	while (<IN>)
	{
		chomp;
		next if /^\s*$/ || /^#/;
		my $id=(split /\s+/)[0];
		$hash{$id}++;
		$in_hash->{$id}++;
	}
	close IN;
	return %hash;
}
## help information
sub USAGE
{
	my $usage = <<"USAGE";
\nDescription: this script is used to process veen statitic && draw venn pictures;\n
Usage:     perl $0 -f T1,T1.list T2,T2.list -od .\n
Options:
     -f    <str>  file list. Eg: T1,T1.list T2,T2.list
     -od   <str>  output directiory
	-head	if the file have the head ,then give the parameter.else do not give this parameter.

Attention:(1) Id used for check should be in column 1.

USAGE
	print $usage;
	exit;
}
