from tkinter import messagebox
from get_node_info import get_node_info

class refresh_node_info:
    def __init__(self, treeView):
        #delete all info in this tree
        treeView.delete(*treeView.get_children())
        # get latest node info
        try:
            info = get_node_info()
            self.node_addr = info.node_addr
            self.device_name = info.device_name
            self.device_platform = info.device_platform

            # stuff data into tree
            for i in range(0, len(self.node_addr)):
                # remove the '\r' found while runing the exe
                self.device_platform[i] = str(self.device_platform[i]).replace('\r', '')
                self.device_platform[i] = str(self.device_platform[i]).replace('\\', '')
                self.device_platform[i] = str(self.device_platform[i]).replace('r', '')
                treeView.insert("", i, text=self.device_name[i], values=(self.node_addr[i], self.device_platform[i]))
            self.tView = treeView

            messagebox.showinfo("Search", "Found " + str(len(self.node_addr)) + " nodes")

        except:
            treeView.delete(*treeView.get_children())
            # stuff data into tree
            for i in range(0, len(self.node_addr)):
                treeView.insert("", i, text='Not found', values=('Not found', 'Not found'))
            self.tView = treeView
            messagebox.showinfo("Error", "Seems like your SnapStick is not attached to your system\rPlease attach one"
                                         " and press 'Refresh' button")
