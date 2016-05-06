import utils
p=utils.iniabu('../../mppnp/USEEPP/iniab1.0E-03GN93.ppn')
#p=utils.iniabu('iniab1.0E-02.ppn_asplund05')
sum=p.habu['c  12']+p.habu['o  16']+p.habu['h   1']
sp={}
sp['h   1']=0.2
sp['c  12']=0.5
sp['o  16']=sum-sp['h   1']-sp['c  12']
p.set_and_normalize(sp)
p.write('p_ini.dat','initial abundance iniab1.0E-03GN93.ppn')
