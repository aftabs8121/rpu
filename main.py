import tkinter as tk
from tkinter import *
from tkinter import ttk
from get_node_info import get_node_info
from node_cmds.cmd_script_upload import cmd_script_upload
from tkinter import messagebox
import os
import _thread
from ftp_download import download_spy

class find_device_details:
    selected_name = ''
    selected_addr = ''
    selected_platform = ''
    device_found = False
    def __init__(self, device_name):
        info = get_node_info()
        addr = info.node_addr
        name = info.device_name
        platform = info.device_platform
        #print('addr, name, platform:', addr, name, platform)

        for i in range(0, len(addr)):
            if str(name[i]) == device_name:
                find_device_details.selected_name       = str(device_name)
                find_device_details.selected_addr       = str(addr[i])
                find_device_details.selected_platform   = str(platform[i])
                messagebox.showinfo('Search', 'Found "' + str(device_name)+'" with address: '+str(addr[i])+' and platform: '+str(platform[i]))
                find_device_details.device_found = True
                break
            else:
                find_device_details.device_found = False

        if find_device_details.device_found == False:
            messagebox.showerror('Device Scan', 'Selected device not found, try again.')
            raise_frame(f3, '')


class find_device_name:
    device_name = ''
    def __init__(self, msg):
        device_name = str(msg[8:])
        find_device_name.device_name = device_name.upper()
        print('device_name:', find_device_name.device_name)

class available_script_file:
    def __init__(self, selected_node_name, selected_node_platform):
        file_list = ''
        if selected_node_platform == 'SM220':
            selected_node_platform = selected_node_name + '_B'
        else:
            selected_node_platform = selected_node_name + '_A'

        #for root, dirs, files in os.walk('spy/' + str(selected_node_name) + '/' + str(selected_node_platform)):
        for root, dirs, files in os.walk('spy/' + str(selected_node_name) + '/' + str(selected_node_platform)):
            for file in files:
                if file.endswith(".spy"):
                    #print('file name: ', file)
                    if file_list == '':
                        file_list = file
                    else:
                        file_list = file_list + ',' + file
        if file_list:
            file_list = file_list.split(',')
            #print('file_list:', file_list)
            #return file_list
            listbox.delete(0, tk.END)
            for item in file_list:
            #OnListSelection.listbox.insert(END, item)
                listbox.insert(tk.END, item)

class firmware_version_selection:
    script_version = ''
    def __init__(self, event, arg):
        listbox = arg
        item = listbox.curselection()
        firmware_version_selection.script_version = listbox.get(item[0])
        #print('firware version: ', firmware_version_selection.script_version)

class firmware_upload_process:
    def __init__(self):
        response = cmd_script_upload(
                    find_device_details.selected_name,
                    find_device_details.selected_addr,
                    find_device_details.selected_platform,
                    firmware_version_selection.script_version)
        #messagebox.showinfo('Device Update', 'Firmware Upload Complete!')
        if response == 'error':
            messagebox.showerror('Error', 'Could not upload the firmware')
            raise_frame(f3, '')
        else:
            raise_frame(f7, '')

class scan_selected_device:
    def __init__(self):
        # this means the device has been selected, now search the device and its related info
        try:
            find_device_details(find_device_name.device_name)
        except:
            messagebox.showerror('Device Error', 'Please check and make sure the SnapStick is attached to your system.')
            raise_frame(f3, '')
        # update the list of firmware versions
        available_script_file(find_device_details.selected_name, find_device_details.selected_platform)
        # don't proceed if desired device type not found
        if find_device_details.device_found == False:
            return
        raise_frame(f5, '')

class raise_frame:
    def __init__(self, frame, msg):
        #print(msg)

        if msg.find('f3') > 0:
            find_device_name(msg)

        elif msg.find('f4') > 0:
            _thread.start_new_thread(scan_selected_device, ())

        elif msg.find('f6') > 0:
            _thread.start_new_thread(firmware_upload_process, ())

        frame.tkraise()

