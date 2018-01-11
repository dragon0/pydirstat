#!/usr/bin/env python3
import os
import os.path

class FileItem:
    def __init__(self, path, size, parent=None):
        self.path = path
        self.size = size
        self.parent = parent

    def __repr__(self):
        return 'FileItem({0.path}, {0.size}, {0.parent})'.format(self)

class DirectoryItem(FileItem):
    def __init__(self, path, size, subitems, parent=None):
        FileItem.__init__(self, path, size, parent)
        self.subitems = subitems

    def __repr__(self):
        return 'DirectoryItem({0.path}, {0.size}, {0.parent}, {1})'.format(
                self,
                list(map(lambda f: f.path, self.subitems)))

def walk(top, cb=None):
    tree = {top: DirectoryItem(top, 0, [])}
    for dirpath, dirnames, filenames in os.walk(top, topdown=False):
        dir = tree.setdefault(dirpath, DirectoryItem(dirpath, 0, []))
        for fn in filenames:
            try:
                stat = os.stat(os.path.join(dirpath, fn))
                size = stat.st_size
            except:
                size = 0
            dir.subitems.append(FileItem(os.path.join(dirpath, fn), size, dir))
            dir.size += size
        for dn in dirnames:
            dn = os.path.join(dirpath, dn)
            subdir = tree.setdefault(dn, DirectoryItem(dn, 0, []))
            subdir.parent = dir.path
            dir.subitems.append(subdir)
            dir.size += tree[dn].size
        if cb:
            cb(tree)
    return tree

def print_tree(tree, root, *, indent=0, **print_kwargs):
    print(' '*indent, os.path.basename(root) + os.path.sep, tree[root].size, **print_kwargs)
    for item in tree[root].subitems:
        if isinstance(item, DirectoryItem):
            print_tree(tree, item.path, indent=indent+2, **print_kwargs)
        else:
            print(' '*(indent+2), item.path, item.size, **print_kwargs)

