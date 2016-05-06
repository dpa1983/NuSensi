#!/bin/bash -x

#. ~/.bashrc
#Executed for every machine defined in machines file. Creates for ppn
#a dir in ppn_path which inherits all run dirs. 

####Environment variables below will be set by execution of run_all_machines.sh
path_results="/nfs/rpod2/critter/SensitivityStudies/video_tutorial/NUSENSI/results/"
ppn_path="/nfs/rpod2/critter/SensitivityStudies/video_tutorial/NUSENSI/simulations/"
#PPN_DIR="ppn_dir_replacement"
#factor=0.01
network_start=229
network_stop=230
cycle=(00512)
NVAL=19
procs=$1
delete_ppn_dirs=false
#####

set -- `svn info| grep Revision`
REV=$2
system=`hostname -s`
job_path=`pwd`

#echo $system >> out.$system
#echo $ppn_path >>out.$system
#system_workdir=$ppn_path"/"$system"/"
#mkdir $system_workdir
#echo $system_workdir >> out
cp -rf ../Run_template $ppn_path'/Runs_'$system  #$system_workdir
#cd $system_workdir/Run_template
cd $ppn_path'/Runs_'$system

echo 'procs: '$procs >> out
if [ $procs -gt 0 ]; then
   cores=$procs

else
   cores=`grep -i processor /proc/cpuinfo | wc -l`
fi

lines_available=1
typeset -x JOB_PATH=$job_path
while [ $lines_available -gt 0 ]
do
	#echo 'test loops1, cores: '$cores >> out.$system
	#whenever a core is available for ppn, another simulation will be started
	while [ "$(ps --no-headers -C ppn.exe | wc -l)" -lt "$(($cores))" ]
	do
		#echo 'test loops' >> out.$system
		line=$(perl <<"EOF"
			my($baseName) = $ENV{"JOB_PATH"} . '/runlist';
			my($lockFile) = $baseName . '.lck';
			my($oldName)  = $baseName . '.txt';
			my($newName)  = $baseName . '.tmp';

			open(LOCK, '>', $lockFile) || die "cannot open $lockFile: $!";
			flock(LOCK, 2);

			open(LIST_OLD, '<', $oldName) || die "cannot open $oldName: $!";
			open(LIST_NEW, '>', $newName) || die "cannot open $newName: $!";
			my $firstLine = <LIST_OLD>;
			while(<LIST_OLD>)
			{
				print LIST_NEW $_;
			}
			close(LIST_NEW);
			close(LIST_OLD);

			rename($newName, $oldName);
			unlink($lockFile);
			
			flock(LOCK, 8);
			close(LOCK);
			print $firstLine;
EOF
		)
		if [ -z "$line" ];
		then
			lines_available=0
			#echo 'no lines' >> out.$system
			break;
		fi

		#set run number
		#IFS='run' read -a array <<< "$line"
		run=$line  #$"${array[-1]}"
		echo 'test'$run >> out
		info=`hostname`
		echo 'execute run_template.sh' >> out
		#run="${line:15:50}"
		. run_template.sh &  
		sleep 10

	done

	sleep 60
done
#To make sure all results exist before ending script
IFS=','
test_cycle=($cycle)
while [ "$(find $path_results -name iso_massf${test_cycle[-1]}.DAT | wc -l)" -lt $(($network_stop-$network_start+1))  ]
do
        sleep 60
done
#delete Run_template on machine
#if [ "delete_ppn_dirs" -eq "True" ]; then
#	cd $ppn_path 
#	rm -rf $system
#fi