def main():
    global listbox
    global image_label
    global summary_label
    global f7, f5, f3
    global btn3
    #btn_font = font.Font(family='Helvetica', size=36, weight='bold')

    # set size the console
    #os.system('mode con: cols=100 lines=20')

    # download all spy file when the window loads at program start
    print('Downloading spy files ...')
    dl = download_spy()
    print('Spy files downloaded complete!')

    # root as the main frame
    root = tk.Tk()

    # frame properties
    #root.resizable(0, 0)
    root.iconbitmap(default='img/icon.ico')
    root.title("COBRA Remote Programming Utility (RPU)")

    f1 = Frame(root)
    f2 = Frame(root)
    f3 = Frame(root)
    f4 = Frame(root)
    f5 = Frame(root)
    f6 = Frame(root)
    f7 = Frame(root)

    for frame in (f1, f2, f3, f4, f5, f6, f7):
        frame.grid(row=0, column=0, sticky='news')

    # f1
    txt0 = 'A simple, free software program for updating COBRA device firmware.'
    lbl0 = tk.Label(f1, text=txt0, justify='left', height = 3, font = '40', foreground='#53544e'
                    ).grid(row = 0, column = 0, columnspan=2)

    btn1 = tk.Button(f1, text='Single Device Update', height=5, width = 20, font='20', background = '#d4f442',
           command=lambda: raise_frame(f2, 'goto-f2')).grid(row = 1, column = 0)

    txt1 = 'A simple, step by step wizard for updating any device including' \
           'the 18R, 18R2, 18M, and Audio Box. All steps include pictures and' \
           'a video for walking you through the simple update procedure.'
    lbl1 = tk.Label(f1, text = txt1, justify='left', height= 6, width = 50,
            wraplength=300).grid(row = 1, column = 1)

    btn2 = tk.Button(f1, text='Update Devices in Batch', height=5, width = 20, font='20', background = '#33ffbd',
            command=lambda: raise_frame(f2, 'goto-f2')).grid(row = 2, column = 0)

    txt2 = 'Updating larger quantities of devices? Use the batch updater to ' \
           'save time and sit back as the program does all the work for you!'
    lbl2 = tk.Label(f1, text=txt2, justify='left', height=6, width = 50,
            wraplength=300).grid(row = 2, column = 1)



    # f2
    txt3 = 'Update a single device'
    lbl3 = tk.Label(f2, text=txt3, justify='left', height=2, font='40', foreground='#53544e'
                    ).grid(row=0, column=0, columnspan=4)
    txt4 = '    1. Choose Device to Update'
    lbl4 = tk.Label(f2, text=txt4, justify='left', height=2, font='30'
                    ).grid(row=1, column=0, columnspan=4)
    ll = tk.Label(f2, text='                 ').grid(row=2, column=0) # just for a gap to the left for following buttons
    btn21 = tk.Button(f2, text='18M', width = 10, background = '#57c93e',
                      command=lambda: raise_frame(f3, 'goto-f3-18m')).grid(row=2, column=1)
    #btn31 = tk.Button(f2, text='18MB', width = 10, background = '#57c93e',
    #                  command=lambda: raise_frame(f3, 'goto-f3-18mb')).grid(row=3, column=1)
    btn41 = tk.Button(f2, text='18MPA', width = 10, background = '#57c93e',
                      command=lambda: raise_frame(f3, 'goto-f3-18mpa')).grid(row=3, column=1)
    #btn51 = tk.Button(f2, text='18MBPA', width = 10, background = '#57c93e',
    #                  command=lambda: raise_frame(f3, 'goto-f3-18mbpa')).grid(row=5, column=1)
    btn22 = tk.Button(f2, text='18R', width = 10, background = '#3e6fc9',
                      command=lambda: raise_frame(f3, 'goto-f3-18r')).grid(row=2, column=2)
    #btn32 = tk.Button(f2, text='18RB', width = 10, background = '#3e6fc9',
    #                  command=lambda: raise_frame(f3, 'goto-f3-18rb')).grid(row=3, column=2)
    btn42 = tk.Button(f2, text='18R2', width = 10, background = '#3e6fc9',
                      command=lambda: raise_frame(f3, 'goto-f3-18r2')).grid(row=3, column=2)
    btn23 = tk.Button(f2, text='AB', width = 10, background = '#dd5e3b',
                      command=lambda: raise_frame(f3, 'goto-f3-ab')).grid(row=2, column=3)
    #btn33 = tk.Button(f2, text='ABB', width = 10, background = '#dd5e3b',
    #                  command=lambda: raise_frame(f3, 'goto-f3-abb')).grid(row=3, column=3)
    btn24 = tk.Button(f2, text='90M', width = 10, background = '#dd3bc4',
                      command=lambda: raise_frame(f3, 'goto-f3-90m')).grid(row=2, column=4)

    l7l = tk.Label(f2, text='                 ').grid(row=4, column=1)
    l72 = tk.Label(f2, text='                 ').grid(row=5, column=1)
    l73 = tk.Label(f2, text='                 ').grid(row=6, column=1)
    btn_bk = tk.Button(f2, text='Back', width=10,
                      command=lambda: raise_frame(f1, 'goto-f1')).grid(row=8, column=1)
    btn_mm = tk.Button(f2, text='Main Menu', width=10,
                       command=lambda: raise_frame(f1, 'goto-f1')).grid(row=8, column=6)
    # f3
    txt5 = 'Update a single device'
    lbl5 = tk.Label(f3, text=txt5, justify='left', height=2, font='40', foreground='#53544e'
                    ).grid(row=0, column=0, columnspan=4)
    txt6 = '    2. Place Unit in Program Mode'
    lbl6 = tk.Label(f3, text=txt6, justify='left', height=2, font='30'
                    ).grid(row=1, column=0, columnspan=4)
    ll = tk.Label(f3, text='                 ').grid(row=2, column=0)  # just for a gap to the left for following buttons
    txt7 = 'If your current firmware is 3.0.2 or higher, you need to place the device into program mode.\n' \
           '\n1. Power on device' \
           '\n2. Allow unit to boot up until channel is displayed' \
           '\n3. Hold SYNC until P is displayed' \
           '\n4. Once P is displayed, click NEXT to the right.'
    lbl7 = tk.Label(f3, text=txt7, justify='left', height= 7, width = 45,  wraplength=300,
                    ).grid(row=2, column=1, columnspan=4)
    btn3 = tk.Button(f3, text='Next', height=5, width = 15, font='20', background = '#d4f442',
                     command=lambda: raise_frame(f4, 'goto-f4')).grid(row=2, column=5, sticky='NE')
    ll = tk.Label(f3, text='                 ').grid(row=7, column=1)
    btn_bk = tk.Button(f3, text='Back', width=10,
                       command=lambda: raise_frame(f2, 'goto-f2')).grid(row=8, column=1)
    btn_mm = tk.Button(f3, text='Main Menu', width=10,
                       command=lambda: raise_frame(f1, 'goto-f1')).grid(row=8, column=5)

    # f4
    ll = tk.Label(f4, text='             ').grid(row=2, column=0)
    txt33 = 'Update a single device'
    lbl33 = tk.Label(f4, text=txt33, justify='left', height=2, font='40', foreground='#53544e'
                     ).grid(row=0, column=1, sticky='nw')
    txt34 = 'Scanning Selected Device'
    lbl11 = tk.Label(f4, text=txt34, justify='left', height=2, font='30'
                     ).grid(row=1, column=1, sticky='nw')
    pb2 = ttk.Progressbar(f4, orient="horizontal", length=200, mode="indeterminate")
    pb2.grid(row=2, column=1, sticky='nw')
    pb2.start()
    ll4 = tk.Label(f4, text='The scan process will take some time, please wait.')
    ll4.grid(row=3, column=1)

    # f5
    txt8 = 'Update a single device'
    lbl8 = tk.Label(f5, text=txt8, justify='left', height=2, font='40', foreground='#53544e'
                    ).grid(row=0, column=0, columnspan=4)
    txt9 = '    3. Select Firmware Version'
    lbl9 = tk.Label(f5, text=txt9, justify='left', height=2, font='30'
                    ).grid(row=1, column=0, columnspan=4)
    ll = tk.Label(f5, text='                 ').grid(row=2, column=0)  # just for a gap to the left for following buttons

    listbox = tk.Listbox(f5, height = 5, width = 50)
    listbox.grid(row=2, column=1)
    for item in ["one", "two", "three", "four"]:
        listbox.insert(tk.END, item)
    listbox.bind("<<ListboxSelect>>", lambda event, arg=listbox: firmware_version_selection(event, arg))

    ll = tk.Label(f5, text='  ').grid(row=2, column=5)  # just for a gap to the left for following buttons
    btn4 = tk.Button(f5, text='Next', height=5, width=15, font='20', background='#d4f442',
                        command=lambda: raise_frame(f6, 'goto-f6')).grid(row=2, column=6, sticky='NE')
                     #command=lambda: raise_frame(f6, 'goto-f5')).grid(row=2, column=6, sticky='NE')

    ll = tk.Label(f5, text='                 ').grid(row=7, column=1)
    btn_bk = tk.Button(f5, text='Back', width=10,
                       command=lambda: raise_frame(f3, 'goto-f3')).grid(row=8, column=1)
    btn_mm = tk.Button(f5, text='Main Menu', width=10,
                       command=lambda: raise_frame(f1, 'goto-f1')).grid(row=8, column=6)

    # f6
    ll = tk.Label(f6, text='             ').grid(row=2, column=0)
    txt10 = 'Update a single device'
    lbl10 = tk.Label(f6, text=txt10, justify='left', height=2, font='40', foreground='#53544e'
                     ).grid(row=0, column=1, sticky='nw')
    txt11 = 'Firmware Upgrade in Progress'
    lbl11 = tk.Label(f6, text=txt11, justify='left', height=2, font='30'
                     ).grid(row=1, column=1, sticky='nw')
    pb = ttk.Progressbar(f6, orient="horizontal", length=200, mode="indeterminate")
    pb.grid(row=2, column=1, sticky='nw')
    pb.start()
    ll2 = tk.Label(f6, text='The upgrade process will take some time, please wait.')
    ll2.grid(row=3, column=1)

    # f7
    txt12 = 'Update a single device'
    lbl12 = tk.Label(f7, text=txt12, justify='left', height=2, font='40', foreground='#53544e'
                     ).grid(row=0, column=0, columnspan=4)
    txt13 = '        Firmware Upgrade Complete'
    lbl13 = tk.Label(f7, text=txt13, justify='left', height=2, font='30'
                     ).grid(row=1, column=0, columnspan=4)
    ll = tk.Label(f7, text='                 ').grid(row=2, column=0)  # just for a gap to the left for following buttons
    txt14 = 'To confirm your device is on the correct firmware, please power your unit off, ' \
            'then power it on. You will see 5.0.2 selected as the new firmware.' \
            '\nYou are good to go!'
    lbl14 = tk.Label(f7, text=txt14, justify='left', height=4, wraplength=300,
                     ).grid(row=2, column=1, columnspan=4)
    btn6 = tk.Button(f7, text='Select Another Device', height=5, width=15, font='20', background='#d4f442', wraplength=100,
                     command=lambda: raise_frame(f2, 'goto-f2')).grid(row=2, column=6, sticky='NE')

    ll = tk.Label(f7, text='                 ').grid(row=7, column=1)
    btn_bk = tk.Button(f7, text='Back', width=10,
                       command=lambda: raise_frame(f5, 'goto-f5')).grid(row=8, column=1)
    btn_mm = tk.Button(f7, text='Main Menu', width=10,
                       command=lambda: raise_frame(f1, 'goto-f1')).grid(row=8, column=6)


    raise_frame(f1, 'goto-start')
    root.mainloop()


if __name__ == '__main__':
    main()