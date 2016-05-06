# run this after initializing el_ratios via the elemental.py script
form_str='%5.2F'

lines=['g:o', 'r-.v', 'k-*', 'b-->', 'k-.D', 'b-.x', 'r-.<', 'b-', 'c--', 'm--', 'g--']
#labels=['$i\mathrm{-process\ 1-zone}$','$\mathrm{lower\ } H/^{12}C$','$\mathrm{lower\ } \\rho$', '$\mathrm{lower\ } Z$', '$^{135}I(n,\gamma) \\times 20$', '$^{135}I(n,\gamma) \\times 5$','JINA reaclib']
labels=['$i\mathrm{-process\ 1-zone}$', '$^{135}I(n,\gamma) \\times 5$','$^{135}I(n,\gamma) \\times 20$']
# conditions for plotting:
el_cond = 'Ba'
cond_log_gt = 3.

elx=['Ba','La']   # [elx[0]/elx[1]]
ely=['La','Eu']
ifig=33

for j in range(len(all_cycles)):
#if False:
	cycles    = all_cycles[j]
	run_label = all_run_labels[j]
	el_ratios = all_el_ratios[j]
	el_this_plot_ratios = []
	for i in range(len(cycles)-1): # substract 1 because we do not want the first 
		els_dmp=[]             # cycle in ratios, 1st cycle contains initial 
		if el_ratios[i][where(array(el_name)==el_cond)[0][0]] > 10**cond_log_gt:
			for this_el in elx+ely:
				els_dmp.append(el_ratios[i][where(array(el_name)==this_el)[0][0]])
			el_this_plot_ratios.append(els_dmp)

	xxx=transpose(array(el_this_plot_ratios))
	figure(ifig)
#	plot(log10(xxx[0]/xxx[1]),log10(xxx[2]/xxx[3]),lines[j],label=run_label)
	plot(log10(xxx[0]/xxx[1]),log10(xxx[2]/xxx[3]),lines[j],label=labels[j])
	xlabel('['+elx[0]+'/'+elx[1]+']')
	ylabel('['+ely[0]+'/'+ely[1]+']')
	ylabel('['+ely[0]+'/'+ely[1]+']')
	legend()
