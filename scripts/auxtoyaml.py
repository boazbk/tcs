#!/usr/bin/python

from os import listdir
from os.path import isfile, join
import os
import re
import yaml
import sys

def readaux(D,f,path="."):
    """
    Read the aux file f and update dictionary D with
    D[label] = {"file":filename (no ext), "class": type (section, theorem, etc..) , "number": number of object (e.g., 1.3)}
    for sections
    TOC[number] = {"filename": file, "title": title, "href": labelid}
    """
    onlyfile = os.path.splitext(f)[0]
    fullname = join(path,f)
    reg = re.compile(r'\\newlabel\{([a-zA-Z\-\_0-9\:]+)\@cref\}\{\{\[([a-zA-Z ]+)\]\[([a-zA-Z0-9 ]*)\]\[([a-zA-Z0-9\,\. ]*)\]([a-zA-Z0-9\,\. ]*)\}.*\}')

    with open(fullname,mode="r",encoding="utf-8") as aux:
        lines = aux.read().split("\n")
        for l in lines:
            m = reg.match(l)
            if m:
                label, kind , _ , _ , number = m.groups()
                D[label] = {"file":onlyfile,"class":kind,"number": number}

def readallaux(path):
    """
    Read all aux files in a directory into a dictionary
    """
    D = {}
    auxfiles = [f for f in listdir(path) if isfile(join(path, f)) and len(f)>4 and f[-4:]==".aux"]
    for f in auxfiles:
        readaux(D,f,path)
    return D

def dumpdict(D,filename):
    """Utility function to dump a dictoinary to a yaml file"""
    with open(filename,mode="w", encoding="utf-8") as file:
        yaml.dump(D,file)

def main():
    args = sys.argv[1:]
    path = args[0] if args else "."
    file = args[1] if len(args)>1 else "bookaux.yaml"
    D = readallaux(path)
    dumpdict(D,file)


if __name__ == '__main__':
    main()
