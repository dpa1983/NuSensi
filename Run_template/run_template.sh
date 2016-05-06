#!/bin/bash
#Prepares ppn run. 


template=src_template
#i=$run
#i="${run:1}"
filename=$run #"run_"$i"_factor_"$factor
#filename="run_""${i:1}""_factor_"$factor

#create dir for simulation results in path_results
mkdir $path_results$filename	


#finally create run dir
mkdir $filename
cd $filename
cp  ../$template/* .
#echo 'test run',$i >> testfile
#####1110 start line with reactions in networksetup.txt

lines=`sed -n "/NGIR/{=;p;}" networksetup.txt`

IFS='
'
array=( $lines )
line=${array[0]}

#linecalc=$(($i+$line))

#echo 'test i',$i >> testfile
#echo 'test ',$line >> testfile
#echo 'test sum',$linecalc >>testfile
#1.000E+00
#factorsci=`printf '%.3E' $factor`

#create array with each reaction rate to change
IFS='_' read -a arrayrates <<< "$run"
#remove first zero element
#arrayrates=("${arrayrates[@]:1}")
#IFS='_ ' read -a array <<< "$a"
export LC_NUMERIC="en_US.UTF-8"
for element in "${arrayrates[@]:1}"
do
	echo 'test element',$element >> testfile
# 1507  IFS='_ ' read -a split_array <<< "$a"
 	IFS='f ' read -a split_element <<< "$element"
 	element=${split_element[0]:1}
 	factor=${split_element[1]}
	echo 'nametest''f'$factor'r'$element >> testfile
	#echo 'test sum',$linecalc >>testfile
	linecalc=$(($element+$line))
	factorsci=`printf '%.3E' $factor`	
	sed -r "$linecalc ~ s/^(.{92})(.{9})/\1$factorsci/" networksetup.txt > networksetup.txt.tmp; mv networksetup.txt.tmp networksetup.txt 
	awk -v line=$linecalc 'NR == line {print}' networksetup.txt >> runinfo.txt
done

. run_sens.sh >>run_sens.out 2>>run_sens.err & 
