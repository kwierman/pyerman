__sani_table__ = {
    '&':  r'\&',
    '%':  r'\%',
    '$':  r'\$',
    '#':  r'\#',
    '_':  r'\letterunderscore{}',
    '{':  r'\letteropenbrace{}',
    '}':  r'\letterclosebrace{}',
    '~':  r'\lettertilde{}',
    '^':  r'\letterhat{}',
    '\\': r'\letterbackslash{}',
}

def latex_sanitize(input):
    temp = input
    for item,value in __sani_table__:
        temp = temp.replace(item, value)
    return temp
