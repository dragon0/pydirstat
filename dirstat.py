#!/usr/bin/env python3
import os
import os.path

def walk(top):
    tree = {}
    for dirpath, dirnames, filenames in os.walk(top, topdown=False):
        dir = dict(size=0, files={}, subdirs=[])
        tree[dirpath] = dir
        for fn in filenames:
            stat = os.stat(os.path.join(dirpath, fn))
            dir['files'][fn] = stat.st_size
            dir['size'] += stat.st_size
        for dn in dirnames:
            dn = os.path.join(dirpath, dn)
            dir['subdirs'].append(dn)
            dir['size'] += tree[dn]['size']
    return tree

