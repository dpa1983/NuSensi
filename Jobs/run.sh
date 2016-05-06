#!/bin/bash

#read in input file
source nusensi.input

printisos() {
     ele="$1"
     found=0
        if [[ "$ele" == "H" ]]; then
           echo 'H 1'
        fi
     foundiso=0
     while IFS='' read -r line || [[ -n "$line" ]]; do
     #echo "Text read from file: $line"
     if [[ $line == *"****"* ]]
	then
	if [[ "1" -eq "$found" ]];
	then
	    break
	fi
	found=1
	
     fi
     ele1=${line:15:2}
     #iso1=`hg st -R "$iso1" | sed -e 's/  *$//'`
     ele1=`echo -n "${ele1//[[:space:]]/}"`
     #echo 'test: '$ele' '$ele1
     if [[ "$ele1" == "$ele" ]]
	then
	#echo 'truefalse: '${line:25:1}
	#is iso in network
	if [[ ${line:25:1} == "T" ]]
	  then
	  echo ${line:15:5}
	  foundiso=1
        fi 	
     fi
     done < ../Run_template/src_template/networksetup.txt	
     if [[ "$foundiso" -eq "0" ]]; then
	echo 'No isotopes found. Try again.'
	continue
     fi	
}

getrateid() {
	#echo 'start getrateid'
	found=0
	foundrate=0
        rate=$1
	ratefactor=$3
        iso=$2
        rate="$(echo -e "${rate}" | sed -e 's/^[[:space:]]*//')"
        iso="$(echo -e "${iso}" | sed -e 's/^[[:space:]]*//')"
	#echo 'look for |'$rate"$iso"'|'
     while IFS='' read -r line || [[ -n "$line" ]]; do
	if [[ $found -eq "0" ]]
	 then
	 if [[ $line == *"NGIR"* ]]
	    then
		#echo 'found NTGIR'
		found=1
	 fi
	 continue
	fi
	# rate and isotope must match
	#echo $line $1 $2
	if [[ $line == *"$rate"* ]] && [[ ${line:0:36} == *"$iso"* ]]
	  then
        #is rate in network
          if [[ ${line:8:1} == "T" ]]
            then
            echo ${line:0:88} >> rateslist.log
	    rateid=${line:0:7}
	    rateid="$(echo -e "${rateid}" | sed -e 's/^[[:space:]]*//')"
	    #echo $line
	    #echo 'rate ID: '$rateid
	    echo 'run_r'"$rateid"'f'"$ratefactor" >> runlist.txt
	    foundrate=1
          fi
        fi
     done < ../Run_template/src_template/networksetup.txt
	if [[ "$foundrate" -eq "0" ]]; then
		echo 'For '"$iso""$rate"' no rate found. Try again.'
	fi
}






#to get absolute paths
ppn_path=`readlink -f $ppn_path`/
path_results=`readlink -f $path_results`/

