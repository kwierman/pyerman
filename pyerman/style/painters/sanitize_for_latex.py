import re


def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    try:
        return input._repr_latex_()
    except AttributeError:
        pass
    text = str(text)
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless',
        '>': r'\textgreater',
    }
    regex = re.compile('|'.join(
        re.escape(unicode(key)) for key in sorted(
            conv.keys(), key=lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)
