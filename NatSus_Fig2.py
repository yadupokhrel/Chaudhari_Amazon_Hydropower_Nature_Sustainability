#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from numpy import *
from pylab import *
import pandas as pd
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap,shiftgrid
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
from matplotlib import colors
import seaborn as sns

r"""
#%%------------------------------------------------------------------
     Description:   NatSus Paper Figure 2

     First Version: 03/18/2020
     last Updated : 03/31/2021

     Developer:	    Suyog Chaudhari

	 Outstanding Issues:
					1-
---------------------------------------------------------------------
#%%
"""
def hex_to_rgb_color(hex):
    return sRGBColor(*[int(hex[i + 1:i + 3], 16) for i in (0, 2 ,4)], is_upscaled=True)

def find_nearest(X, value):
    ii=unravel_index(np.argmin(np.abs(X - value)), X.shape)[0]
    return ii

def draw_screen_poly( lats, lons, m,l):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( list(xy), edgecolor='k',  facecolor='None',lw=l,zorder=10 )
    plt.gca().add_patch(poly)

#%%
#Set data
amz_shp='data/Shp_files/Amazon_basin'
continents = 'data/Shp_files/Continents'
ext_dam = 'data/Shp_files/Existing_dams'
pro_dam = 'data/Shp_files/Planned_dams'
und_dam = 'data/Shp_files/Underconstruction_dams'
ISI = 'data/Shp_files/Brazil_Instream_indices'
PAS= 'data/Shp_files/Protected_Areas'
cities = [[-48.48,-1.594],[-59.99,-3.117],[-55.99,-4.67],[-55.12,-11.41],[-57.78,-6.14],[-61.93,-10.87],[-60.12,-12.68],[-63.9,-8.76],[-61.13,1.81]]
cities_names = ['Belem','Manaus','Itaituba','Sinop','Jacareacanga','Ji-Paraná','Vilhena','Porto Velho','Caracaraí']

#%%
#================================= CREATING CUSTOM TRI-VARIATE COLORBAR ==============================================
import colormath
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from colormath.color_objects import sRGBColor, HSVColor, LabColor, LCHuvColor, XYZColor, LCHabColor
from colormath.color_conversions import convert_color

def plot_color_palette(colors, subplot, title, plt_count):
    ax = fig.add_subplot(plt_count, 1, subplot)
    for sp in ax.spines: ax.spines[sp].set_visible(False)
    for x, color in enumerate(colors):
        ax.add_patch(mpl.patches.Rectangle((x, 0), 0.95, 1, facecolor=color))
    ax.set_xlim((0, len(colors)))
    plt.title(title)

def create_palette(start_rgb, end_rgb, n, colorspace):
    start = convert_color(start_rgb, colorspace).get_value_tuple()
    end = convert_color(end_rgb, colorspace).get_value_tuple()
    points = list(zip(*[np.linspace(start[i], end[i], n) for i in range(3)]))
    rgb_colors = [convert_color(colorspace(*point), sRGBColor) for point in points]
    return [color.get_rgb_hex() for color in rgb_colors]

#------------- CREATING START AND END COLOR OF EACH LINE-----------------------
start_color = ['#cc6c35','#cc6c35','#e3986d','#c59810','#c59810','#c5ad10','#f2cb30','#f0de13','#f0de13','#f0dd0e']
end_color = ['#3ea8cc','#3ea8cc','#10c2c5','#10c592','#1fb551','#a9de4e','#dcf230','#ecf013','#ecf013','#f0dd0e']
colorspaces = (sRGBColor, HSVColor, LabColor, LCHuvColor, LCHabColor, XYZColor)
colorspaces_selected=[LabColor,XYZColor,XYZColor,LCHuvColor,LabColor,HSVColor,HSVColor,LCHuvColor,LabColor,HSVColor]
bounds=zeros((len(start_color),100))
plot_colors=np.chararray((len(start_color),255), itemsize=7,unicode=True)

#------- DISPLAY THE CUSTOM 2D COLORBAR
fig = plt.figure(figsize=(3, 3), frameon=False)
ax=plt.subplot(111)
number_of_colors=10
cx=0.0; cy=0;cxl=1;cxe=1

