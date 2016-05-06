#
# CR: Most functions adapted from NuGridpy package
# by the NuGrid Team




from sensitivity import load_matrix
from numpy import *
import matplotlib.pyplot as pl
from matplotlib.ticker import *
from matplotlib import colors,cm
import astronomy as ast
import matplotlib
from matplotlib.patches import Rectangle, Arrow
from matplotlib.collections import PatchCollection
from matplotlib.offsetbox import AnchoredOffsetbox, TextArea
from matplotlib.lines import Line2D
from matplotlib.ticker import *
from collections import OrderedDict
import numpy as np
import os
import threading
import time
import sys


class plot_sens():

    '''
	Plotting results from the sensitivity matrix
    '''

    def __init__(self,sens_matrix='sensitivity_matrix.txt'):

        #read in sensitivity matrix
        sens_mat = load_matrix(sens_matrix)

	self.sens_mat=sens_mat


        self.stable_el = [['Neutron','999'],['H',1, 2],['He', 3, 4],['Li', 6, 7],['Be', 9],
                 ['B', 10, 11],['C', 12, 13],['N', 14, 15],['O', 16, 17, 18],['F', 19],
                 ['Ne', 20, 21, 22],['Na', 23],['Mg', 24, 25, 26],['Al', 27],['Si', 28, 29, 30],
                 ['P', 31],['S', 32, 33, 34, 36],['Cl', 35, 37],['Ar', 36, 38, 40],['K', 39, 40, 41],
                 ['Ca', 40, 42, 43, 44, 46, 48],['Sc', 45],['Ti', 46, 47, 48, 49, 50],['V', 50, 51],
                 ['Cr', 50, 52, 53, 54],['Mn', 55],['Fe', 54, 56, 57, 58],['Co', 59],
                 ['Ni', 58, 60, 61, 62, 64],['Cu', 63, 65],['Zn', 64, 66, 67, 68, 70],['Ga', 69, 71],
                 ['Ge', 70, 72, 73, 74, 76],['As', 75],['Se', 74, 76, 77, 78, 80, 82],['Br', 79, 81],
                 ['Kr', 78, 80, 82, 83, 84, 86],['Rb', 85, 87],['Sr', 84, 86, 87, 88],['Y', 89],
                 ['Zr', 90, 91, 92, 94, 96],['Nb', 93],['Mo', 92, 94, 95, 96, 97, 98, 100],
                 ['Tc',999],['Ru', 96, 98, 99, 100, 101, 102, 104],['Rh', 103],
                 ['Pd', 102, 104, 105, 106, 108, 110],['Ag', 107, 109],
                 ['Cd', 106, 108, 110, 111, 112, 113, 114, 116],['In', 113, 115],
                 ['Sn', 112, 114, 115, 116, 117, 118, 119, 120, 122, 124],['Sb', 121, 123],
                 ['Te', 120, 122, 123, 124, 125, 126, 128, 130],['I', 127],
                 ['Xe', 124, 126, 128, 129, 130, 131, 132, 134, 136],['Cs', 133],
                 ['Ba', 130, 132, 134, 135, 136, 137, 138],['La', 138, 139],['Ce', 136, 138, 140, 142],
                 ['Pr', 141],['Nd', 142, 143, 144, 145, 146, 148, 150],['Pm',999],
                 ['Sm', 144, 147, 148, 149, 150, 152, 154],['Eu', 151, 153],
                 ['Gd', 152, 154, 155, 156, 157, 158, 160],['Tb', 159],
                 ['Dy', 156, 158, 160, 161, 162, 163, 164],['Ho', 165],
                 ['Er', 162, 164, 166, 167, 168, 170],['Tm', 169],['Yb', 168, 170, 171, 172, 173, 174, 176],
                 ['Lu', 175, 176],['Hf', 174, 176, 177, 178, 179, 180],['Ta', 180, 181],
                 ['W', 180, 182, 183, 184, 186],['Re', 185, 187],['Os', 184, 186, 187, 188, 189, 190, 192],
                 ['Ir', 191, 193],['Pt', 190, 192, 194, 195, 196, 198],['Au', 197],
                 ['Hg', 196, 198, 199, 200, 201, 202, 204],['Tl', 203, 205],['Pb', 204, 206, 207, 208],
                 ['Bi', 209],['Th', 232],['U',235,238],['Po',999]]

	self.elements_names=[]
	for k in range(len(self.stable_el)):
		self.elements_names.append(self.stable_el[k][0])

    def abu_chart(self,sens_param_type='reaction',sens_param='C  13(a,n)',
		   mass_range=None ,ilabel=True,
                  imlabel=False, imlabel_fontsize=12, imagic=False,
                  boxstable=True, lbound=(-100,1),
                  plotaxis=[0, 0, 0, 0], show=True, color_map='gist_rainbow_r',
                  ifig=1,data_provided=False,thedata=None,
                  savefig=False,drawfig=None,drawax=None,mov=False):
        ''' 
        Plots an abundance chart

        Parameters
        ----------
        mass_range : list, optional
            A 1x2 array containing the lower and upper mass range.  If
            this is an instance of abu_vector this will only plot
            isotopes that have an atomic mass within this range.  This
            will throw an error if this range does not make sence ie
            [45,2] if None, it will plot over the entire range.  The
            default is None.
        ilabel : boolean, optional
            Elemental labels off/on.  The default is True.
        imlabel : boolean, optional
            Label for isotopic masses off/on.  The default is True.
        imlabel_fontsize : integer, optional
            Fontsize for isotopic mass labels.  The default is 12.
        imagic : boolean, optional
            Turn lines for magic numbers off/on.  The default is False.
        boxstable : boolean, optional
            Plot the black boxes around the stable elements.  The
            defaults is True.
        lbound : tuple, optional
            Boundaries for colour spectrum ploted.  The default is
            (-12,0).
        plotaxis : list, optional
            Set axis limit.  If [0, 0, 0, 0] the complete range in (N,Z)
            will be plotted.  It equates to [xMin, xMax, Ymin, Ymax].
            The default is [0, 0, 0, 0].
        show : boolean, optional
            Boolean of if the plot should be displayed.  Useful with
            saving multiple plots using abu_chartMulti.  The default is
            True.
        color_map : string, optional
            Color map according to choices in matplotlib
            (e.g. www.scipy.org/Cookbook/Matplotlib/Show_colormaps).
            The default is 'jet'.
        ifig : integer, optional
            Figure number, if ifig is None it wiil be set to the cycle
            number.  The defaults is None.
        savefig : boolean, optional
            Whether or not to save the figure.
            The default is False
        drawfig, drawax, mov : optional, not necessary for user to set these variables
            The figure and axes containers to be drawn on, and whether or not a movie is
            being made (only True when se.movie is called, which sets mov to True
            automatically
            
        '''

        if ifig == None and not mov:
            #ifig=cycle

            #self.abu_chartMulti(cycle, mass_range,ilabel,imlabel,imlabel_fontsize,imagic,boxstable,\
                                #lbound,plotaxis,color_map)
            return
        #plotType=self._classTest()

        if mass_range!=None and mass_range[0]>mass_range[1]:
            raise IOError("Please input a proper mass range")


        #elif plotType=='nusensi':
	if True:
                sens_mat=self.sens_mat
                #sens_param_type='reaction' #either isotope or reaction
                #sens_param='C  12(a,g)'


                if  sens_param_type == 'reaction':
                        for i in range(2,len(sens_mat[0])):
                                if sens_param in sens_mat[0][i]:
                                        print 'found rate'
                                        rate_idx=i
                                        break

                        isotopes=[]
			ain=[]
			zin=[]	
			nin=[]
                        for i in range(1,len(sens_mat)):
			    if '*' in sens_mat[i][0]:
				continue #skip isomers
			    if 'g' in sens_mat[i][0].split('-')[1]:
				continue
                            yin1=float(sens_mat[i][rate_idx])
                            #skip sensitivites of 0
                            if yin1 == 0.0:
                                continue
			    a1= int(sens_mat[i][0].split('-')[1])
			    ain.append(a1)
			    ele=sens_mat[i][0].split('-')[0]
			    if sens_mat[i][0] =='N-1':
				ele='Neutron'
				z1=0
			    else:	
			        z1=int(get_z_from_el(ele))
			    zin.append(z1)
			    nin.append(a1-z1)
			#abundance
			yin = []
			ymax=1e-99
			ymin=1e99
                        for i in range(1,len(sens_mat)):
                            if '*' in sens_mat[i][0]:
                                continue #skip isomers
                            if 'g' in sens_mat[i][0].split('-')[1]:
                                continue
			    yin1=float(sens_mat[i][rate_idx])
			    #skip sensitivites of 0
			    if yin1 == 0.0:
				continue
		            yin.append(yin1)		 
			    #if i==1:
			    #	ymax=yin1
			    #	ymin=yin1
			    if True:
				if ymax<yin1:
					ymax=yin1
				if ymin>yin1:
					ymin=yin1
			#no isomeric state for now, but there is *
			isom=len(yin)*[1]
		        if lbound == (0,0):
			    lbound=(ymin,ymax)
	
		elif sens_param_type == 'isotope':
			import re
			#find all available reactions affecting 
			#isotope and plot them color-code	
			#sens_param='C  12'
			#find isotope index
                        for i in range(2,len(sens_mat)):
                                if sens_param in sens_mat[i][0]:
                                        print 'found isotope'
                                        iso_idx=i
                                        break

			#get the list with one sens factor for each rate
			#identify the first isotope of each reaction
			#sens_facs=[]
			#iso=[]	

                        ain=[]
                        zin=[]
                        nin=[]
                        for i in range(2,len(sens_mat[0])):
			    rate=sens_mat[0][i]
			    print 'check rate ',rate
			    iso=rate.split('(')[0]
                            if '*' in iso:
                                continue #skip isomers
                            if 'g' in iso:
                                continue
                            yin1=float(sens_mat[iso_idx][i])
                            if yin1 == 0.0:
				#print 'skip rate due to 0.0'
                                continue
			    iso=iso.replace(' ','')
                            #print 'Iso ','|',iso,'|'
			    match = re.match(r"([a-z]+)([0-9]+)", iso, re.I)
			    a1 = int(match.groups()[1])
			    ele=match.groups()[0].capitalize()
			    print 'choose',ele,a1
                            ain.append(a1)
                            if iso =='N   1':
                                ele='Neutron'
                                z1=0
                            else:
                                z1=int(get_z_from_el(ele))
                            zin.append(z1)
                            nin.append(a1-z1)

			#print 'ain: ',ain
			#print 'zin: ',zin
			#print 
                        #abundance
                        yin = []
                        ymax=1e-99
                        ymin=1e99
                        for i in range(2,len(sens_mat[0])):
                            rate=sens_mat[0][i]
                            #print 'rate ',rate
                            iso=rate.split('(')[0]
                            if '*' in sens_mat[i][0]:
                                continue #skip isomers
                            if 'g' in sens_mat[i][0].split('-')[1]:
                                continue
                            yin1=float(sens_mat[iso_idx][i])
                            #skip sensitivites of 0
                            if yin1 == 0.0:
                                continue
                            yin.append(yin1)
			    #print 'sens',yin
                            #if i==1:
                            #   ymax=yin1
                            #   ymin=yin1
                            if True:
                                if ymax<yin1:
                                        ymax=yin1
                                if ymin>yin1:
                                        ymin=yin1
                        #no isomeric state for now, but there is *
                        isom=len(yin)*[1]
                        if lbound == (0,0):
                            lbound=(ymin,ymax)



	
		else:
			print 'ERror wrong sens_param_type input'
			return

	else:
            raise IOError("This method, abu_chart, is not supported by this class")

        # in case we call from ipython -pylab, turn interactive on at end again
        turnoff=False
        if not show:
            try:
                ioff()
                turnoff=True
            except NameError:
                turnoff=False

        nnmax = int(max(nin))+1
        nzmax = int(max(zin))+1
        nzycheck = zeros([nnmax,nzmax,3])

        for i in range(len(nin)):
            if isom[i]==1:
                ni = int(nin[i])
                zi = int(zin[i])

                nzycheck[ni,zi,0] = 1
                nzycheck[ni,zi,1] = yin[i]

        #######################################################################
        # elemental names: elname(i) is the name of element with Z=i

        elname=self.elements_names

        #### create plot
        ## define axis and plot style (colormap, size, fontsize etc.)
        if plotaxis==[0,0,0,0]:
            xdim=10
            ydim=6
        else:
            dx = plotaxis[1]-plotaxis[0]
            dy = plotaxis[3]-plotaxis[2]
            ydim = 6
            xdim = ydim*dx/dy


        params = {'axes.labelsize':  12,
                  'text.fontsize':   12,
                  'legend.fontsize': 12,
                  'xtick.labelsize': 12,
                  'ytick.labelsize': 12,
                  'text.usetex': True}
        #pl.rcParams.update(params) #May cause Error, someting to do with tex
        if mov:
            fig=drawfig
            fig.set_size_inches(xdim,ydim)
            artists=[]
        else:
            fig=pl.figure(ifig,figsize=(xdim,ydim),dpi=100)
        axx = 0.10
        axy = 0.10
        axw = 0.85
        axh = 0.8
        if mov:
            ax=drawax
        else:
            ax=pl.axes([axx,axy,axw,axh])
        # Tick marks
        xminorlocator = MultipleLocator(1)
        xmajorlocator = MultipleLocator(5)
        ax.xaxis.set_major_locator(xmajorlocator)
        ax.xaxis.set_minor_locator(xminorlocator)
        yminorlocator = MultipleLocator(1)
        ymajorlocator = MultipleLocator(5)
        ax.yaxis.set_major_locator(ymajorlocator)
        ax.yaxis.set_minor_locator(yminorlocator)

        # color map choice for abundances

        cmapa = cm.get_cmap(name=color_map)
        # color map choice for arrows
        cmapr = cm.autumn
        # if a value is below the lower limit its set to white
        cmapa.set_under(color='w')
        cmapr.set_under(color='w')
        # set value range for abundance colors (log10(Y))
        #norma = colors.Normalize(vmin=lbound[0],vmax=lbound[1])
	logthresh=3
	norma= colors.SymLogNorm(vmin=lbound[0],vmax=lbound[1],linthresh=10**-logthresh)
        # set x- and y-axis scale aspect ratio to 1
        ax.set_aspect('equal')
        #print time,temp and density on top
        temp = ' '#'%8.3e' %ff['temp']
        time = ' '#'%8.3e' %ff['time']
        dens = ' '#'%8.3e' %ff['dens']

        #May cause Error, someting to do with tex
        '''
        #box1 = TextArea("t : " + time + " s~~/~~T$_{9}$ : " + temp + "~~/~~$\\rho_{b}$ : " \
        #             + dens + ' g/cm$^{3}$', textprops=dict(color="k"))
        anchored_box = AnchoredOffsetbox(loc=3,
                        child=box1, pad=0.,
                        frameon=False,
                        bbox_to_anchor=(0., 1.02),
                        bbox_transform=ax.transAxes,
                        borderpad=0.,
                        )
        ax.add_artist(anchored_box)
        '''
        ## Colour bar plotted

        patches = []
        color = []
        for i in range(nzmax):
            for j in range(nnmax):
                if nzycheck[j,i,0]==1:
                    xy = j-0.5,i-0.5

                    rect = Rectangle(xy,1,1,)

                    # abundance
                    yab = nzycheck[j,i,1]
                    if yab == 0:

                        yab=1e-99


                    #col =log10(yab)
		    col = yab
                    patches.append(rect)
                    color.append(col)

        p = PatchCollection(patches, cmap=cmapa, norm=norma)
        p.set_array(array(color))
        p.set_zorder(1)
        if mov:
            artist1=ax.add_collection(p)
            artists.append(artist1)
        else:
            ax.add_collection(p)
        if not mov:
		test=True
	        if test:
		   maxlog=int(np.ceil(np.log10(lbound[1])))
		   minlog=int(np.ceil(np.log10(-lbound[0]))) 
		   tick_locations=([-(10**x) for x in xrange(minlog,-logthresh-1,-1)] + [0.0]+ [(10**x) for x in xrange(-logthresh,maxlog+1)])		
		   
		   #tick_locations,labels=makeTickLables(lbound[0],lbound[1],10**-logthresh)
			
		   cb = pl.colorbar(p,ticks=tick_locations)
		   cb.ax.set_yticklabels(tick_locations)
	        else:
                   cb = pl.colorbar(p)

                # colorbar label
                cb.set_label('Sensitivity S$_{i/j}$',fontsize='x-large')

        # plot file name
        graphname = 'abundance-chart'+str(ifig)

        # Add black frames for stable isotopes
        if boxstable:
            for i in xrange(len(self.stable_el)):
                if i == 0:
                    continue


                tmp = self.stable_el[i]
                try:
                    zz= self.elements_names.index(tmp[0]) #charge
                except:
                    continue

                for j in xrange(len(tmp)):
                    if j == 0:
                        continue

                    nn = int(tmp[j]) #atomic mass
                    nn=nn-zz

                    xy = nn-0.5,zz-0.5
                    rect = Rectangle(xy,1,1,ec='k',fc='None',fill='False',lw=3.)
                    rect.set_zorder(2)
                    ax.add_patch(rect)


        # decide which array to take for label positions
        iarr = 0

        # plot element labels
        if ilabel:
            for z in range(nzmax):
                try:
                    nmin = min(argwhere(nzycheck[:,z,iarr]))[0]-1
                    ax.text(nmin,z,elname[z],horizontalalignment='center',verticalalignment='center',\
                            fontsize='x-small',clip_on=True)
                except ValueError:
                    continue

        # plot mass numbers
        if imlabel:
            for z in range(nzmax):
                for n in range(nnmax):
                    a = z+n
                    if nzycheck[n,z,iarr]==1:
                        ax.text(n,z,a,horizontalalignment='center',verticalalignment='center',\
                                fontsize=imlabel_fontsize,clip_on=True)

        # plot lines at magic numbers
        if imagic:
            ixymagic=[2, 8, 20, 28, 50, 82, 126]
            nmagic = len(ixymagic)
            for magic in ixymagic:
                if magic<=nzmax:
                    try:
                        xnmin = min(argwhere(nzycheck[:,magic,iarr]))[0]
                        xnmax = max(argwhere(nzycheck[:,magic,iarr]))[0]
                        line = ax.plot([xnmin,xnmax],[magic,magic],lw=3.,color='r',ls='-')
                    except ValueError:
                        dummy=0
                if magic<=nnmax:
                    try:
                        yzmin = min(argwhere(nzycheck[magic,:,iarr]))[0]
                        yzmax = max(argwhere(nzycheck[magic,:,iarr]))[0]
                        line = ax.plot([magic,magic],[yzmin,yzmax],lw=3.,color='r',ls='-')
                    except ValueError:
                        dummy=0

        # set axis limits
        if plotaxis==[0,0,0,0]:

            xmax=max(nin)
            ymax=max(zin)
            ax.axis([-0.5,xmax+0.5,-0.5,ymax+0.5])
        else:
            ax.axis(plotaxis)

        # set x- and y-axis label
        ax.set_xlabel('neutron number (A-Z)',fontsize=14)
        ax.set_ylabel('proton number Z',fontsize=14)
        if not mov:
            pl.title('Isotopic Chart for '+sens_param)
        if savefig:
            fig.savefig(graphname)
            print graphname,'is done'
        if show:
            pl.show()
        if turnoff:
            ion()

        if mov:
            return p,artists
        else:
            return

