import ppn 
import data_plot as dp
p=ppn.abu_vector('.')
cycles=range(0,126,25)
for cyc in cycles:   
   cycstr=dp.padding_model_number(cyc,999)
   figure(2,figsize=(14, 9))
   p.abu_chart(cyc,ilabel=True, imlabel=True,imagic=True,imlabel_fontsize=4,plotaxis=[46,110,33,82],\
               boxstable=True,lbound=(-9,-2),ifig=2)
   Nn=p.get('densn',fname=cyc)
   mod=p.get('mod',fname=cyc)
   title('$^{13}C-pocket$ $s$ $process, 3M_\odot, Z=0.02, mod=$'+str(mod)+', $  N_\mathrm{n}=$'+'%4.1F'%log10(Nn)+"$ cm^{-3}$")
   savefig('Abu'+cycstr+'.png',dpi=100)
   close(2)
   close(cyc)
   close(1);figure(1)
   p.elemental_abund(cyc,zrange=[33,80],ylim=[-9, -2])
   title('$^{13}C-pocket$ $s$ $process, 3M_\odot, Z=0.02, mod=$'+str(mod)+', $  N_\mathrm{n}=$'+'%4.1F'%log10(Nn)+"$ cm^{-3}$")
   savefig('elem'+cycstr+'.png')
