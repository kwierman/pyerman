

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import math
import datetime

from tableau_color import getTableauColorasRGB
from root_interface import getErrorBarPlot



config_list=[{'run':23393,'dipole':3,'mode':0},
{'run':23398,'dipole':3,'mode':1},
{'run':23400,'dipole':3,'mode':2},
{'run':23403,'dipole':3.5,'mode':0},
{'run':23404,'dipole':3.5,'mode':1},
{'run':23406,'dipole':3.5,'mode':2},
{'run':23408,'dipole':4,'mode':0},
{'run':23409,'dipole':4,'mode':1},
{'run':23411,'dipole':4,'mode':2},
{'run':23414,'dipole':2.5,'mode':0},
{'run':23415,'dipole':2.5,'mode':1},
{'run':23421,'dipole':2.5,'mode':2},
{'run':24104,'dipole':0.5,'mode':0},
{'run':24105,'dipole':0.5,'mode':1},
{'run':24107,'dipole':0.5,'mode':2},
{'run':24110,'dipole':0.1,'mode':0},
{'run':24108,'dipole':0.1,'mode':1},
{'run':24111,'dipole':0.1,'mode':2}]

#for each of the dipole modes
dipole_voltages = [3,3.5,4,2.5,0.5,0.1]
out_pdf=PdfPages('transmission_residual_analysis.pdf')
for volt in dipole_voltages:
    print("Now analyzing dipole voltage: ", volt)
    up_run = [i for i in config_list if (i['dipole']==volt and i['mode']==0) ]
    print("Up Run: ", up_run)
    down_run = [i for i in config_list if (i['dipole']==volt and i['mode']==1) ]
    print("Down Run: ", down_run)
    chaos_run = [i for i in config_list if (i['dipole']==volt and i['mode']==2) ]
    plot_up = getErrorBarPlot( 'data/Tier1/output'+str(up_run[0]['run'])+'.root' )#,path="beans/TrendGraph00/TrendGraph00")
    plot_down=getErrorBarPlot('data/Tier1/output'+str(down_run[0]['run'])+'.root')#,path="beans/TrendGraph00/TrendGraph00")
    plot_chaos=getErrorBarPlot('data/Tier1/output'+str(chaos_run[0]['run'])+'.root')#,path="beans/TrendGraph00/TrendGraph00")
    #now plot all three
    plt.figure()
    plot_down_x = [ plot_down['X'][len(plot_down['X'])-1]-i for i in plot_down['X']]
    fig, ax = plt.subplots()
    ax.errorbar(plot_up['X'], plot_up['Y'], xerr=plot_up['ERR_X'], yerr=plot_up['ERR_Y'],color= getTableauColorasRGB(0))
    ax.errorbar(plot_down['X'], plot_down['Y'], xerr=plot_down['ERR_X'], yerr=plot_down['ERR_Y'],color= getTableauColorasRGB(2))
    #ax.errorbar(plot_chaos['X'], plot_chaos['Y'], xerr=plot_chaos['ERR_X'], yerr=plot_chaos['ERR_Y'],color= getTableauColorasRGB(4))
    ax.set_title("Transmission Functions at: "+str(volt)+" V Dipole" )
    #ax.set_xlabel("$(U_0-U_{IE})$")
    ax.set_xlabel("Time since run start")
    ax.set_ylabel("Normalized Transmission")
    ax.grid(True)
    out_pdf.savefig()
    plt.close()



    plt.figure()
    res_x=[]
    res_y=[]
    res_err_x=[]
    res_err_y=[]
    last_x = plot_up['X'][len(plot_up['X'])-1]
    for index,item in enumerate( plot_up['X'] ):
        #find the next closest point in the down list
        m = min(plot_down['X'], key=lambda x:abs(x-item) )
        down_index = plot_down['X'].index(m)

        res_x.append( (item+plot_down['X'][down_index])/2.0   )
        res_y.append( plot_up['Y'][index]-plot_down['Y'][down_index]   )
        res_err_x.append( (item-plot_down['X'][down_index])/2.0   )
        y_err_squared = math.pow(plot_up["ERR_Y"][index],2)+math.pow(plot_down['ERR_X'][down_index],2)
        res_err_y.append( math.sqrt(y_err_squared)   )

    plt.errorbar(res_x, res_y, xerr=res_err_x, yerr=res_err_y, color = getTableauColorasRGB(0) )
    plt.title("Residuals at "+str(volt)+" Dipole Voltage")
    plt.xlabel("$(U_0-U_{IE})$")
    plt.ylabel("Residual (Up-Down)")
    out_pdf.savefig()
    plt.close()

    plt.figure()
    fig, ax = plt.subplots()
    res_x=[]
    res_y=[]
    res_err_x=[]
    res_err_y=[]
    #last_x = plot_down['X'][len(plot_down['X'])-1]
    for index,item in enumerate( plot_down['X'] ):
        #find the next closest point in the down list
        m = min(plot_up['X'], key=lambda x:abs(x-item) )
        down_index = plot_up['X'].index(m)

        res_x.append( (item+plot_up['X'][down_index])/2.0   )
        res_y.append( plot_down['Y'][index]-plot_up['Y'][down_index]   )
        res_err_x.append( (item-plot_up['X'][down_index])/2.0   )
        y_err_squared = math.pow(plot_down["ERR_Y"][index],2)+math.pow(plot_up['ERR_X'][down_index],2)
        res_err_y.append( math.sqrt(y_err_squared)   )

    ax.errorbar(res_x, res_y, xerr=res_err_x, yerr=res_err_y, color = getTableauColorasRGB(0) )
    ax.set_title("Residuals at "+str(volt)+" Dipole Voltage")
    ax.set_xlabel("$(U_0-U_{IE})$")
    ax.set_ylabel("Residual (Down-UP)")
    ax.grid(True)
    out_pdf.savefig()
    plt.close()


#
d = out_pdf.infodict()
d['Title'] = 'Residual Analysis'
d['Author'] = u'Kevin Wierman'
d['Subject'] = 'Deuterium Output Formatter'
d['Keywords'] = 'Deuterium Tritium Residual KATRIN Kevin Wierman kwierman'
d['CreationDate'] = datetime.datetime(2009, 11, 13)
d['ModDate'] = datetime.datetime.today()
out_pdf.close()
