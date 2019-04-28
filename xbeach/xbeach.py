import numpy as np
import matplotlib.pyplot as plt
import netCDF4 as nc4
import os
from utils import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.figure_factory as ff
#from IPython.display import HTML
import plotly.graph_objs as go
import plotly.offline as po
import pandas as pd
import warnings
from scipy.io import loadmat
warnings.filterwarnings("ignore")
from mpl_toolkits.basemap import Basemap
import pathlib as pl
import glob
import utm
from PIL import Image


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

def utm2geo(x,y,code:int=18,zone:str='northern'):
    limits = x.shape
    x2,y2 = np.array(np.zeros(x.shape)),np.ma.array(np.zeros(y.shape))
    for i in range(0,limits[0]):
        for ii in range(0,limits[1]):
            coord = utm.to_latlon(x[i,ii],y[i,ii],code,zone)
            x2[i,ii] = coord[1] 
            y2[i,ii] = coord[0]
    return x2,y2

def map_plot(x,y,z,data,time,title,levels,lat1:float,lat2:float,lon1:float,lon2:float,label:str='elevation(m)',figsize=(18,10),cmap='jet',save='xbeach.gif'):
  wl=[]
  data[data.mask]=np.nan
  for i in range(0,len(time)):
    file_number = '%05d'%i
    fig,ax = plt.subplots(figsize=figsize)
    data[data <=z+0.00001] = np.nan
    wl.append('WL{}.png'.format(file_number))
    plt.contourf(x,y,data[i,:,:],levels=levels,cmap=cmap,shading='gouraud',vmin=np.min(levels),vmax=np.max(levels),aspect='auto')
    m = Basemap(projection='cyl',llcrnrlat=lat1,urcrnrlat=lat2,llcrnrlon=lon1,
                        urcrnrlon=lon2,resolution='h', epsg = 4269)
    m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 600, verbose= False)
    cb = plt.colorbar(cmap=cmap,fraction=0.026,pad=0.04) 
    cb.set_label(label,fontsize=10)
    ax.autoscale_view(tight=True)
    plt.title(title + str(i))
    plt.savefig('WL{}.png'.format(file_number),dpi=400,bbox_inches = 'tight', pad_inches = 0.1)
    plt.close()
    images = []
  for ii in range(0,len(wl)):
      frames = Image.open(wl[ii])
      images.append(frames)
  images[0].save(save,
     save_all=True,
     append_images=images[1:],
     delay=.1,
     duration=300,
     loop=0)
  for f in glob.glob('WL*'):
      os.remove(f) 



  return





'''
frames = []
x = xb.variables['globalx'][:,:][0]
data = [dict(x=x, y=x*0+-5,
           name='topo',mode='lines',legendgroup='b',line=dict(width=2, color='white')),
        dict(x=x, y=xb.variables['H_mean'][0,:][0]+xb.variables['zs_mean'][0,:][0],
           name='waves',mode='lines',legendgroup='b',line=dict(width=2, color='#3399ff')),
       dict(x=x, y=xb.variables['zs_mean'][0,:][0],
           name='water depth',mode='lines',legendgroup='a',line=dict(width=2, color='blue')),
       dict(x=x, y=xb.variables['zb_mean'][0,:][0],
           name='topo/bathy',mode='lines',line=dict(width=2, color='grey'),
           fill='tonexty',fillcolor='blue'),
       ]
            #fill='tozeroy',fillcolor='#737373'),
       # dict(x=x, y=xb.variables['zb_mean'][0,:][0],
       #    mode='lines',legendgroup='a',showlegend= False,line=dict(width=2, color='#737373'),
       #     fill='tonexty',fillcolor='blue')]#,
        #dict(x=x, y=xb.variables['zs_mean'][0,:][0],
        #   name=None,mode='lines',legendgroup='b',showlegend= False,line=dict(width=2, color=None),
        #    fill='tonexty',fillcolor='cyan')]

    
frames=[dict(data=[dict(x=x, y=xb.variables['H_mean'][k,:][0]+xb.variables['zs_mean'][k,:][0], 
                        mode='lines',line=dict(color='#3399ff', width=2),),
                   dict(x=x, y=xb.variables['zs_mean'][k,:][0], 
                        mode='lines',line=dict(color='blue', width=2)),
                   dict(x=x, y=xb.variables['zb_mean'][k,:][0], 
                        mode='lines',line=dict(color='grey', width=2),
                        fill='tonexty',fillcolor='blue'),
                    dict(x=x, y=x*0+-3, 
                        mode='lines',line=dict(color='white', width=2),
                        fill='tonexty',fillcolor='grey')
                  # dict(x=x, y=xb.variables['zb_mean'][k,:][0],
                  #      mode='lines',legendgroup='a',showlegend= False,line=dict(color='blue', width=2)),
                  #  dict(x=x, y=xb.variables['zs_mean'][k,:][0],name=None,mode='lines',
                  #       legendgroup='b',showlegend= False,line=dict(width=2, color=None))
                  ]) for k in range(0,len(t))]    

sliders=[dict(steps=[dict(method='animate',args= [
                    dict(mode='immediate',frame= dict(duration=len(t), redraw= False),
                    transition=dict(duration=len(t),steps= []))],
                    label='{:d}'.format(k+1)) for k in range(len(t))],
                    transition= dict(duration=len(t)),x=0.01,y=0, 
        currentvalue=dict(font=dict(size=12), 
                          prefix='Time step: ', visible=True, 
                          xanchor='center'),len=1.0)]
layout=dict(width=1100, height=500,
            xaxis=dict(range=[0, 104],zeroline=False,showline=False),yaxis=dict(range=[-.5, 4]),
              title='XBeach', hovermode='closest',
            updatemenus= [{'type': 'buttons','buttons': [{'label': 'Play',
                        'method': 'animate','args': [None, {'frame': {'duration': 1000, 'redraw': False},
                         'fromcurrent': True, 'transition': {'duration': 100, 'easing': 'quadratic-in-out'}}]},
                        {'label': 'Pause','method': 'animate','args': [[None], {'frame': {'duration': 0, 'redraw': False},
                        'mode': 'immediate','transition': {'duration': 0}}]}],'direction': 'left','pad': {'r': 10, 't': 87},
                        'showactive': False,'type': 'buttons','x': 0.1,'xanchor': 'right','y': -0.05,'yanchor': 'top'}],sliders=sliders)  

figure=dict(data=data,layout=layout, frames=frames)          
po.plot(figure,'xbeach_animation.html')
iplot(figure)
'''


