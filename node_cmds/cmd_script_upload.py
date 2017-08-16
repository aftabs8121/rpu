import subprocess
from pathlib import Path
#from main import *

cmd_scr_upload = ['snap', 'node', 'addr', 'script', 'upload', 'spy/AB_v5.spy'] #'C:/temp/AB_SM220.spy']

def cmd_script_upload(name, addr, platform, filename):
    result = 0
    #print('cmd_script_upload.....')
    #print('parameters: ', name, addr, platform, filename)
    # stuff the address into the cmd
    cmd_scr_upload[2] = str(addr)

    try:
        # find which device selected
        name = str(name)
        addr = str(addr)
        platform = str(platform)
        filename = str(filename)
        #if name == 'AB' and platform == 'SM220':
        if platform == 'SM220':
            cmd_scr_upload[5] = 'spy/' + name + '/' + name + '_B' + '/' + filename
        elif platform == 'RF200':
            cmd_scr_upload[5] = 'spy/' + name + '/' + name + '_A' + '/' + filename
        else:
            print('Wrong device/platform/version combination selected')
            #main.prog_msg.config(text = 'Wrong device/platform/version combination selected')

        # upload the image/firmware
        print('file to upload: ', str(cmd_scr_upload[5]))
        script_file = Path(cmd_scr_upload[5])
        if script_file.is_file():
            # execute cmd
            #print('executing the cmd...')
            result = subprocess.check_output(cmd_scr_upload)
            if result:
                result = result.decode('utf-8')
                #print('prog output:', result)
        else:
            print('required script file not found')

    except:
        print('Error: Could not upload the firmware')
        result = 'error'

    return result