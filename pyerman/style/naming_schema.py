
__current_header__ = None
__current_subheader__= None


def setheading(heading):
    global __name_preset__ = heading.replace(" ", "_")
    return "# {}".format(heading)

def setSubHeading(subheading):
    global __current_subheader__ = subheading
    return "## {}".format(subheading

def getNamePreset():
    global __current_header__
    global __current_subheader__
    if __current_header__ is None:
        return "figure"
    elif __current_subheader__ is None:
        return __current_header__.replace(" ","_")
    else:
        return '{}_{}'.format(__current_header__, __current_subheader__).replace(" ",'_')
