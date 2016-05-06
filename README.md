NuGrid Sensitivity Tool (NUSENSI)
=======

Contains the NUSENSI tool for
rate test calculations with the single-zone PPN and analyze
the results with ipython.


    02/15: CR: Updated and new features
    12/12: Adapted for general use + features added C. Ritter
    For suggestions or bug reports please contact critter[at]uvic.ca    
 
    Based on scripts written by A. Koloczek and B. Thomas 

Contains the NUSENSI tool for
rate test calculations with the single-zone PPN and analyze
the results with ipython.
Multiple PPN runs can be started in parallel, each
with specified modification of rates.


General approach:

1. Start PPN runs by using scripts in the Jobs dir.
   These scripts create copies of the Run_template dir which contains the ppn run directory
   src_template.
2. Do the sensitivity analysis by using scripts in the Analysis dir.

Note: Each sub-directory has its README file for more details

Instructions:

1.
   Adapt the Run_template dir and provide your ppn run directory for the tests.
   See the README file in Run_template for the instructions. 
   Note that the ppn hif example is set as default in Run_template.
2. 
   To run the rate test simulations follow the instructions in the Jobs README file.
3. 
   If necessary use the analysis dir. For more information about analysis features see the README in
   in the Analysis dir. 



