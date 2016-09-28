from .importROOT import ROOT
from ROOT import TFile


def getValueFromConfig(filename, key):
    input_file = ROOT.TFile(filename)
    config = input_file.Get("config")
    geometry = config.Get("geometry")
    for object_key in geometry.GetListOfKeys():
        if key in object_key.GetName():
            return object_key.GetName().split("value=\"")[1].split("\"")[0]
    raise ValueError("Key Not Found in File")


def getEGunEnergy(filename):
    input_file = ROOT.TFile(filename)
    config = input_file.Get("config")
    geometry = config.Get('ksgen_generator_composite name="egun_gauss_cosine" \
    pid="11"')
    energy = geometry.Get('energy_composite')
    for object_key in energy.GetListOfKeys():
        if "energy_gauss" in object_key.GetName():
            name = object_key.GetName()
            name = name.split("value_mean=\"")[1].split("\"")[0]
            value = object_key.GetName().split("value_sigma=\"")[1]
            value = value.split("\"")[0]
            return name, value
    raise ValueError("Key Not Found in File")


def getEGunThetaDirection(filename):
    input_file = ROOT.TFile(filename)
    config = input_file.Get("config")
    geometry = config.Get('ksgen_generator_composite name="egun_gauss_cosine" \
    pid="11"')
    energy = geometry.Get('direction_surface_composite surfaces=\
    "world\\egun\\@generator_tag" outside="true"')
    for object_key in energy.GetListOfKeys():
        if "theta_cosine" in object_key.GetName():
            n = object_key.GetName().split("angle_min=\"")[1].split("\"")[0]
            m = object_key.GetName().split("angle_max=\"")[1].split("\"")[0]
            return n, m
    raise ValueError("Key Not Found in File")


def getEGunPhiDirection(filename):
    input_file = ROOT.TFile(filename)
    config = input_file.Get("config")
    geometry = config.Get('ksgen_generator_composite name="egun_gauss_cosine" \
    pid="11"')
    energy = geometry.Get('direction_surface_composite surfaces=\
    "world\\egun\\@generator_tag" outside="true"')
    for object_key in energy.GetListOfKeys():
        if "phi_uniform" in object_key.GetName():
            n = object_key.GetName().split("value_min=\"")[1].split("\"")[0]
            m = object_key.GetName().split("value_max=\"")[1].split("\"")[0]
            return n, m
    raise ValueError("Key Not Found in File")


def getElectrodeEGunDipole(filename):
    return getValueFromConfig(filename, "electrode_egun_dipole")


def getElectrodeEGunGround(filename):
    return getValueFromConfig(filename, "electrode_egun_ground")


def getElectrodeEGunBack(filename):
    return getValueFromConfig(filename, "electrode_egun_back")


def getElectrodeEGunFront(filename):
    return getValueFromConfig(filename, "electrode_egun_front")


def getMainSpecHull(filename):
    return getValueFromConfig(filename, 'electrostatic_dirichlet \
    surfaces="axial_main_spec_assembly/@hull_tag"')


def getWireElectrodes(filename):
    return getValueFromConfig(filename,
                              'axial_main_spec_assembly/\
    downstream_middle_flat_cone_module/@middle_flat_cone_inner_wire_tag')


def getErrorBarPlot(filename, obj="NormalizedTransmissionFunction"):
    if ".root" in filename:
        try:
            path = "beans/{0}/{0}".format(obj)
            rootfile = TFile(filename)
            if (rootfile.IsZombie()):
                return None
            output_object = rootfile.Get(path)
            n = output_object.GetN()

            x = [output_object.GetX()[i].real for i in range(n)]
            y = [output_object.GetY()[i].real for i in range(n)]
            err_x = [output_object.GetEX()[i].real for i in range(n)]
            err_y = [output_object.GetEY()[i].real for i in range(n)]
            return {'X': x, 'Y': y, 'ERR_X': err_x, 'ERR_Y': err_y}
        except Exception as e:
            print(e)
            return {'X': [], 'Y': [], 'ERR_X': [], 'ERR_Y': []}


def getErrorBarSegmentPlot(filename, obj="NormalizedTransmissionFunction"):
    output = {}

    for index in range(0, 21):
        path = "beans/Segment{0}/{1}/{1}".format(index, obj)
        if(index < 10):
            path = "beans/Segment0{0}/{1}/{1}".format(index, obj)
        rootfile = TFile(filename)
        if (rootfile.IsZombie()):
            return None
        output_object = rootfile.Get(path)
        n = output_object.GetN()

        x = [output_object.GetX()[i].real for i in range(n)]
        y = [output_object.GetY()[i].real for i in range(n)]
        err_x = [output_object.GetEX()[i].real for i in range(n)]
        err_y = [output_object.GetEY()[i].real for i in range(n)]

        output["Subrun{}".format(index)] = {'x': x,
                                            'y': y,
                                            'xerr': err_x,
                                            'yerr': err_y}
    return output


def getSegmentHist(filename, obj="NormalizedTransmissionFunction"):
    output = {}

    for index in range(0, 21):
        path = "beans/Segment{0}/{1}/{1}".format(index, obj)
        if(index < 10):
            path = "beans/Segment0{0}/{1}/{1}".format(index, obj)
        rootfile = TFile(filename)
        if (rootfile.IsZombie()):
            return None
        output_object = rootfile.Get(path)
        nx = output_object.GetNbinsX()
        x = [output_object.GetBinCenter(i) for i in range(nx)]
        ny = output_object.GetNbinsY()
        y = [output_object.GetBinContent(i) for i in range(ny)]

        output["Subrun{}".format(index)] = {'x': x,
                                            'y': y}
    return output


def print_file(input_file, tablevel=0):
    input_file = TFile(input_file)
    print("Browsing: ", input_file.GetName())
    beansdir = input_file.Get("beans")
    n = beansdir.GetListOfKeys().GetEntries()
    print("Number of Entries: ", n)
    for i in range(n):
        print('\t', beansdir.GetListOfKeys().At(i).GetName())
        nm = beansdir.GetName()+"/"+beansdir.GetListOfKeys().At(i).GetName()
        d = input_file.Get(nm)
        if not hasattr(d, "GetListOfKeys"):
            continue
        for j in range(d.GetListOfKeys().GetEntries()):
            obj_name = d.GetListOfKeys().At(j).GetName()
            print("\t\t"+obj_name)
            nm = beansdir.GetName()
            nm += "/"+beansdir.GetListOfKeys().At(i).GetName()
            nm += "/"+obj_name
            obj = input_file.Get(nm)
            print(obj)