def makeTickLables(vmin,vmax,linthresh):
    """
    make two lists, one for the tick positions, and one for the labels
    at those positions. The number and placement of positive labels is 
    different from the negative labels.
    """
    nvpos = int(np.log10(vmax))-int(np.log10(linthresh))
    nvneg = int(np.log10(np.abs(vmin)))-int(np.log10(linthresh))+1
    ticks = []
    labels = []
    lavmin = (np.log10(np.abs(vmin)))
    lvmax = (np.log10(np.abs(vmax)))
    llinthres = int(np.log10(linthresh))
    # f(x) = mx+b
    # f(llinthres) = .5
    # f(lavmin) = 0
    m = .5/float(llinthres-lavmin)
    b = (.5-llinthres*m-lavmin*m)/2
    for itick in range(nvneg):
        labels.append(-1*float(pow(10,itick+llinthres)))
        ticks.append((b+(itick+llinthres)*m))
    # add vmin tick
    labels.append(vmin)
    ticks.append(b+(lavmin)*m)
    # f(x) = mx+b
    # f(llinthres) = .5
    # f(lvmax) = 1
    m = .5/float(lvmax-llinthres)
    b = m*(lvmax-2*llinthres) 
    for itick in range(1,nvpos):
        labels.append(float(pow(10,itick+llinthres)))
        ticks.append((b+(itick+llinthres)*m))
    # add vmax tick
    labels.append(vmax)
    ticks.append(b+(lvmax)*m)

    return ticks,labels

