import ROOT
from root_numpy import root2array, root2rec, tree2rec
from ROOT import gROOT, TCanvas, TF1, TFile, TGraphErrors, Double

import logging
import exceptions

logger = logging.getLogger(__name__)

class PyListOfLeaves(dict):
    pass

class CallBackPrototype:
    def __init__(self, leafname):
        self.leafname=leafname
    def at_get_entry(self, pyl, tree):
        pass

class GetValueAsListCallBack(CallBackPrototype):
    def __init__(self, leafname):
        self.leafname=leafname
        self.values=[]
    def at_get_entry(self, pyl, tree):
        self.values.append( getattr(pyl,self.leafname).GetValue() )
    def get_values(self):
        return self.values

class GetStringsAsListCallBack(CallBackPrototype):
    def __init__(self, leafname):
        self.leafname=leafname
        self.values=[]
    def at_get_entry(self, pyl, tree):
        s = list( getattr(tree, self.leafname)  )
        self.values.append( ''.join(s) )
    def get_values(self):
        return self.values

class KassiopeiaFile:

    def __init__(self, filename="NonAxialEGunSimulation-0.root"):
        self.filename = filename
        self.f = TFile(self.filename, 'read')
        if self.f.IsZombie():
            self.f.Close()
            raise exceptions.IOError("TFile is Zombie: "+filename)
        else:
            self.f.Close()

    def getArray(self, treename):
        return root2array(self.filename, treename)

    def getRecord(self,treename):
        """
        # Rename the fields
        rec.dtype.names = ('x', 'y', 'sqrt_y', 'landau_x', 'cos_x_sin_y')

        # Convert the NumPy record array into a TTree
        tree = array2tree(rec, name='tree')

        # Dump directly into a ROOT file without using PyROOT
        array2root(rec, 'selected_tree.root', 'tree')
        """
        return  root2rec(self.filename, treename)

    def getTrackArray(self):
        """
        rec = tree2rec(intree,
        branches=['x', 'y', 'sqrt(y)', 'TMath::Landau(x)', 'cos(x)*sin(y)'],
        selection='z > 0',
        start=0, stop=10, step=2)
        """
        return self.getArray("output_track_world_DATA")

    def getStepArray(self):
        return self.getArray("output_step_world_DATA")

    def explore_tree(self, treename="output_track_world_DATA"):
        f = TFile(self.filename, 'read')
        tree=f.Get(treename)
        leaves = tree.GetListOfLeaves()
        output=[leaves.At(i).GetName() for i in range(0, leaves.GetEntries() ) ]

    def get_tree_class(self, treename):
        f = TFile(self.filename, 'read')
        tree=f.Get(treename)
        leaves = tree.GetListOfLeaves()
        pyl = PyListOfLeaves()
        for i in range(0,leaves.GetEntries() ) :
            leaf = leaves.At(i)
            name = leaf.GetName()
            pyl.__setattr__(name,leaf)
        return pyl

    def getTreeLeafValues(self, treename, callbacks=[] ):
        f = TFile(self.filename, 'read')
        tree=f.Get(treename)
        leaves=None
        try:
            leaves = tree.GetListOfLeaves()
        except Exception as e:
            self.logger.warning("Tree not in File: "+treename)
            self.logger.warning(e)
            return
        pyl = self.get_tree_class(treename)

        nev = tree.GetEntries()
        for iev in range(0,nev) :
            tree.GetEntry(iev)
            #perform the callback
            for c in callbacks:
                c.at_get_entry(pyl, tree)
                
