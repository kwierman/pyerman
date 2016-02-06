

import os

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import math
import datetime
from numpy.fft import fft, ifft

from tableau_color import getTableauColorasRGB
from root_interface import getErrorBarPlot


#for each of the dipole modes
d = out_pdf.infodict()
d['Title'] = 'Residual Analysis'
d['Author'] = u'Kevin Wierman'
d['Subject'] = 'Deuterium Output Formatter'
d['Keywords'] = 'Deuterium Tritium Residual KATRIN Kevin Wierman kwierman'
d['CreationDate'] = datetime.datetime(2009, 11, 13)
d['ModDate'] = datetime.datetime.today()

for volt in dipole_voltages:
    print("Now analyzing dipole voltage: ", volt)
    up_run = [i for i in config_list if (i['dipole']==volt and i['mode']==0) ]
    print("Up Run: ", up_run)
    down_run = [i for i in config_list if (i['dipole']==volt and i['mode']==1) ]
    print("Down Run: ", down_run)
    chaos_run = [i for i in config_list if (i['dipole']==volt and i['mode']==2) ]
    plot_up    = getErrorBarPlot('data/Tier1/output'+str(up_run[0]['run'])+'.root'   ,path="beans/TrendGraph00/TrendGraph00")
    plot_down  = getErrorBarPlot('data/Tier1/output'+str(down_run[0]['run'])+'.root' ,path="beans/TrendGraph00/TrendGraph00")
    plot_chaos = getErrorBarPlot('data/Tier1/output'+str(chaos_run[0]['run'])+'.root',path="beans/TrendGraph00/TrendGraph00")

    #now plot all three
    plt.figure()




    length = len(plot_down['X'])
    adjust=1
    plot_up['X']=plot_up['X'][adjust:length+adjust]
    plot_up['Y']=plot_up['Y'][adjust:length+adjust]
    plot_up['ERR_X']=plot_up['ERR_X'][adjust:length+adjust]
    plot_up['ERR_Y']=plot_up['ERR_Y'][adjust:length+adjust]

    plot_down['X']=plot_down['X']
    plot_down['Y']=plot_down['Y']
    plot_down['ERR_X']=plot_down['ERR_X']
    plot_down['ERR_Y']=plot_down['ERR_Y']
    #print "Length of both, ",len(plot_down['Y']), " , ", len(plot_up['Y'])

    fig, ax = plt.subplots()
    ax.errorbar(plot_up['X'], plot_up['Y'], xerr=plot_up['ERR_X'], yerr=plot_up['ERR_Y'],color= getTableauColorasRGB(0))
    ax.errorbar(plot_down['X'], plot_down['Y'], xerr=plot_down['ERR_X'], yerr=plot_down['ERR_Y'],color= getTableauColorasRGB(2))
    ax.set_title("Transmission Functions at: "+str(volt)+" V Dipole" )
    ax.set_xlabel("Time since run start")
    ax.set_ylabel("Normalized Transmission")
    ax.grid(True)
    out_pdf.savefig()
    plt.close()



    plt.figure()
    fig, ax = plt.subplots()
    plot_down['Y'] = [i for i in reversed(plot_down['Y'])]

    ax.errorbar(plot_up['Y'], plot_down['Y'], xerr=plot_up['ERR_Y'], yerr=plot_down['ERR_Y'],color= getTableauColorasRGB(0))
    ax.set_title("Time assigned positions in Transmission function" )
    ax.set_xlabel("Up Transmission Function")
    ax.set_ylabel("Down Transmission Function")
    ax.grid(True)
    out_pdf.savefig()
    plt.close()

    plt.figure()
    fig, ax = plt.subplots()
    ax.errorbar(plot_up['X'], plot_down['X'], xerr=plot_up['ERR_X'], yerr=plot_down['ERR_X'],color= getTableauColorasRGB(0))
    ax.set_title("Time Up Vs Time Down" )
    ax.set_xlabel("Up Transmission Function")
    ax.set_ylabel("Down Transmission Function")
    ax.grid(True)
    out_pdf.savefig()
    plt.close()


    plt.figure()
    fig, ax = plt.subplots()
    res_x=[]
    res_y=[]
    res_err_x=[]
    res_err_y=[]
    for i in range(len(plot_up['X'])):
        x = plot_down['X'][i]
        res_x.append( (plot_up['X'][i]+x)/2.0   )
        res_y.append( plot_up['Y'][i]-plot_down['Y'][len(plot_down['Y'])-i-1]   )
        res_err_x.append( (plot_up['X'][i]-x)/2.0   )
        y_err_squared = math.pow(plot_up["ERR_Y"][i],2)+math.pow(plot_down['ERR_X'][i],2)
        res_err_y.append( math.sqrt(y_err_squared)   )


    ax.errorbar(res_x, res_y, xerr=res_err_x, yerr=res_err_y, color = getTableauColorasRGB(0) )
    ax.set_title("Residuals at "+str(volt)+" Dipole Voltage")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Residual (Up-Down)")
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
        #m = min(plot_up['X'], key=lambda x:abs(2+last_x-x-item) )
        #down_index = plot_up['X'].index(m)

        res_x.append( (item+plot_up['X'][index])/2.0   )
        res_y.append( plot_down['Y'][index]-plot_up['Y'][index]   )
        res_err_x.append( (item-plot_up['X'][index])/2.0   )
        y_err_squared = math.pow(plot_down["ERR_Y"][index],2)+math.pow(plot_up['ERR_X'][index],2)
        res_err_y.append( math.sqrt(y_err_squared)   )

    ax.errorbar(res_x, res_y, xerr=res_err_x, yerr=res_err_y, color = getTableauColorasRGB(0) )
    ax.set_title("Residuals at "+str(volt)+" Dipole Voltage")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Residual (Down-UP)")
    ax.grid(True)
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

    res_y = fft(res_y)
    ax.errorbar(res_x[0:len(res_x)/2:1], res_y[0:len(res_x)/2:1], xerr=res_err_x[0:len(res_x)/2:1], yerr=res_err_y[0:len(res_x)/2], color = getTableauColorasRGB(0) )
    ax.set_title("FFT Residuals at "+str(volt)+" Dipole Voltage")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Residual (Down-UP)")
    ax.grid(True)
    out_pdf.savefig()
    plt.close()





#
out_pdf.close()


#plt.show()
