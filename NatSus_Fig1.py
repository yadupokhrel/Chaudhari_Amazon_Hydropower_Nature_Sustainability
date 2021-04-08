#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from pylab import *
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Polygon

r"""
#%%------------------------------------------------------------------
     Description:   NatSus Paper Figure 1

     First Version: 03/18/2020
     last Updated : 03/31/2021

     Developer:	    Suyog Chaudhari

	 Outstanding Issues:
					1-
---------------------------------------------------------------------
#%%
"""
def yy(a):
    return math.trunc(float(float(a + 20.5) / 0.01666666667))

def xx(a):
    return math.trunc(float(float(a + 81.5) / 0.01666666667))

def draw_screen_poly( lats, lons, m):
    x, y = m( lons, lats )
    xy = zip(x,y)
    poly = Polygon( list(xy), edgecolor='k',  facecolor='None',lw=1.2 )
    plt.gca().add_patch(poly)

#%%
#Set Data
IGHP = 'data/Shp_files/IGHP30'
THP = 'data/Shp_files/TIP_40D'
amz_shp='data/Shp_files/Amazon_basin'
continents = 'data/Shp_files/Continents'
ext_dam = 'data/Shp_files/Existing_dams'
pro_dam = 'data/Shp_files/Planned_dams'
und_dam = 'data/Shp_files/Underconstruction_dams'

df=pd.read_excel('Chaudhari_NatSus2021_Fig1_data.xlsx',sheetname='IGHP30')
df1=pd.read_excel('Chaudhari_NatSus2021_Fig1_data.xlsx',sheetname='DamVsInst')
IGHP_subbasin = list(df.IGHP30)

rivers=['japura', 'madeira', 'negro', 'purus', 'solimoes', 'tapajos', 'tocantins', 'xingu']
riv_basin = ['Japura','Madeira','Negro','Purus','Solimoes','Tapajos','Tocantins','Xingu']

#%%
#================================= CREATING CUSTOM COLORBAR ==============================================
import matplotlib as mpl
cmap=plt.cm.get_cmap('gist_earth_r',14)
norm = mpl.colors.BoundaryNorm(list(range(14)), cmap.N)

plot_colors = [mpl.colors.rgb2hex(cmap(j)[:3]) for j in range(cmap.N)]
plot_colors = plot_colors[1:]
bounds = [0,1,10,20,30,100,500,1000,2000,6000,15000]

from matplotlib.colors import LinearSegmentedColormap
cmap = LinearSegmentedColormap.from_list('cm', plot_colors[:12], N=10)
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

#%%
#================================= CREATING BASEMAP ==========================================
fig = plt.figure(figsize=(7,8.2),facecolor='white',edgecolor=None,linewidth=1.0,frameon=True)
##----------------- for basemap
nxa=-81.50
nxb=nxa + 37
nya=-22
nyb=nya + 29
res=0.01666666667
##----------------- for basemap
gs = gridspec.GridSpec(12,2, width_ratios = [4,1])
gs.update(wspace=0.15,hspace=0.5)
fig.subplots_adjust(left=0.04, right=0.96, bottom=0.1, top=0.97 )

#================================= Plot Gross Potential polylines =============================
ax1 = plt.subplot(gs[0:6, 0])
map=Basemap( projection ='cyl',  llcrnrlon  = nxa,  urcrnrlon  = nxb,  llcrnrlat  = nya,  urcrnrlat  =  nyb,  resolution = "i")
map.drawcountries (linewidth=0.1, color='gray');
map.drawparallels(np.arange(-21,10,3.),labels=[1,0,1,0],linewidth=0.1,fontsize=8,dashes=(5,20))
map.drawmeridians(np.arange(-80,46,5.),labels=[1,0,1,0],linewidth=0.1,fontsize=8,dashes=(5,20))
plt.annotate('a', xy=(-47,5),  xycoords='data',fontsize=11, fontweight='bold')

