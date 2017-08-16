from node_cmds import cmd_ping_network
from node_cmds import cmd_device_info
import parse_node_addrs
from tkinter import messagebox

class get_node_info:
    def __init__(self):
            # find available nodes
        try:
            result = cmd_ping_network.cmd_ping_network()
        except:
            messagebox.showerror('Device Scan', 'Ping command failed')
            # find node addresses
        try:
            self.node_addr = parse_node_addrs.parse_node_addrs(result)
        except:
            messagebox.showerror('Device Scan', 'Address parse failed')
            # find node device info
        try:
            self.device_name, self.device_platform = cmd_device_info.cmd_device_info(self.node_addr)
        except:
            messagebox.showerror('Device Scan', 'Device info cmd failed')
            pass