for i in range(len(start_color)):
    start_rgb = hex_to_rgb_color(start_color[i]); end_rgb = hex_to_rgb_color(end_color[i])
    for index, colorspace in enumerate(colorspaces):
        palette = create_palette(start_rgb, end_rgb, 255, colorspace)
        if index==colorspaces.index(colorspaces_selected[i]): plot_colors[i,:]=palette[:]
    cax = fig.add_axes([cx, cy, cxl, 0.1])
    cb = mpl.colorbar.ColorbarBase(cax, cmap=colors.ListedColormap(plot_colors[i,:]), spacing='uniform', orientation='horizontal',extend='both',extendfrac=0.1)
    cb.outline.set_visible(False)
    cb.set_ticks([])
    bounds[i]=linspace(cx,cxe,100)
    cx+=0.05; cy+=0.1; cxl-=0.1;cxe-=0.05

#%%
def color_coord(side,EDI,IPI,PAI):
    H=0.866
    #Vertices
    xe=0; ye=0      #EDI
    xi=1; yi=0      #IPI
    xp=0.5; yp=H    #PAI

    #EDI co-ordinate
    xe_i=0.75;ye_i=H/2 #midpoint of the opposite side
    X_EDI=(EDI*xe + (1-EDI)*xe_i);  Y_EDI = (EDI*ye + (1-EDI)*ye_i)

    #IPI co-ordinate
    xi_i=0.25;yi_i=H/2 #midpoint of the opposite side
    X_IPI=(IPI*xi + (1-IPI)*xi_i);  Y_IPI = (IPI*yi + (1-IPI)*yi_i)

    #PAI co-ordinate
    xp_i=0.5;yp_i=0 #midpoint of the opposite side
    X_PAI=(PAI*xp + (1-PAI)*xp_i);  Y_PAI = (PAI*yp + (1-PAI)*yp_i)

    return (X_EDI+X_IPI+X_PAI)/3, (Y_EDI+Y_IPI+Y_PAI)/3

#%%
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
#================================= CREATING BASEMAP =================================
fig = plt.figure(figsize=(7,5.3),facecolor='white',edgecolor=None,linewidth=1.0,frameon=True)
##----------------- for basemap
nxa=-81.5
nxb=nxa + 37
nya=-22
nyb=nya + 29
res=0.01666666667
##----------------- for basemap
fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.97 )
indices =['ISI','PAI','EDI','IPI']

ax = plt.subplot(111)
map=Basemap( projection ='cyl',  llcrnrlon  = nxa,  urcrnrlon  = nxb,  llcrnrlat  = nya,  urcrnrlat  =  nyb,  resolution = "i")

map.drawparallels(arange(-21,10,5.),labels=[1,1,0,0],linewidth=0.1,fontsize=7,color='grey',dashes=(5,20))
map.drawmeridians(arange(-79,46,8.),labels=[1,1,1,0],linewidth=0.1,fontsize=7,color='grey',dashes=(5,20))
map.readshapefile(continents, 'Continents', drawbounds=True, linewidth=0.5, color='#808B96')
map.readshapefile(amz_shp, 'Amazon_basin', drawbounds=True, linewidth=1., color='#95A5A6')
map.readshapefile(ISI, 'ISI', drawbounds=False)
for info, shape in zip(map.ISI_info, map.ISI):
    EDI=info['EDI']; IPI=info['IPI']; PAI=info['PAI']
    XX,YY=color_coord(1,EDI,IPI,PAI)
    cmap_index  = find_nearest(linspace(0,0.866,9),YY)
    color_index = find_nearest(bounds[cmap_index],XX)
    cmap=colors.ListedColormap(plot_colors[cmap_index,:])
    norm=mpl.colors.BoundaryNorm(bounds[cmap_index], cmap.N)
    color=cmap(norm(XX))
    patches=[]; patches.append( Polygon(np.array(shape), True) )
    ax.add_collection(PatchCollection(patches, facecolor= color, edgecolor='white', zorder=1,lw=0.3))


