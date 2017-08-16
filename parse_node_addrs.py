
def parse_node_addrs(result):
    if result:
        #print('result:\n' + result)
        node_addr = ''
        node_array = result.split(' ')
        #print('node_array:\n' + str(node_array))
        for i in range (0, len(node_array)):
            if len(node_array[i]) >= 6:
                if '\n' in node_array[i]:
                    data = node_array[i].split()
                    node_array[i] = data[1]
                if node_addr == '':
                    node_addr = node_array[i]
                else:
                    node_addr = node_addr + ',' + node_array[i]
        node_addr = node_addr.split(',')
        #print('node_addr:\n' + str(node_addr))
        #msg_lable.config(text=out_array)
    return node_addr