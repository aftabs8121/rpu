import subprocess
cmd_scr_info = ['snap', 'node', 'addr', 'info', 'script']
from tkinter import messagebox

def cmd_script_info(node_addr):
    cmd_scr_info[2] = str(node_addr)
    try:
        result = subprocess.check_output(cmd_scr_info)
        if result:
            #result = "Found nodes: \n" + result.decode('utf-8')
            result = result.decode('utf-8')
            ptr = result.find('device.script-name')
            script = result[ptr + 20:]
            #print('script info:', script)
            script = str(script)
            ss = 'SnapStick'
            if ss in script:
                name = 'SnapStick'
                platform = 'SnapStick'
            else:
                script_info = script.split('_')
                name = str(script_info[1])
                platform = str(script_info[2])
        else:
            name = ''
            platform = ''
        return name, platform
    except:
            #messagebox.showerror('Error', 'cmd cmd_script_info failed')
            return 'error', 'error'