map.readshapefile(continents, 'Continents', drawbounds=True, linewidth=0.5, color='#808B96')
map.readshapefile(amz_shp, 'Amazon_basin', drawbounds=True, linewidth=1., color='#95A5A6')
map.readshapefile(IGHP, 'IGHP', drawbounds=False)
for info, shape in zip(map.IGHP_info, map.IGHP):
    x=[]; y=[]
    if info['GRID_CODE'] <= 1: lwidth = 0.2; cc = plot_colors[0]
    elif info['GRID_CODE'] <= 10 and info['GRID_CODE'] > 1: lwidth = 0.2; cc = plot_colors[1]
    elif info['GRID_CODE'] <= 20 and info['GRID_CODE'] > 10: lwidth = 0.3; cc = plot_colors[2]
    elif info['GRID_CODE'] <= 30 and info['GRID_CODE'] > 20: lwidth = 0.4; cc = plot_colors[3]
    elif info['GRID_CODE'] <= 100 and info['GRID_CODE'] > 30: lwidth = 0.5; cc = plot_colors[4]
    elif info['GRID_CODE'] <= 500 and info['GRID_CODE'] > 100: lwidth = 0.8; cc = plot_colors[5]
    elif info['GRID_CODE'] <= 1000 and info['GRID_CODE'] > 500: lwidth = 1.5; cc = plot_colors[6]
    elif info['GRID_CODE'] <= 2000 and info['GRID_CODE'] > 1000: lwidth = 2.0; cc = plot_colors[7]
    elif info['GRID_CODE'] <= 6000 and info['GRID_CODE'] > 2000: lwidth = 2.5; cc = plot_colors[8]
    elif info['GRID_CODE'] > 6000: lwidth = 3.0; cc = plot_colors[9]

    x.append(info['START_X'])
    x.append(info['END_X'])
    y.append(info['START_Y'])
    y.append(info['END_Y'])
    map.plot(x, y, marker=None,color=cc,linewidth=lwidth,solid_capstyle='round')

#Locate Existing and Underconstruction Dams
map.readshapefile(ext_dam, 'Existing_dams', drawbounds=False)
map.readshapefile(und_dam, 'Underconstruction_dams', drawbounds=False)

for info, dam in zip(map.Existing_dams_info, map.Existing_dams):
    map.plot(dam[0], dam[1], marker='o', markeredgecolor='dodgerblue', fillstyle='none', markersize=9, markeredgewidth=1.2) if float(info['capacity']) > 1000. \
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='dodgerblue', fillstyle='none', markersize=7, markeredgewidth=1.2) if float(info['capacity']) > 300. and float(info['capacity']) <= 1000. \
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='dodgerblue', fillstyle='none', markersize=5, markeredgewidth=1.2) if float(info['capacity']) > 30. and float(info['capacity']) <= 300. \
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='dodgerblue', fillstyle='none', markersize=2, markeredgewidth=0.5)

for info, dam in zip(map.Underconstruction_dams_info, map.Underconstruction_dams):
    map.plot(dam[0], dam[1], marker='o', markeredgecolor='#eda41c', fillstyle='none', markersize=9, markeredgewidth=1.2) if float(info['capacity']) > 1000. \
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='#eda41c', fillstyle='none', markersize=7, markeredgewidth=1.2) if float(info['capacity']) > 300. and float(info['capacity']) <= 1000.\
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='#eda41c', fillstyle='none', markersize=5, markeredgewidth=1.2) if float(info['capacity']) > 30. and float(info['capacity']) <= 300. \
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='#eda41c', fillstyle='none', markersize=3, markeredgewidth=0.5)
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#================================= GHP side plots ===============================================
ax2 = plt.subplot(gs[:3, 1])
y_pos = np.arange(len(riv_basin))
ax2.bar(y_pos,IGHP_subbasin, align='center',color=('#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f','#e5c494','#b3b3b3'))
ax2.set_yticks(np.arange(0,1100,200))
ax2.set_yticklabels(np.arange(0,1100,200),fontsize=10)
ax2.set_ylim(0,1100)
ax2.set_xticks(y_pos)
ax2.set_xticklabels([])
plt.gca().yaxis.grid(True,'both',linestyle='--',lw=0.8)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
ax2.text(8.5, 525, r'IGHP$_{30}$', rotation=90, verticalalignment='center', fontsize=11, fontweight='bold')
ax2.text(-0.5, 1010, 'TWh $yr^{-1}$', horizontalalignment='left', fontsize=10)
ax2.text(6.5, 1010, 'b', horizontalalignment='left', fontsize=11, fontweight='bold')
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#================================= Planned_vs_Instream side plot ==================================
ax6 = plt.subplot(gs[3:, 1])
map.readshapefile(pro_dam, 'Planned_dams', drawbounds=False)
set_colors=['#66c2a5','#fc8d62','#8da0cb','#e78ac3','#a6d854','#ffd92f','#e5c494','#b3b3b3']
cap = list(df1.Capacity)
X = list(df1.Basin_num)
Inst_cap=list(df1.Instream_cap)

