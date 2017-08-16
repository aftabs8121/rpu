import subprocess
cmd_find_nodes = ['snap', 'network', 'ping']

def cmd_ping_network():

    try:
        result = subprocess.check_output(cmd_find_nodes)
        if result:
            #result = "Found nodes: \n" + result.decode('utf-8')
            result = result.decode('utf-8')
    except:
        #msg_lable.config(text="Err: Snapstick not found", bg="red")
        print('Error: Network ping command failed.')
        result = 'error'

    return result