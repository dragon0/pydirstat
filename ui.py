import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tkmb
import dirstat

class FileFrame(tk.Frame):
    def __init__(self, parent, fileItem):
        tk.Frame.__init__(self, parent)
        self.fileItem = fileItem

        self.nameLabel = tk.Label(self, text=fileItem.path)
        self.nameLabel.pack(side=tk.LEFT)

        self.sizeLabel = tk.Label(self, text=fileItem.size)
        self.sizeLabel.pack(side=tk.LEFT)

class DirectoryFrame(tk.Frame):
    def __init__(self, parent, dirItem):
        tk.Frame.__init__(self, parent)
        self.dirItem = dirItem

        self.fileFrame = FileFrame(self, dirItem)
        self.fileFrame.pack(side=tk.TOP)

        self.subdirFrame = tk.Frame(self)
        self.subdirFrame.pack(side=tk.RIGHT)

        self.childFrames = c = []
        for item in dirItem.subitems:
            if isinstance(item, dirstat.DirectoryItem):
                frame = DirectoryFrame(self.subdirFrame, item)
            else:
                frame = FileFrame(self.subdirFrame, item)
            frame.pack(side=tk.TOP)
            c.append(frame)

class MainWindow(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.fileFrame = ff = tk.Frame(self)
        ff.pack(side=tk.TOP)

        self.topPath = tk.StringVar()
        self.topPath.set('.')
        self.topPathEntry = tpe = tk.Entry(ff, textvariable=self.topPath)
        tpe.pack(side=tk.LEFT)
        self.browseButton = bb = tk.Button(ff, text='...', command=self.selectDir)
        bb.pack(side=tk.LEFT)
        self.goButton = gb = tk.Button(ff, text='>', command=self.walk)
        gb.pack(side=tk.LEFT)

        self.treeFrame = ttk.Treeview(self, columns=('size',))
        self.treeFrame.heading('#0', text='Path')
        self.treeFrame.column('size', width=100)
        self.treeFrame.heading('size', text='Size')
        self.treeFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def selectDir(self, *args):
        #TODO
        pass

    def walk(self, *args):
        self.clear_tree()
        try:
            root = self.topPath.get()
            tree = dirstat.walk(root)
            self.insert_node(tree[root], tree)
        except Exception as e:
            #tkmb.showerror('Error', e)
            raise

    def clear_tree(self):
        c = self.treeFrame.get_children('')
        for i in c:
            self.treeFrame.delete(i)

    def insert_node(self, item, tree, parent=''):
        id = self.treeFrame.insert(parent, 'end', text=item.path, values=(item.size,))
        if isinstance(item, dirstat.DirectoryItem):
            for subitem in item.subitems:
                self.insert_node(subitem, tree, id)

def main():
    root = tk.Tk()
    mw = MainWindow(root)
    mw.pack(fill=tk.BOTH, expand=True)
    root.mainloop()

if __name__ == '__main__':
    main()