for ii in range(len(cap)):
    ax6.scatter(X[ii],cap[ii], s=30,marker='o',facecolors='none', edgecolors=set_colors[X[ii]],linewidths=2)
    ax6.scatter(X[ii],Inst_cap[ii], s=80,marker='s',facecolors='none', edgecolors=set_colors[X[ii]],linewidths=2, zorder=0)
ax6.set_xticks(range(len(riv_basin)))
ax6.set_xticklabels([])
plt.gca().yaxis.grid(True,'major',linestyle='--',lw=0.8)
ax6.set_ylim(1,10000)
ax6.set_yscale('log')
ax6.set_xticks(y_pos)
ax6.set_xticklabels(riv_basin, fontsize=10,rotation=90)
ax6.spines['top'].set_visible(False)
ax6.spines['right'].set_visible(False)
ax6.text(8.5,100, 'Planned Dam Capacity vs In-stream Capacity', rotation=90, verticalalignment='center', fontsize=11, fontweight='bold')
ax6.text(-0.5,8100, 'MW', horizontalalignment='left', fontsize=10)
ax6.text(6.5, 8100, 'd', horizontalalignment='left', fontsize=11, fontweight='bold')
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#================================= Plot Technical Potential polylines ============================
ax4 = plt.subplot(gs[6:, 0])
map=Basemap( projection ='cyl',  llcrnrlon  = nxa,  urcrnrlon  = nxb,  llcrnrlat  = nya,  urcrnrlat  =  nyb,  resolution = "i")
map.drawcountries (linewidth=0.1, color='gray');
map.drawparallels(np.arange(-21,10,3.),labels=[1,0,0,0],linewidth=0.1,fontsize=8,dashes=(5,20))
map.drawmeridians(np.arange(-80,46,5.),labels=[1,0,0,0],linewidth=0.1,fontsize=8,dashes=(5,20))
plt.annotate('c', xy=(-47,5),  xycoords='data',fontsize=11, fontweight='bold')

map.readshapefile(continents, 'Continents', drawbounds=True, linewidth=0.5, color='#808B96')
map.readshapefile(amz_shp, 'Amazon_basin', drawbounds=True, linewidth=1., color='#95A5A6')
map.readshapefile(THP, 'THP', drawbounds=False)
for info, shape in zip(map.THP_info, map.THP):
    x=[]; y=[]
    if info['GRID_CODE']/1000 <= 1: lwidth = 0.2; cc = plot_colors[0]
    elif info['GRID_CODE']/1000 <= 10 and info['GRID_CODE']/1000 > 1:      lwidth = 0.2; cc = plot_colors[1]
    elif info['GRID_CODE']/1000 <= 20 and info['GRID_CODE']/1000 > 10:     lwidth = 0.3; cc = plot_colors[2]
    elif info['GRID_CODE']/1000 <= 30 and info['GRID_CODE']/1000 > 20:     lwidth = 0.4; cc = plot_colors[3]
    elif info['GRID_CODE']/1000 <= 100 and info['GRID_CODE']/1000 > 30:    lwidth = 0.5; cc = plot_colors[4]
    elif info['GRID_CODE']/1000 <= 500 and info['GRID_CODE']/1000 > 100:   lwidth = 0.8; cc = plot_colors[5]
    elif info['GRID_CODE']/1000 <= 1000 and info['GRID_CODE']/1000 > 500:  lwidth = 1.5; cc = plot_colors[6]
    elif info['GRID_CODE']/1000 <= 2000 and info['GRID_CODE']/1000 > 1000: lwidth = 2.0; cc = plot_colors[7]
    elif info['GRID_CODE']/1000 <= 6000 and info['GRID_CODE']/1000 > 2000: lwidth = 2.5; cc = plot_colors[8]
    elif info['GRID_CODE']/1000 > 6000: lwidth = 3.0; cc = plot_colors[9]
    else: lwidth = 3.0; cc = plot_colors[9]

    x.append(info['START_X'])
    x.append(info['END_X'])
    y.append(info['START_Y'])
    y.append(info['END_Y'])
    map.plot(x, y, marker=None,color=cc,linewidth=lwidth,solid_capstyle='round')

