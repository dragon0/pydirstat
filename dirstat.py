#!/usr/bin/env python3
import os
import os.path

class FileItem:
    def __init__(self, path, size):
        self.path = path
        self.size = size

class DirectoryItem(FileItem):
    def __init__(self, path, size, subitems):
        FileItem.__init__(self, path, size)
        self.subitems = subitems

def walk(top):
    tree = {}
    for dirpath, dirnames, filenames in os.walk(top, topdown=False):
        dir = DirectoryItem(dirpath, 0, [])
        tree[dirpath] = dir
        for fn in filenames:
            stat = os.stat(os.path.join(dirpath, fn))
            dir.subitems.append(FileItem(os.path.join(dirpath, fn), stat.st_size))
            dir.size += stat.st_size
        for dn in dirnames:
            dn = os.path.join(dirpath, dn)
            subdir = tree[dn]
            dir.subdirs.append(subdir)
            dir.size += tree[dn]['size']
    return tree

def print_tree(tree, root, *, indent=0, **print_kwargs):
    print(' '*indent, os.path.basename(root) + os.path.sep, tree[root].size, **print_kwargs)
    for item in tree[root].subitems:
        if isinstance(item, DirectoryItem):
            print_tree(tree, item.path, indent=indent+2, **print_kwargs)
        else:
            print(' '*(indent+2), fn, size, **print_kwargs)

tree = walk('.')
print_tree(tree, '.')

