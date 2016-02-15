from .importROOT import ROOT
from  ROOT import TFile
import exceptions

class PyListOfLeaves(dict):
    """
        PyListofLeaves was originally designed to work as an abstract class that
        would be defined though successive calls to getattr, setattr. In the
        interest of maintaining  the idea of resurrecting that idea, this class
        remains.
    """
    pass


class BaseGenerator:
    """
        BaseGenerator exits to generate leaves from a tree in a given root file.
        While realistically, multiple classes shouldn't be accessing the same
        root file, this relatively safe implementation can be used multiple
        times on the same file simultaniously.

        This generator exists to pull out one iteration of branch at a time.
    """
    def __init__(self, filename="something.root", treename="mytree;0"):
        self.filename = filename
        self.treename = treename
        self.f = None

    def __del__(self):
        self.closeFile()

    def __len__(self):
        if self.f is None:
            self.openFile()
        return self.nev

    def openFile(self):
        self.f = TFile(self.filename, 'read')
        if self.f.IsZombie():
            self.f.Close()
            raise exceptions.IOError("TFile is Zombie: "+self.filename)

        self.tree = self.f.Get(self.treename)
        try:
            self.leaves= self.tree.GetListOfLeaves()
        except Exception as e:
            print(e)
            self.closeFile()
            raise exceptions.IOError("Tree Does not Exist or is empty: "+self.treename)
        self.pyl = PyListOfLeaves()
        for i in range(0,self.leaves.GetEntries()) :
            leaf = self.leaves.At(i)
            name = leaf.GetName()
            self.pyl[name]=leaf
        self.nev = self.tree.GetEntries()
        self.iev=0

    def closeFile(self):
        if self.f is not None:
            self.f.Close()
        self.f = None

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        """
        raises: StopIteration when it reaches the end of the file, then it resets itself so that the file
        can be parsed a second time.
        """
        if self.f is None:
            self.openFile()

        if self.iev>self.nev:
            self.iev=0
            self.closeFile()
            raise StopIteration()
        self.tree.GetEntry(self.iev)
        self.iev+=1
        return self.pyl, self.tree
