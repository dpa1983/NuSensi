# set the following parameters:
PPN_DIR=../..

function check_okay {
        if [ $error -ne 0 ]
        then
             echo $fail_warning
	     exit 1
        fi
}

diff parameter.inc $PPN_DIR/frames/ppn/CODE/parameter.inc
error=$?
fail_warning="WARNING: parameter.inc is not the same as in CODE directory"
if [ $error -ne 0 ]
then
    echo $fail_warning
    echo "Attempting to fix this ..."
    cp parameter.inc $PPN_DIR/frames/ppn/CODE/
    cd $PPN_DIR/frames/ppn/CODE
    make distclean
    make
    cd -
    error=$?
    fail_warning="Error: Could not recompile automatically, try manually."
    check_okay
    echo "Automatic recompile apparently successful, now attempting to run ..."
fi


rm -f ../NPDATA
error=$?; fail_warning="WARNING: can not remove ../NPDATA"; check_okay
cp -R $PPN_DIR/frames/ppn/NPDATA ..
error=$?; fail_warning="WARNING: can not copy link NPDATA"; check_okay

$PPN_DIR/frames/ppn/CODE/ppn.exe |tee OUT

python $PPN_DIR/utils/pylib/examples/abu_chart.py 1 125 126 "\"plotaxis\"" = "[38,96,29,65]" "\"lbound\"" = "(-11,-3)" "\"imlabel\"" = False

echo Finished making *.png plots. Compare with master_results/*png.