def get_z_from_el(element):
    '''
    Very simple function that gives the atomic number AS A STRING when given the element symbol.
    Uses predefined a dictionnary.
    Parameter :
    element : string
    For the other way, see get_el_from_z
    '''
    dict_name={'Ru': '44', 'Re': '75', 'Ra': '88', 'Rb': '37', 'Rn': '86', 'Rh': '45', 'Be': '4', 'Ba': '56', 'Bi': '83', 'Br': '35', 'H': '1', 'P': '15', 'Os': '76', 'Hg': '80', 'Ge': '32', 'Gd': '64', 'Ga': '31', 'Pr': '59', 'Pt': '78', 'C': '6', 'Pb': '82', 'Pa': '91', 'Pd': '46', 'Cd': '48', 'Po': '84', 'Pm': '61', 'Ho': '67', 'Hf': '72', 'K': '19', 'He': '2', 'Mg': '12', 'Mo': '42', 'Mn': '25', 'O': '8', 'S': '16', 'W': '74', 'Zn': '30', 'Eu': '63', 'Zr': '40', 'Er': '68', 'Ni': '28', 'Na': '11', 'Nb': '41', 'Nd': '60', 'Ne': '10', 'Fr': '87', 'Fe': '26', 'B': '5', 'F': '9', 'Sr': '38', 'N': '7', 'Kr': '36', 'Si': '14', 'Sn': '50', 'Sm': '62', 'V': '23', 'Sc': '21', 'Sb': '51', 'Se': '34', 'Co': '27', 'Cl': '17', 'Ca': '20', 'Ce': '58', 'Xe': '54', 'Lu': '71', 'Cs': '55', 'Cr': '24', 'Cu': '29', 'La': '57', 'Li': '3', 'Tl': '81', 'Tm': '69', 'Th': '90', 'Ti': '22', 'Te': '52', 'Tb': '65', 'Tc': '43', 'Ta': '73', 'Yb': '70', 'Dy': '66', 'I': '53', 'U': '92', 'Y': '39', 'Ac': '89', 'Ag': '47', 'Ir': '77', 'Al': '13', 'As': '33', 'Ar': '18', 'Au': '79', 'At': '85', 'In': '49'}
    return int(dict_name[element])

