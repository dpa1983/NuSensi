# run one-zone simulation
# execute this after you have set parameters
# in config.sh and then run compile.sh

function check_okay {
        if [ $error -ne 0 ]
        then
             echo $fail_warning
	     exit 1
        fi
}

[ -L ../NPDATA ]
error=$?; fail_warning="WARNING: ../NPDATA should be link and can not be found. Compile again in CODE."; check_okay

NPDATA_DIR=`readlink $PPN_DIR/frames/ppn/NPDATA`
echo "Using NPDATA in $NPDATA_DIR"

######### set input for i process example

######### PPN NUSENSI part below  #############

source ~/.bashrc
echo 'test out' >> out1
echo nice -n $NVAL ./ppn.exe >> out1
nohup nice -n $NVAL ./ppn.exe  >>out &    #|tee OUT
id=$!
#echo $id >>$job_path/log_$id

#wait for simulation, check if resulting .DAT files exist
echo 'stop at cycle(s): '${cycle[@]} >> out_test
IFS=','
cycle_array=($cycle)
iso_massf_file="iso_massf"${cycle_array[-1]}".DAT"
echo 'check  for file '$iso_massf_file >> out_test
while [ ! -f $iso_massf_file ]; do
	sleep 5
	#echo $id >>$job_path/log
done
#copy results
echo 'found DAT' >> out_test
for cycle_1 in "${cycle_array[@]}"
do
        iso_massf_file="iso_massf"$cycle_1".DAT"
        cp $iso_massf_file $path_results$filename"/"
        #echo $path_results$filename"/" >>$job_path/results_path
	#echo $iso_massf_file >>$job_path/log 
	#echo `pwd` >>$job_path/log
	#ls >>$job_path/ls_file
done



cp runinfo.txt $path_results$filename"/"
#save also isotopedatabase.txt to allow decay plots	
cp isotopedatabase.txt $path_results$filename"/"
#fd=`basename $PWD`

echo 'killing job' >> out_test

cd ..


#end PPN run
kill $id

#delete run dir
#for now save run dir
#delete Run_template on machine
echo "$delete_ppn_dirs" >> out_test
if [ "$delete_ppn_dirs" == "true" ]; then
	echo 'try delete' >> out_test
	`pwd` >> out_test
	echo $$filename >> out_test
	rm -vrf $filename >> out_test
fi

