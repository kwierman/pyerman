import os,sys
from ROOT import gROOT, TCanvas, TF1, TFile, TGraphErrors, Double

def getErrorBarPlot(filename, obj="NormalizedTransmissionFunction"):
    if ".root" in filename:
        try:
            path = "beans/{0}/{0}".format(obj)
            rootfile = TFile(filename)
            if (rootfile.IsZombie() ):
                return None
            output_object = rootfile.Get(path)
            n = output_object.GetN()

            x = [ output_object.GetX()[i].real for i in  range(n)]
            y = [ output_object.GetY()[i].real for i in  range(n)]
            err_x = [ output_object.GetEX()[i].real for i in  range(n)]
            err_y = [ output_object.GetEY()[i].real for i in  range(n)]
            return {'X':x, 'Y':y,'ERR_X':err_x, 'ERR_Y':err_y}
        except Exception as e:
            print e
            return {'X':[], 'Y':[],'ERR_X':[], 'ERR_Y':[]}

def getErrorBarSegmentPlot(filename, obj="NormalizedTransmissionFunction"):
    output = {}

    for index in range(0,21):
        path = "beans/Segment{0}/{1}/{1}".format(index,obj)
        if(index<10):
            path = "beans/Segment0{0}/{1}/{1}".format(index,obj)
        rootfile = TFile(filename)
        if (rootfile.IsZombie() ):
            return None
        output_object = rootfile.Get(path)
        n = output_object.GetN()

        x = [ output_object.GetX()[i].real for i in range(n)]
        y = [ output_object.GetY()[i].real for i in range(n)]
        err_x = [ output_object.GetEX()[i].real for i in range(n)]
        err_y = [ output_object.GetEY()[i].real for i in range(n)]

        output["Subrun{}".format(index) ]={'x':x, 'y':y,'xerr':err_x,'yerr':err_y}
    return output


def print_file(input_file, tablevel=0):
    input_file = TFile(input_file)
    print "Browsing: ", input_file.GetName()
    beansdir = input_file.Get("beans")
    n = beansdir.GetListOfKeys().GetEntries()
    print "Number of Entries: ", n
    for i in range(n):
        print '\t', beansdir.GetListOfKeys().At(i).GetName()
        d = input_file.Get(beansdir.GetName()+"/"+beansdir.GetListOfKeys().At(i).GetName()  )
        if not hasattr(d, "GetListOfKeys"):
            continue
        for j in range( d.GetListOfKeys().GetEntries() ):
            obj_name = d.GetListOfKeys().At(j).GetName()
            print "\t\t"+obj_name
            obj = input_file.Get(beansdir.GetName()+"/"+beansdir.GetListOfKeys().At(i).GetName()+"/"+obj_name )
