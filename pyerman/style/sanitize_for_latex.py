__sani_table__={
'\\' : r"\\textbackslash{}",
'{' : r"\\{",
'}' : r'\\}',
'$' : r'\\$',
'&' : r'\\&',
'#' : r'\\#',
'^' : r'\\textasciicircum{}',
'_' : '\\_',
'~' : r'\\textasciitilde{}',
'%':'\%'
}
def latex_sanitize(input):
    temp = input
    for item,value in __sani_table__:
        temp = temp.replace(item, value)
    return temp
