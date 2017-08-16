import subprocess
from node_cmds import cmd_script_info
from tkinter import messagebox
from subprocess_hdl import subprocess_args
import os, sys

cmd_str_device_info = ['snap', 'node', 'addr', 'info', 'device']

def cmd_device_info(node_addr):
    if len(node_addr):
        device_name = ''
        device_platform = ''
        for i in range(0, len(node_addr)):

            # lets use the firmware/script info method to extract name and platform
            name, platform = cmd_script_info.cmd_script_info(node_addr[i])
            #print('name: %s, platform: %s', name, platform)

            cmd_str_device_info[2] = str(node_addr[i])
            #print('Found node at addr:', str(node_addr[i]))
            with open('out.txt', 'w') as f:
                try:
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    env = os.environ
                    result = subprocess.check_output(cmd_str_device_info,
                                                     stdin=subprocess.PIPE,
                                                     stderr=subprocess.PIPE,
                                                     startupinfo=startupinfo,
                                                     env = env)
                    f.write(result)
                except OSError as e:
                    f.write('Failed: ' + str(e))
                    #messagebox.showerror('Error', '--device info cmd failed')
                    print('Can\'t find device info')
                    return
            print('Result::::: ', result)
            result = str(result).replace(' ', '')
            # device_name -- already found instead through script info cmd
            '''
            ptr = result.find('device.name')
            name = result[ptr + 11:]
            ptr = str(name).find('device.platform')
            name = name[:ptr - 2]
            if str(name) == '':
                name = 'N/A'
            # print('device info of ' + str(node_addr[i]) + ':\n' + str(result))
            # print('name: ' + str(name))
            '''
            if device_name == '':
                device_name = str(name)
            else:
                device_name = device_name + ',' + str(name)

            # device_platform
            ptr = result.find('device.platform')
            platform = result[ptr + 15:]
            ptr = str(platform).find('device.type')
            platform = platform[:ptr - 2]
            if str(platform) == '':
                platform = 'N/A'
            # print('device info of ' + str(node_addr[i]) + ':\n' + str(result))
            # print('name: ' + str(name))
            if device_platform == '':
                device_platform = str(platform)
            else:
                device_platform = device_platform + ',' + str(platform)

        device_name = device_name.split(',')
        device_platform = device_platform.split(',')

        #'''
        # remove junk from device names
        for i in range(0, len(device_name)):
            d_name = str(device_name[i])
            d_name = d_name.replace('\\', '')
            device_name[i] = d_name.replace('r', '')

        # remove junk from device platform
        for i in range(0, len(device_platform)):
            d_plat = str(device_platform[i])
            d_plat = d_plat.replace('\\', '')
            device_platform[i] = d_plat.replace('r', '')
        #'''


        return device_name, device_platform