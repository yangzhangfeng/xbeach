import warnings
from scipy.io import loadmat
warnings.filterwarnings("ignore")
from mpl_toolkits.basemap import Basemap
import pathlib as pl
import glob
import utm
from PIL import Image
from datetime import datetime,timedelta
from mpl_toolkits.mplot3d import Axes3D
import folium 
import branca
from folium.plugins import MeasureControl
import scipy
import numpy as np

def write_waves(root_dir,h0,Tp,duration,period,mainang=90.0,gammajsp=3.3,s=10.0,fnyq=0.45,timestep=1.0):
	root_dir = pl.Path(root_dir)
	data = []
	y = 0
	data.append('FILELIST'+'\n')
	for i in range(1,int(period/duration)):
		with open(str(root_dir / f'jonswap_{i}.txt'),'w') as fin:
			fin.write('Hm0           = {:.4e}'.format(h0[y])+ '\n' +
					  'fp            = {:.4e}'.format(float(1/Tp[y]))+ '\n' +
					  'mainang       = {:.4e}'.format(mainang) + '\n' +
					  'gammajsp      = {:.4e}'.format(gammajsp) + '\n' +
					  's             = {:.4e}'.format(s) + '\n' +
					  'fnyq          = {:.4e}'.format(fnyq) + '\n')
			data.append(f'    {duration}    {timestep}    jonswap_{i}.txt'+'\n')
		y+=1
	with open(str(root_dir / 'filelist.txt'),'w') as control:
		lines = control.writelines(data)
	return

def write_tide(root_dir,time,front,back):
	root_dir = pl.Path(root_dir)
	file = root_dir / 'tide.txt'
	data = []
	for i in range(0,len(time)):
		if float(front[i])/float(front[i]) != 1:
			if float(front[i-1])/float(front[i-1]) != 1:
				front[i] = 0.5
			else:
				front[i] = front[i-1]
		 #   front[i] = 0
		 #  back[i] = 0
		data.append('    {:.4e}    {:.4e}    {:.4e}'.format(float(time[i]),float(front[i]),float(front[i])) + '\n')
		#data.append('    {:.4e}    {:.4e}    {:.4e}'.format(float(time[i]),float(front[i])*1.5,float(back[i])*1.5) + '\n')
	with open(file,'w') as fin:
		fin.writelines(data)
	return

def write_2delft(path:str,array:np.array,filename:str):
    xx,yy = array.shape
    with open(str(path / filename),'w') as fin:
        for i in range(0,xx):
            for ii in range(0,yy):
                if (ii/12).is_integer() and ii != 0:
                    fin.write('   '+str(array[i,ii]) + '\n')
                else:
                    fin.write('   '+str(array[i,ii]))
    return


