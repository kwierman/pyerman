import re
import os


def gen_metadata(base, structure, filetypes):
    """
        Walks a directory to fetch metadata from the directory tree structure
        and finds files at the tree terminus.

        :param: base The base path of the structure to walk
        :type: base str
        :param: structure A list of structures represented in the file path
        :type: structure list
        :param filetypes A dictionary matching a name of a file type to the
        regex search
        :type: filetypes dict

        :returns A dict of the metadata, with a field "path" for the end path
        of the tree
        and a field ['files'] matching the file types against the regex
        search returns.
    """

    for root, dirnames, filenames in os.walk(base):
        if len(filenames) > 0:
            path_split = root.split('/')
            metadata = {'path': root}
            for x, i in enumerate(reversed(structure)):
                metadata[i] = path_split[-1-x]
            metadata['files'] = {}
            for file_t in filetypes:
                ft = [i for i in filenames if re.search(filetypes[file_t],
                                                        i) is not None]
                metadata['files'][file_t] = ft
            yield metadata
