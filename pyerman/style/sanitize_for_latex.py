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
    for item in __sani_table__:
        temp = temp.replace(item, __sani_table__[item])
    return temp