#to create run.list
if [ $inirates -eq 2 ] || [ $inirates -eq 0  ]
then
###Create runlist
#if [ -f "runlist.txt" ]; then
   #echo "Warning:runlist.txt already exists, overwrite? [yes/no]"
   #read answer
   #if [ "$answer" == "yes" ]; then
	if [ -f "runlist.txt" ]; then
		echo 'Overwrite runlist.txt? (y/n)'
		read overr
		if [[ "$overr$" == "y" ]]; then
		   rm runlist.txt
		fi
	fi

	echo '############################################################'
	echo '###### Interface to prepare runs (populate runlist.txt) ####'
        echo '############################################################'
	echo 'How do you want to select network?'
	echo 'Single[1], Network[2]'
	read choice_netw
        if [ "$choice_netw" -eq "1" ]; then

            if [ -f "rateslist.log" ]; then
                echo 'Overwrite rateslist.log? (y/n)'
                read overr
                if [[ "$overr$" == "y" ]]; then
                   rm rateslist.log
                fi
            fi  
            


	    echo 'Factor by which you want to change rate (0.02 means factor 50 down)?'
	    read ratefactor
	    echo 'Which rates do you consider?'
	    echo 'all[1], (n,g)[2], (p,g)[3] ?'
	    read ratechoice_inp
	    ratechoice=( '|(p,g)|(v,v)|(+,g)|(g,p)|' '(n,g)' '(p,g)' )
	    IFS='| ' read -r -a ratechoicearray <<< "${ratechoice[$ratechoice_inp-1]}"
	    while [ 1 ]
	      do
	      echo 'Which element (e.g. FE)? Press q to exit selection.'
	      read element
	      if [[ "$element" == "q" ]]; then
		        break
	      fi
              if [[ "$element" == "NEUT" ]] || [[ "$element" == "NEUTRON" ]]; then
                echo 'Neutron cannot be chosen. Try again.'
                continue
	      fi
	      echo 'Available isotopes:'
	      printisos $element
	      echo 'List your mass numbers (A)'
	      read Ain
	      #depending on ratechoice get rates
	      IFS=',' read -r -a  aarray <<< "$Ain"	
	      for A in "${aarray[@]}"
	        do
		 for rate in "${ratechoicearray[@]}"   
		   do
			#echo 'A'${#A}'elem'${#element}
			nspaces=$(( 5 - ${#A}-${#element}))
			#echo 'number of spaces '$nspaces
			if [[ $nspaces -eq 0 ]];then
				space=""
			else
				space=`printf "%${nspaces}s" " "`
			fi
			#echo '|'"$space"'|'
			#echo 'found space: '$space
			iso=`printf "$element""$space""$A"`
			if [[ "$iso" == "H   1" ]]; then
				iso="PROT "
			fi
			#if [[ '$iso' == 'N  1' ]]; then
			echo 'Look for '$iso$rate
		        getrateid $rate "$iso" $ratefactor
		   done
	        done
	    done
            if [ $inirates -eq 0  ]; then
             echo 'Check runlist.txt for choice of rate modifications.'
	     echo 'rateslist.log helps to idenfify the rate to each rate ID.'
             echo 'To run simulations execute run.sh with inirates=1 in nusensi.input.'
             #continue #return #exit
	    else
	     echo 'Created runlist.txt and rateslist.log with choice of rate modifications.'
            fi
	fi	
	if [ "$choice_netw" -eq "2" ]; then
	    echo 'Read size of network from nusensi.input.'
	    test_cycle=($cycle)
	    #check if the run results already exist by looking for the last .DAT file
            for ((i=$network_start;i<=$network_stop;i=i+1)); 
		do file=$path_results"run_r"$i"f"$factor"/iso_massf"${test_cycle[-1]}".DAT";  [ -f $file ] && continue; echo "run_r"$i"f"$factor >> runlist.txt;  
		done;
            if [ $inirates -eq 0  ]; then
             echo 'Check runlist.txt for choice of rate modifications.'
             echo 'To run simulations execute run.sh with inirates=1 in nusensi.input.'
             #endnow=true #return
            else
	     echo 'Created runlist.txt with choice of rate modifications.'
	    fi
        fi

elif [ $inirates -eq 1 ]; then
    echo 'Read input from runlist.txt'
else
    echo 'Wrong choice of input parameter inirates, stop'
fi

if [ ! $inirates -eq 0  ]; then
    #test_cycle=($cycle)
    #for ((i=network_start;i<=$network_stop;i=i+1));
#	do file=$path_results"run_"$i"_factor_"$factor"/iso_massf"${test_cycle[-1]}".DAT";  [ -f $file ] && continue; echo factor"_"$factor"_run_"$i  >> runlist.txt;
#        done;
 #   echo "runlist as runlist.txt created"

###Chance to change runlist.txt
#echo -n "Do you want to edit runlist.txt? [yes/no] "
#read answer
#if [ "$answer" == "yes" ]; then
#  echo "Changes done? [yes]"
#     read answer 
#fi

###Read in the adresses of the machines you want to use
IFS='
'
machines=( $( < machines ) )

#rm run_single_machine.sh
cp run_machine_template.sh run_machine.sh
#Set environment for script used on different machines. Needed because of the ssh connection.
sed -i "s|path_results_replacement|$path_results|g" run_machine.sh #un_single_machine.sh  > run_single_machine.sh.1
sed -i "s|ppn_path_replacement|$ppn_path|g" run_machine.sh #run_single_machine.sh.1  > run_single_machine.sh.2
#sed -i "s|ppn_dir_replacement|$PPN_DIR|g" run_machine.sh  #run_single_machine.sh.2  > run_single_machine.sh.3
sed -i s/factor_replacement/$factor/ run_machine.sh  #run_single_machine.sh.3  > run_single_machine.sh.4
sed -i s/network_start_replacement/$network_start/ run_machine.sh  #run_single_machine.sh.4  > run_single_machine.sh.5
sed -i s/network_stop_replacement/$network_stop/  run_machine.sh   # run_single_machine.sh.5  > run_single_machine.sh.6
sed -i s/cycle_replacement/$cycle/ run_machine.sh #run_single_machine.sh.6  > run_single_machine.sh.7
sed -i s/nval_replacement/$NVAL/ run_machine.sh  #run_single_machine.sh.7  > run_single_machine.sh.8
#sed -i s/delete_ppn_dirs/$delete_ppn_dirs/ run_machine.sh  #run_single_machine.sh.8  > run_single_machine.sh
sed -i s/deleteppndirreplacement/$delete_ppn_dirs/ run_machine.sh
#rm run_single_machine.sh.*

time=.1
currentdir=`pwd`

#check if sum of procs <= networksize
#networksize=$(($network_stop -$network_start +1))
sumprocs=0
for machine in "${machines[@]}"
do
	#ignore comments
	#echo 'machine '$machine'xxx'${machine:0:1}
	if [ ${machine:0:1} == '#' ]; then
		#echo 'skip '$machine
		continue
	fi
        IFS=' '
        machine_array=($machine)
        let  ${machine_array[1]}
	sumprocs=$(($sumprocs + $procs))
done

awk '!/#/' machines > temp
IFS='
'
machines=( $( < temp ) )
rm temp
#here I remove all comments from runlist.txt
#sed -i '' '/#/d' ./runlist.txt
awk '!/#/' runlist.txt > runlist.hist.txt #&& mv temp runlist.txt
numberruns=`wc -l < runlist.hist.txt`
#echo $sumprocs
#echo $numberruns
if [ "$sumprocs" -gt "$numberruns" ] ; then
        echo "Stop: Sum of procs of all machines specified in machines file must be smaller or equal to number of runs in runlist.txt!"
        #return #exit 1
else

readarray runnames < runlist.hist.txt

###Start runs
i=0
for machine in "${machines[@]}"
do
	IFS=' '
        machine_array=($machine)
	#echo 'testst'$
	let  ${machine_array[1]}
	#echo 'test'${machine_array[1]}
	echo 'Check for jobs in runlist.txt on machine '${machine_array[0]}
	ssh -tv ${machine_array[0]} "cd $currentdir;screen -d -m ./run_machine.sh $procs; sleep $time" > out 2>err
	#>/dev/null 2>&1
done

if [ $delete_ppn_dirs ]; then

	echo 'Run dirs in '$ppn_path$' will be automatically deleted after runs finisshed.'
	echo 'Results can be found in '$path_results
fi

######To follow the progress
echo 'Calculation in progress...' 
while true; do
     linetest=`wc -l < runlist.hist.txt`
     if [ $linetest -eq "0" ]; then
	break
     fi
     sleep 30

done
echo 'Last runs started...'

#Are all results available?
#echo 'Waiting until all results are in '$path_results' available'
while true; do
	missing=false
	#echo 'Test for files'
	for run in "${runnames[@]}"
	do
		run1=`echo $run | tr -d '\n'` 
		#run1=${run
		fullp=$path_results'/'$run1'/isotopedatabase.txt'	
		#echo 'test '$fullp
		if [ ! -f "$fullp" ]; then
		   #echo 'Could not find '$run1'/isotopedatabase.txt'
		   missing=true	
		fi
	done
	#all finsihed
	if [ $missing == 'false' ]; then
		break
	fi

	sleep 30
done
echo '##### Done: All results available ####'
fi #enough procs
fi #not [ $inirates -eq 0  ]
