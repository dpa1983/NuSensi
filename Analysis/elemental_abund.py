#Script to compare the abundance distributions in mass fractions of elements of different runs
import ppn 
path='../results/'
pkr88d20=ppn.abu_vector(path+'run_r15792f0.05')      #Kr88d20
pkr8889d20=ppn.abu_vector(path+'run_r15792f0.05_r15805f0.05')    #Kr88Kr89d20
pkr878889d20=ppn.abu_vector(path+'run_r15779f0.05_r15792f0.05_r15805f0.05') #Kr87Kr88Kr89d20

pkr88d20.elemental_abund(512,zrange=[34,44],ylim=[-7,-4])
pkr8889d20.elemental_abund(512,zrange=[34,44],ylim=[-7,-4])
pkr878889d20.elemental_abund(512,zrange=[34,44],ylim=[-7,-4])
#legend
text(34.2,-6.7,'green: $^{88}$Kr(n,g)/20')
text(34.2,-6.8,'red: $^{88}$Kr, $^{89}$Kr(n,g)/20')
text(34.2,-6.9,'light blue: $^{87}$Kr, $^{88}$Kr, $^{89}$Kr(n,g)/20')
ylabel('$\log_{10}\,X$')
title('I process test at time step 512')