#Locate Planned Dams
map.readshapefile(pro_dam, 'Planned_dams', drawbounds=False)
for info, dam in zip(map.Planned_dams_info, map.Planned_dams):
    map.plot(dam[0], dam[1], marker='o', markeredgecolor='purple', fillstyle='none', markersize=9, markeredgewidth=1.2) if float(info['Capacity_1']) > 1000 \
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='purple', fillstyle='none', markersize=7, markeredgewidth=1.2) if float(info['Capacity_1']) > 300. and float(info['Capacity_1']) <= 1000 \
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='purple', fillstyle='none', markersize=5, markeredgewidth=1.2) if float(info['Capacity_1']) > 30. and float(info['Capacity_1']) <= 300 \
    else map.plot(dam[0], dam[1], marker='o', markeredgecolor='purple', fillstyle='none', markersize=3, markeredgewidth=0.5)

rec_lats = [[ 0, 4, 4, 0],[ -11, -6.5, -6.5, -11 ],[ -5, -1, -1, -5 ],    [ -14.5, 2, 2, -14.5 ]]
rec_lons = [[ -63.5, -63.5, -60, -60 ],  [ -63, -63, -59, -59 ],  [ -68, -68, -63, -63 ],[ -80, -80, -72.5, -72.5 ]]
for i in range(len(rec_lats)):
    draw_screen_poly( rec_lats[i], rec_lons[i], map )
    ax4.text(rec_lons[i][1]+0.2,rec_lats[i][1]+0.2, str(i+1),fontsize=10, fontweight='bold')


##============================ Adding Scatter Legend ==================================================================
from matplotlib.lines import Line2D
legend_elements = [Line2D([0], [0], color='w',marker='o', label='Existing', markeredgecolor='dodgerblue', fillstyle='none', markersize=9, markeredgewidth=1.2),
                   Line2D([0], [0], color='w',marker='o', label='Under construction', markeredgecolor='#eda41c', fillstyle='none', markersize=9, markeredgewidth=1.2),
                   Line2D([0], [0], color='w',marker='o', label='Planned', markeredgecolor='purple', fillstyle='none', markersize=9, markeredgewidth=1.2)]
legend1=plt.legend(handles=legend_elements, bbox_to_anchor=(0.3, 0.0), loc=1,ncol=1, borderpad=0.1, labelspacing=0.5,fontsize=10,handletextpad=0.1)

#Dam Capacity legend
legend_elements1 = [Line2D([0], [0], color='w',marker='o', label='>1000 MW', markeredgecolor='k', fillstyle='none', markersize=9, markeredgewidth=1.2),
                   Line2D([0], [0], color='w',marker='o', label='300-1000 MW', markeredgecolor='k', fillstyle='none', markersize=7, markeredgewidth=1.2),
                   Line2D([0], [0], color='w',marker='o', label='30-300 MW', markeredgecolor='k', fillstyle='none', markersize=5, markeredgewidth=1.2),
                   Line2D([0], [0], color='w',marker='o', label='<30 MW', markeredgecolor='k', fillstyle='none', markersize=3, markeredgewidth=0.5)]
plt.legend(handles=legend_elements1, bbox_to_anchor=(0.305, 0.25), loc=1,ncol=1, borderpad=0.3,fontsize=9.5,handletextpad=0.1)
plt.gca().add_artist(legend1)

##======================== Create Second Axes For Colorbar ============================================================
cbw=.015; cbl=.47
cax = fig.add_axes([0.26, 0.06, cbl, cbw])
cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, norm=norm, spacing='uniform', orientation='horizontal', ticks=bounds, boundaries=bounds,extend='both')#, format='%0.2f')
cb.ax.invert_yaxis()
[t.set_fontsize(9.5) and t.set_rotation(0) for t in cb.ax.get_xticklabels()]
fig.text(0.45, 0.015,'GWh/year',fontsize=10, verticalalignment='center',fontweight='bold') #Axis label

fig.savefig('Figure_1.png', dpi=300)