#------------------------------ INSERT PLANNED DAMS ------------------------------
map.readshapefile(pro_dam, 'Planned_dams', drawbounds=False)
for info, dam in zip(map.Planned_dams_info, map.Planned_dams):
    map.plot(dam[0], dam[1], marker='o', markeredgecolor='purple', fillstyle='none', markersize=9, markeredgewidth=0.8) if float(info['Capacity_1']) > 1000 \
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='purple', fillstyle='none', markersize=7, markeredgewidth=0.8) if float(info['Capacity_1']) > 300. and float(info['Capacity_1']) <= 1000 \
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='purple', fillstyle='none', markersize=5, markeredgewidth=0.8) if float(info['Capacity_1']) > 30. and float(info['Capacity_1']) <= 300 \
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='purple', fillstyle='none', markersize=3, markeredgewidth=0.5)
from matplotlib.lines import Line2D
legend_elements1 = [Line2D([0], [0], color='w',marker='o', label='>1000 MW', markeredgecolor='purple', fillstyle='none', markersize=9, markeredgewidth=0.8),
                    Line2D([0], [0], color='w',marker='o', label='300-1000 MW', markeredgecolor='purple', fillstyle='none', markersize=7, markeredgewidth=0.8),
                    Line2D([0], [0], color='w',marker='o', label='30-300 MW', markeredgecolor='purple', fillstyle='none', markersize=5, markeredgewidth=0.8),
                    Line2D([0], [0], color='w',marker='o', label='<30 MW', markeredgecolor='purple', fillstyle='none', markersize=3, markeredgewidth=0.8)]
plt.legend(handles=legend_elements1, bbox_to_anchor=(0.59, 0.00), loc=3,ncol=2, borderpad=0.5,fontsize=10,handletextpad=0.1,columnspacing=0.1)


#------------------------------ INSERT PROTECTED AREAS ------------------------------
map.readshapefile(PAS, 'All_together_protected_areas_merged_new1', drawbounds=False)
shapes = {}
mpl.rcParams['hatch.linewidth'] = 0.1
for info, shape in zip(map.All_together_protected_areas_merged_new1_info, map.All_together_protected_areas_merged_new1):
    ax.add_patch(Polygon(np.array(shape), fill=False, color='#A04000', hatch="/"*5, lw=0.1))##A04000
    #ax.add_patch(Polygon(np.array(shape), fill=False, ec='#CD6155',lw=0.1))
mpl.rcParams['hatch.linewidth'] = 0.3
plt.annotate('PAI', xy=(-74, -18),  xycoords='data', xytext=(-76.2,-14.6), textcoords='data',va='center',fontweight='bold',fontsize=11)
plt.annotate('EDI', xy=(-74, -18),  xycoords='data', xytext=(-81.3,-21.3), textcoords='data',va='center',fontweight='bold',fontsize=11)
plt.annotate('IPI', xy=(-74, -18),  xycoords='data', xytext=(-71,-21.3), textcoords='data',va='center',fontweight='bold',fontsize=11)

#------------------------------ INSERT CITIES ----------------------------------------
for jj in range(len(cities)):
    x,y = map([cities[jj][0]],[cities[jj][1]])
    map.plot(x,y,marker="o",markersize=1.5, color="k", label=cities_names[jj], ls="")
    if jj==2 or jj==7 or jj==8:
        plt.annotate(cities_names[jj], xy=(cities[jj][0]-0.2,cities[jj][1]+0.2),  xycoords='data',fontsize=8,ha='right')
    else:
        plt.annotate(cities_names[jj], xy=(cities[jj][0]+0.2,cities[jj][1]+0.2),  xycoords='data',fontsize=8)

#------------------------------ INSERT CUSTOM COLOR BAR ------------------------------
cx=0.095; cy=0.04;cxl=0.2
cxl_step=cxl/10
cx_step=cxl/20
cy_step=cxl_step
width=cxl/10

for i in range(len(start_color)):
    cax = fig.add_axes([cx, cy, cxl, width])
    cb = mpl.colorbar.ColorbarBase(cax, cmap=colors.ListedColormap(plot_colors[i,:]), spacing='uniform', orientation='horizontal')
    #cb.outline.set_visible(False)
    cb.set_ticks([])
    cx+=cx_step; cy+=cy_step; cxl-=cxl_step

savefig('Figure_2.png',dpi=300)
