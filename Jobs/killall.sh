#!/bin/bash

###Read in the adresses of the machines you want to use
IFS='
'
machines=( $( < machines ) )


for machine in "${machines[@]}"
do
        IFS=' '
        machine_array=($machine)
	ssh ${machine_array[0]}  "killall screen;killall -9 ppn.exe" >/dev/null 2>&1
done

#in case of 'Device or resource busy' when deleting directories:
#lsof +D /directory/with/resourcebusy/

