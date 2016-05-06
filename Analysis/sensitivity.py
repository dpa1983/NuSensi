#!/bin/python

''' PPN sensitivity calculation tool

    Adapted for general use + features added by Christian Ritter 12/12
    For suggestions & bug reports please contact critter@gsi.de    
 
    Based on scripts written by Alexander Koloczek and Benedikt Thomas 

    In the following you can find a short example how to use this script.
    As in other NuGrid analysis tools it is recommended using ipython
    with matplotlib and numpy. ppn.py must be in the PYTHONPATH for usage
    alias mpython='ipython -pylab -p numpy -editor emacsclient'

    Import the module

        In [1]: import sensitivity as sens

    read in the reference run:

	In [2]: runs=sens.read_ref_run(cycle=125,path='../src_template_c13_ref/')

    create the sensitivity matrix from all available runs in path_results:

        In [3]: runs.sens_matrix(path_results=["../results/"],factors=[0.9],filename='sensitivity_matrix.txt',decay=False)

    do a error analysis:

        In [4]: runs.error_matrix(sens_matrix="sensitivity_matrix.txt",filename='error_sensitivity_matrix.txt',abu_threshold = 2e-15)


'''

from numpy import * 
import os
import ppn as p

class read_ref_run():    
    ''' read PPN reference run

    '''

    def __init__(self,cycle=600,path='../src_template_c13_ref/'):


        '''
	Reads abundances of reference run. Reference run is simulation without any rate modifications.
	It has to be created by the user, for example by running a copy of the src_template.

        path_ :  path to reference ppn run
	cycle : cycle you want to use for the sensitivity calculations, e.g. cycle 125
	'''

	#self.path_baseline=path
	self.cycle=cycle
	#self.pwd=os.getcwd()
	#os.chdir(path_baseline)
	#get the baseline/reference run isotopes and abundances
	a=p.abu_vector(path)
	self.abuv=p.abu_vector(path)
	#self.def_abu=a.get('ABUNDANCE_MF',cycle)
	#self.isotopes_ref=a.get('ISOTP',cycle)
	#os.chdir(self.pwd)
		


    def sens_matrix(self,path_results=["../results/"],runs=[],factors=[0.9],filename='sensitivity_matrix.txt',decay=False,abu_threshold=1e-9):


        '''
        Calculation of sensitivity matrix from path_results dir containing sensitivity factors S_i_j
	for isotope i and rate j:

	S_i_j = (relative change of abundance of isotope i) / (relative change of rate j)
	      = (Delta_abu_i/abu_i) / (Delta_r_j/r_j)      (result rounded to third digit after the decimal point.)	

	The following four variables have the same meaning as in the nusensi.input file

	path_results : array containing the directory(s) with the results from the PPN runs
	factors : array contain the contain(s) factor(s) for rate change(s), e.g. 0.9
	runs: which runs to be selected in path_results?
		choose all results with []
		choose runs given by names, for example ['r48f0.01','r49f0.01']
		choose network range: [network_start,network_stop]
			network_start : reaction number of the start of network used for the sensitivity matrix
			network_stop  : reaction number of the end of network used for the sensitivity matrix
	decay : option to consider only decayed abundances; 


	Output matrix structure:

	| Isotopes  | Abundances(ref) | rate 1     | rate 2        | ....|
	| isotope 1 | X_1	      | S_1_1      | S_1_2	   | ....|
	| isotope 2 | X_2	      | S_2_1      | S_2_2	   | ....|
	| .....	    | .....	      | .....      | .....	   | ....|

	ref: Final abundances from reference run

        Experimental case:
        If more than on path is specified in path_results the rate and isotope specific
        sensitivity is calculated as as meanvalue of the sensitivities resulting from
        different factors

	'''


        # relative change of rates (since factor is rate/rate_ref)
        x=[]
        for i in range(len(factors)):
                x.append(factors[i] -1.)


	#for reference abundances
	if decay==False:
        	self.def_abu=self.abuv.get('ABUNDANCE_MF',self.cycle)
        	isotopes_all=self.abuv.get('ISOTP',self.cycle)
	else:	
		#if decayed abundances considered
		self.abuv.get(attri=self.cycle,decayed=True)
		self.def_abu=self.abuv.abunds
		isotopes_all=self.abuv.isotope_to_plot

	#for now take all isotopes
	num_iso=len(isotopes_all)
	isotopes=isotopes_all

	sens_matrix=[]

	#first line of sensitivity matrix
	sens_matrix.append([])
	sens_matrix[0].append('Isotope')
	for i in range(len(isotopes)):
		sens_matrix[0].append(isotopes[i])

	#second line with abundances from reference run
	sens_matrix.append([])
	sens_matrix[1].append('Abu')

	for i in range(len(self.def_abu)):
		abu = '{:.3E}'.format(self.def_abu[i])
		while len(abu)<11:
			abu = abu + ' ' 
		sens_matrix[1].append(abu)

	#from third line on, add for each rate/run


	## which runs to choose
	if len(runs) ==0:
		option=1
		runs1=os.listdir(path_results[0])
		print 'Found ',runs1
		rate_ids=runs1
	elif isinstance(runs[0],basestring):
		option=2
		rate_ids=runs
		print 'Found',runs

	else:
		option=3
		rate_ids=range(runs[0],runs[1]+1)
		print 'Found ',rate_ids 
	hh=-1
	for run in rate_ids: #range(network_start,network_stop+1):
		hh=hh+1
    		c=[]
		#read in rate information and add to matrix
		if option==3:
			f=open(path_results[0]+'run_r'+str(run)+'f'+str(factors[0])+'/runinfo.txt')
		else:
			f=open(path_results[0]+rate_ids[hh]+'/runinfo.txt')
    		line=f.readline() 
    		sens_matrix.append([])
    		if line[43:44] == '*' or line[43:44] == 'g' :
    			sens_matrix[len(sens_matrix)-1].append(line[14:19]+line[80:85]+line[43:44])
    		else :
    			sens_matrix[len(sens_matrix)-1].append(line[14:19]+line[80:85])
    		#read in abundance (of all results if experimental case)
    		for i in range(len(path_results)):
			if option==3:
				c.append(p.abu_vector(path_results[i]+'/run_r'+str(run)+'f'+str(factors[i])))
			else:
				c.append(p.abu_vector(path_results[i]+'/'+rate_ids[hh]))
		# decay abundances, then available in abunds variable
		if decay==True:
			c[i].get(attri=self.cycle,decayed=True)

		#for each isotope in chosen isotope range calculate sensitivity factor
		c[i].get(attri=self.cycle,decayed=True)
    		for isoj in range(0,num_iso):
			ylist=[]
			#get abundance of isotope (more than one loop only in experimental case)
			for i in range(len(path_results)):
				if decay == False:
					ylist.append(c[i].get('ABUNDANCE_MF',self.cycle)[isoj])
				else:
					ylist.append(c[i].abunds[isoj])
			# relative change of abundance: (abundance - abundance_ref)/(abundance_ref)

                        if (isoj==15) and (run==238):
                                print '############### N-15, abu: ',y
			y=ylist/self.def_abu[isoj]-1
	
			# Definition of sensitivity factor! relative change of abundance / relative change of rate;
			sens_factor = meanvalue(y/x) #round! input parameter?   (meanvalue necessary only if experimental case)

			#check that sens factor from element above abu_threshold
			if ((meanvalue(ylist) <= abu_threshold) and (self.def_abu[isoj]<abu_threshold)):
				sens_factor = 0.0
			if (abs(sens_factor) == 0.0):
				sens_factor=abs(sens_factor)
			sens_factor_form='{:.3E}'.format(sens_factor)
			if (sens_factor>=0):
				sens_factor_form = ' '+sens_factor_form
			if (isoj==15) and (run==238):
				print '############### N-15, ref abu: ',self.def_abu[isoj]
				print '############## sens fac: ',sens_factor
			sens_matrix[len(sens_matrix)-1].append(sens_factor_form)
	#os.chdir(self.pwd)
	#print 'Create sensitivity matrix in sensitivity_matrix_full.txt in current dir'
	out = open(filename,"w")
	for i in range(len(sens_matrix[2])):
		for j in range(len(sens_matrix)):
			while len(str(sens_matrix[j][i])) < 11 :
				sens_matrix[j][i] = str(sens_matrix[j][i]) + ' '
			out.write(str(sens_matrix[j][i]) + '	')
		out.write('\n')
	out.close()
	print 'Created sensitivity matrix in file '+filename   
 
    def error_matrix(self,sens_matrix="sensitivity_matrix.txt",filename='error_sensitivity_matrix.txt',abu_threshold = 2e-15,sens_threshold = 0.01,filter_stable='false',iso_filter=['false']):

	'''
	One can calculate the errors attached to each sensitivity factor in the created sensitivity matrix
	sens_matrix by taking into account the rate errors provided in error.txt:
	
	sensitivity error =  (+/- rate error*sensitivity )

	The function reads in the sensitivity matrix sens_matrix and extents matrix by adding the errors.
	Filter and thresholds can be applied.

	sens_matrix : name of file containing the sensitivity matrix created with the function calculate_matrix
        filename :  Saves error matrix in filename.

 	filter_stable : default 'false': use all isotopes provided in the sensitivity matrix 
		        if true: only stable isotopes identified via file stable.txt (stable.txt: s)
		        if long: stables + long-lived isotopes (stable.txt: s+l)
	iso_filer : list of isotopes of interrest, e.g. ['Ni-56','Se-76']; if ['false'] take all isotopes
		    One can also choose all isotopes of specific elements ['Ni','Se'].

	abu_threshold :  isotopes with abundances below threshold are ignored
	sens_threshold : if sensitivities of rates corresponding to an isotope are below threshold, 
			 they will be ignored, same for isotopes corresponding to
        		 rate (see rates - isotopes plain of matrix)
	
        Output matrix structure:

        | Isotopes   | Abundances | rate 1     		   | rate 2     	  	| ....|
        | isotope 1  | X_1        | S_1_1 (+/-error*S_1_1) | S_1_2 (+/-error*S_1_2) 	| ....|
        | isotope 2  | X_2	  | S_2_1 (...)            | S_2_2 (...)   	  	| ....|
	| .....      | .....      | .....      		   | .....      	  	| ....| 


	'''

	source_file = sens_matrix
	new_file = filename #output_file                       
	stable_file = 'stable.txt'      # file with list of stable elements
	error_file = 'error.txt'   #file with rate errors 

	#read in sensitivity matrix
	sens_mat = load_matrix(source_file)

        #for i in range(2,len(array(sens_mat).T)): #rate loop
        #        print 'check rate ',array(sens_mat).T[i][0]


	#Apply iso filter to matrix
	if not iso_filter[0] == 'false':
        	new_mat = []
        	new_mat.append(sens_mat[0])
        	for i in range(1,len(sens_mat)):
                	for j in range(len(iso_filter)):
                        	if sens_mat[i][0][0:len(iso_filter[j])] == iso_filter[j]:
                                	new_mat.append(sens_mat[i])
        	sens_mat = new_mat

	#Apply stable filter to matrix by using the information in stable.txt
	if filter_stable == 'true':
		print 'This might take a moment..'
        	new_mat = []
        	new_mat.append(sens_mat[0])
        	for i in range(1,len(sens_mat)):
                	if is_stable(sens_mat[i][0],stable_file) == 't':
                        	new_mat.append(sens_mat[i])
        	sens_mat = new_mat
	# in case the long-lived isotopes need to be added to the stable isotopes.
	elif filter_stable == 'long':
		print 'This might take a moment..'
        	new_mat = []
        	new_mat.append(sens_mat[0])
        	for i in range(1,len(sens_mat)):
                	if (is_stable(sens_mat[i][0],stable_file) == 't') or (is_stable(sens_mat[i][0],stable_file) == 'l'):
                        	new_mat.append(sens_mat[i])
        	sens_mat = new_mat

	#if abundance of isotopes is below threshold abu_threshold discard
	new_mat=[]
	new_mat.append(sens_mat[0])
	for i in range(1,len(sens_mat)):
        	if abs(float(sens_mat[i][1])) > abu_threshold :
                	new_mat.append(sens_mat[i])
	sens_mat = new_mat

	#as long as sensitivity of a certain rate is above threshold, 
	#include this rate (column) in the table
	trans_mat = array(new_mat).T
	new_trans_mat= []
	new_trans_mat.append(trans_mat[0])
	new_trans_mat.append(trans_mat[1])
	#loop over rates
	for i in range(2,len(trans_mat)):
		#loop over isotopes, is rate relevant, any entry above sens_threshold?
        	for j in range(1,len(trans_mat[i])):
                	if abs(float(trans_mat[i][j])) >=sens_threshold:
				#if yes, add whole rate entry and go to next rate
                        	new_trans_mat.append(trans_mat[i])
                        	break
			if  j == (len(trans_mat[i])-1):
				print 'Sensitivities of rate ',trans_mat[i][0],' below threshold. Skip rate.'
	
	trans_mat = new_trans_mat
	#trans_mat=sens_mat
	#######error calculations#######

	#read in errors from errors.txt
	error_mat = loadtxt(error_file ,delimiter='\t', dtype='string')

	new_trans_mat = []
	new_trans_mat.append([])
	new_trans_mat.append([])
	new_trans_mat[0].append(trans_mat[0][0])
	new_trans_mat[1].append(trans_mat[1][0])
	#new_trans_mat[0].append(' ')
	#new_trans_mat[1].append(' ')
	#add all isotopes and abundances(ref)
	for i in range(1, len(trans_mat[0])):
		new_trans_mat[0].append(trans_mat[0][i])
        	new_trans_mat[1].append(trans_mat[1][i])

	#add sensitivities of each rate, including the errors
	for i in range(2,len(trans_mat)): #rate loop
		#print 'check rate ',trans_mat[i][0]
        	count = 0
        	new_trans_mat.append([])
        	new_trans_mat[i].append(trans_mat[i][0])
		#loop over isotopes with errors 
        	for j in range(len(error_mat)):
			#if isotope exists in sens matrix
                	if trans_mat[i][0] == error_mat[j][0]:
				#loop over rates
                        	for k in range(1,len(trans_mat[i])):
					#add plus sign if positive
                                	if abs(float(trans_mat[i][k])) == float(trans_mat[i][k]):
                                        	trans_mat[i][k] = '+' + trans_mat[i][k]
					#element=trans_mat[i][k]
                               		#while len(element) < 7:
                                        #	element = element + ' '
					#calculate error: sens factor * rel. Error [%]
					error_factor=abs(float(trans_mat[i][k])*float(error_mat[j][3][:-1]))
					error_factor_format=' ('+'{:.2E}'.format(error_factor)+'%)'
                                        while len(error_factor_format) < 11:
                                                error_factor_format = error_factor_format + ' '
                                	new_trans_mat[i].append(trans_mat[i][k]+error_factor_format)
                        	count = 1
                        	break

			#if error.txt for rate is not available
                	if j == len(error_mat)-1 and count == 0:
                        	print('Error value of rate '+trans_mat[i][0] + ' not in available in error.txt. Skip rate.')
				#loop over rates
                        	for k in range(1,len(trans_mat[i])):
                                	if abs(float(trans_mat[i][k])) == float(trans_mat[i][k]):
                                        	trans_mat[i][k] = '+' + trans_mat[i][k]
					element=trans_mat[i][k]
                                	while len(element) < 11:
                                        	element = element + ' '
					#write sens error as '-'
                                	new_trans_mat[i].append(element+'(-)')


	#tmp_mat=array(new_trans_mat).T

	'''
	new_mat=[]

	# copy first header
	new_mat.append([])
	new_mat[0].append(tmp_mat[0][0])
	new_mat[0].append(tmp_mat[0][1])
	new_mat[0].append('Error (sqrt)')
	for i in range(2,len(tmp_mat[0])):
        	new_mat[0].append(tmp_mat[0][i])

	#copy 2nd header
	new_mat.append([])
	new_mat[1].append(tmp_mat[1][0])
	new_mat[1].append(tmp_mat[1][1])
	new_mat[1].append(' ')

	for i in range(2,len(tmp_mat[1])):
        	new_mat[1].append(tmp_mat[1][i])

	for i in range(2,len(tmp_mat)):
        	new_mat.append([])
        	new_mat[i].append(tmp_mat[i][0])
        	new_mat[i].append(tmp_mat[i][1])
        	new_mat[i].append(0)    #error sqrt
        	for j in range(2,len(tmp_mat[i])):
        	        new_mat[i].append(tmp_mat[i][j])

	# calculate square root of mean error 
	for i in range(2,len(new_mat)):
        	sumsqrt = 0
		counts=0
        	for j in range(3,len(new_mat[i])):      #4: iso+abu+error
                	error = new_mat[i][j][8:len(new_mat[i][j])-3]
                	if len(error) > 0:
                        	sumsqrt = sumsqrt + float(error)*float(error)
				counts = counts +1
        	sumsqrt = sqrt(sumsqrt/counts)
        	new_mat[i][2]='+-'+str(round(abs(sumsqrt),1))+'%'
	sens_mat = new_mat
	'''
	sens_mat = array(new_trans_mat).T #tmp_mat	

	write_matrix(sens_mat, new_file)
	print 'Error matrix in file '+new_file+' created.'
	#str(len(sens_mat[0])-1)+'x'+str(len(sens_mat)-1)+' matrix created' )


