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

def write_spatial_vege(path:str,bathy_file:str,fname:str='vege_map.txt'):
	path = pl.Path(path)
	with open(str(path / bathy_file),'r+') as fin:
		with open(str(path / fname),'w+') as fout:
			lines = fin.readlines()
			new_line,temp,ii = 0,0,0
			for line in lines:
				temp += 1
				data = line.strip().split('  ')

				if (temp/28).is_integer():
					ii = 0
					new_line += 1

				for i in range(0,len(data)):
					vege = []
					new = []
					if data != '':            
						if 81 < new_line < 134 and 87 < ii < 132 and 0.05<float(data[i]) < 0.6:
							fout.write('   '+str(2))
						elif 0.05 < float(data[i]) < 0.55:
							fout.write('   '+str(1))
						elif float(data[i]) > 0.75:
							fout.write('   '+str(3))
						else:
							fout.write('   '+str(0))
						ii += 1

				fout.write('\n')
	return


