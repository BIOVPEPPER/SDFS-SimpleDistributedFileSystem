import socket
import sys

SIZE = 8192

def getMem(sock):
    sock.sendto(b'GETMEM_t', ('127.0.0.1', 5005))
    data, addr = sock.recvfrom(1024)
    for i in data.decode('utf-8').split(','):
            print((int(i.split(' ')[0]),i.split(' ')[1],i.split(' ')[2]))

def getPred(sock):
    sock.sendto(b'GETPRED', ('127.0.0.1', 5005))
    data, addr = sock.recvfrom(1024)
    print(data.decode('utf-8'))

def getSelf(sock):
    sock.sendto(b'GETSELF', ('127.0.0.1', 5005))
    data, addr = sock.recvfrom(1024)
    print(data.decode('utf-8'))

def getSucc1(sock):
    sock.sendto(b'GETSUCC1', ('127.0.0.1', 5005))
    data, addr = sock.recvfrom(1024)
    print(data.decode('utf-8'))

def getSucc2(sock):
    sock.sendto(b'GETSUCC2', ('127.0.0.1', 5005))
    data, addr = sock.recvfrom(1024)
    print(data.decode('utf-8'))

def getLoss(sock):
    sock.sendto(b'GETLOSS', ('127.0.0.1', 5005))
    data, addr = sock.recvfrom(1024)
    print(data.decode('utf-8'))

def getMETA(sock, filename):
    sock.sendto(b'GETMAS 5006', ('127.0.0.1', 6019))
    masNum, addr = sock.recvfrom(SIZE)
    sock.sendto(b'GETMEM_t', ('127.0.0.1', 5005))
    mem_list, addr = sock.recvfrom(SIZE)
    mem_list = {i.split(' ')[0]:(i.split(' ')[1],i.split(' ')[2]) for i in mem_list.decode('utf-8').split(',')}
    masIP = mem_list[masNum.decode('utf-8')][0]
    sock.sendto(b'GETMETA', (masIP, 6020))
    meta, _  = sock.recvfrom(SIZE)
    meta = eval(meta.decode('utf-8'))
    if filename in meta:
        print(meta[filename])
    else:
        print('File Not Found!')

def getLocal(sock):
    sock.sendto(b'GETLOCAL', ('127.0.0.1', 6021))
    data, addr = sock.recvfrom(SIZE)
    print(data.decode('utf-8'))

def getVersions(sock, remotefile, num, localfile):
    sock.sendto(b'GETMAS 5006', ('127.0.0.1', 6019))
    masNum, addr = sock.recvfrom(SIZE)
    sock.sendto(b'GETMEM_t', ('127.0.0.1', 5005))
    mem_list, addr = sock.recvfrom(SIZE)
    mem_list = {i.split(' ')[0]:(i.split(' ')[1],i.split(' ')[2]) for i in mem_list.decode('utf-8').split(',')}
    masIP = mem_list[masNum.decode('utf-8')][0]
    sock_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock_TCP.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
    sock.sendto(('GETVER ' + remotefile + ' ' + str(num)).encode('utf-8'), (masIP, 6022))
    version_dict, _ = sock.recvfrom(SIZE)
    version_dict = eval(version_dict)
    max_ver = max([max(version_dict[key]) for key in version_dict.keys()])
    with open(localfile, 'wb') as file:
        for ver in range(max_ver, 0, -1):
            file.write((f'---------------- Version {ver} ----------------\n').encode('utf-8'))
            for key in version_dict.keys():
                if ver in version_dict[key]:
                    sock_TCP.connect((key.split(' ')[1], 6007))
                    request_R = 'R '+ remotefile + ' ' + str(ver)
                    sock_TCP.send(request_R.encode('utf-8'))
                    while True:
                        data = sock_TCP.recv(SIZE)
                        if not data:
                            break
                        file.write(data)
                    break
            sock_TCP.close()
            sock_TCP = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock_TCP.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            num -= 1
            if num == 0:
                sock_TCP.close()
                break
    

    






if __name__ == "__main__":
    sockObj = socket.socket(socket.AF_INET, # Internet
                        socket.SOCK_DGRAM) # UDP
    sockObj.bind(('0.0.0.0', 5006))
    if sys.argv[1] == 'list_mem':
        getMem(sockObj)
    if sys.argv[1] == 'list_self':
        getSelf(sockObj)
    if sys.argv[1] == 'list_pred':
        getPred(sockObj)
    if sys.argv[1] == 'list_succ1':
        getSucc1(sockObj)
    if sys.argv[1] == 'list_succ2':
        getSucc2(sockObj)
    if sys.argv[1] == 'set_loss_3':
        sockObj.sendto(b'SETLOSS_3', ('127.0.0.1', 5005))
    if sys.argv[1] == 'set_loss_30':
        sockObj.sendto(b'SETLOSS_30', ('127.0.0.1', 5005))
    if sys.argv[1] == 'set_loss_0':
        sockObj.sendto(b'SETLOSS_0', ('127.0.0.1', 5005))
    if sys.argv[1] == 'get_loss':
        getLoss(sockObj)
    if sys.argv[1] == 'ls':
        getMETA(sockObj, sys.argv[2])
    if sys.argv[1] == 'store':
        getLocal(sockObj)
    if sys.argv[1] == 'get_version':
        getVersions(sockObj, sys.argv[2], int(sys.argv[3]), sys.argv[4])