###############Intern functions which should not be called by the user


def meanvalue(liste):
	summe = 0
	for i in range(len(liste)):
		summe = summe + liste[i]
	return summe/len(liste)



def load_matrix(mat_file):

	'''
		Loads sensitivity matrix written by calc_matrix
	'''


	new_mat=[]
        file=open(mat_file,'r')
        first_line = file.readline()

        liste=[]
        for i in range(len(first_line)/12):
                liste.append(first_line[12*i:12*(i+1)])
        for i in range(len(liste)):
                if not ((liste[i][10:11]==' ') or (liste[i][10:11]=='\t') or (liste[i][10:11]=='\n')):
                        liste[i] = liste[i][:11]
                else :
                        liste[i] = liste[i][:10]
        new_mat.append(liste)

        for line in file.readlines():
                sens_line = line.split()
                new_mat.append(sens_line)
        file.close()
        return new_mat

def write_matrix(matrix, file_name):
	out=open(file_name,'w')
	for i in range(len(matrix)):
                for j in range(len(matrix[i])):
			element=matrix[i][j]
                        while len(element) < 18 :
                                element = str(element) + ' '
                        out.write(str(element))
                out.write('\n')
        out.close()


def is_stable(isotope,stable_file):
        stable_list = loadtxt(stable_file, dtype='string')
        for i in range(len(stable_list)):
                if isotope == stable_list[i][0]:
                        return stable_list[i][1]
                        break



