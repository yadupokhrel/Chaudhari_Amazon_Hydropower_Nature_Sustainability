#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import division # force division to be floating point in Python
from numpy import *
from pylab import *
import matplotlib.pyplot as plt
from math import pi

r"""
#%%------------------------------------------------------------------
     Description:   NatSus Paper Figure 3

     First Version: 03/18/2020
     last Updated : 03/31/2021

     Developer:	    Suyog Chaudhari

	 Outstanding Issues:
					1-
---------------------------------------------------------------------
#%%
"""
# Set data
df =  [['Bem-Querer','Castaheira', 'Jatoba','Tabajara','Prainha','Sumaúma','Inferninho','Quebra Remo','Marabá'],
       [0.055,0.0692,0.0620,0.0532,0.0477,0.0462,0.1194,0.0506,0.0632]] #bluebars - estimated costs
inst_cost=[0.0381,0.0444] #range of in-stream turbine cost

low=array( [0.001,0.0649,0.0649,0.0659,0.0659,0.0659,0.0659,0.0659,0.0729]) #pink dots - average estimated of exsiting dams
high=array([0.001,0.0842,0.0842,0.1159,0.1159,0.1159,0.1159,0.1159,0.0742]) #red dots - average reported of exsiting dams

avg_dam_cost=0.0824
colors = ['#8da0cb','#ffd92f','#ffd92f','#fc8d62','#fc8d62','#fc8d62','#fc8d62','#fc8d62','#e5c494','#e5c494']

# Set data
categories=list(df[0])
N = len(categories)

values=df[1]
values += values[:1]
#values =array(values)
angles = [((n / float(N)) * 2 * pi) for n in range(N)]
angles += angles[:1]
angles1 = array([n+(angles[1]/2) for n in angles])


# Initialise the figure
fig = plt.figure(figsize=(8, 4))
fig.subplots_adjust(left=0.3,right=0.7,top=0.7,bottom=0.3)
ax = fig.add_subplot(111, polar=True)

plt.xticks(angles[:-1], [], color='black', size=1)
ax.tick_params(axis='x', which='major', pad=15)

# Draw ylabels
min_r = 0.001; max_r = 0.14
labels=arange(0.01,0.21,0.01)
ax.set_rticks(labels)
ax.set_yticklabels([],fontweight='bold')
ax.set_rlim(0, max_r - min_r)

plt.gca().yaxis.grid(True,'major',lw=0.5,color='w',ls='dashed')
plt.gca().xaxis.grid(True,'major',lw=0.5,color='w',ls='dashed')

# Plot data
ax.bar(angles1, array([1]*len(angles1)), bottom=0.001,linewidth=0.1, linestyle='solid',color='#d8d8d8',edgecolor ='r',width=2*pi/N,zorder=0,alpha=0.8)
ax.bar(angles1[:-1], values[:-1],bottom=0.001, linewidth=1, linestyle='solid',color='#d8b365',width=2*pi/N,alpha=0.5)

da=360 #angle steps
angles2 = np.linspace(0,360,da)*np.pi/180
ax.plot(angles2, 0*angles2 + inst_cost[0], color = '#1b9e77', linewidth = 1.6,ls='--')
ax.plot(angles2, 0*angles2 + inst_cost[1], color = '#1b9e77', linewidth = 1.6,ls='--')
ax.plot(angles2, 0*angles2 + avg_dam_cost, color = '#d95f02', linewidth = 1.6,ls='--')

ax.text(angles2[110],0.042,'0.044',color='#1b9e77',rotation=14,ha='center',va='bottom')
ax.text(angles2[60],0.019,'0.038',color='#1b9e77',rotation=-18,ha='center',va='bottom')
ax.text(angles2[140],0.080,'0.082',color='#d95f02',rotation=45,ha='center',va='bottom')


for i in range(1,len(low)):
    ax.scatter(angles1[i],low[i],s=30,color='#f2be96',edgecolor='k',lw=0.6,alpha=0.8,zorder=5)
    ax.scatter(angles1[i],high[i],s=30,color='#d95f02',edgecolor='k',lw=0.6,alpha=0.8,zorder=5)

#Radial grids
ax.plot(angles2, 0*angles2 + 0.01, color = '#909090', linewidth = 1.,ls='--')
ax.plot(angles2, 0*angles2 + 0.1, color = '#909090', linewidth = 1.,ls='--')
ax.text(angles2[0],0.01,'0.01',color='#909090',va='center',rotation=90)
ax.text(angles2[0],0.102,'0.1',color='#909090',va='center',rotation =90)

#Pie plot
fig.add_axes([0.3, 0.1, 0.4,0.8])
plt.pie([1]*N, radius=1.75, colors=colors, wedgeprops=dict(width=0.35,ec='w'),startangle=0)

fig.add_axes([0.3, 0.087, 0.4,0.8],frameon=False)
plt.axis('off')
xx=[1.07,0.80,0.38,0.03,-0.11,0.01, 0.40, 0.82,1.08]
yy=[0.73,1.05,1.12,0.91, 0.53,0.12,-0.10,-0.02,0.29]
names=['Bem-Querer','Castanheira', 'Jatoba','Tabajara','Prainha','Sumaúma','Inferninho','Quebra Remo','Marabá']
rot = [-68,-30,11,52,90,-53,-10,30,68]
for i in range(9):
    plt.text(xx[i],yy[i],names[i],fontsize=11,va='center',ha='center',rotation=rot[i])

plt.tight_layout()
savefig('Figure_3.png', dpi=400, bbox_inches='tight')
