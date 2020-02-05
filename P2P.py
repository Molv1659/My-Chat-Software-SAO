"""
communicate with the other users
functions:
send msg
send file
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from socket import *
import threading
import json
import time
import os
from CS import *


def send_msg_thread(ip, port, data):
    data = json.dumps(data)  # dict 2 str
    msg_sender = socket(AF_INET, SOCK_STREAM)
    try:
        msg_sender.connect((ip,port))
        msg_sender.sendall(data.encode('utf-8'))
    except Exception as e:
        print('fail to send msg')
        print(e)
    finally:
        msg_sender.close()


def send_msg(src, dst, port, msg):
    data = {}
    data['type'] = 'text'
    data['src'] = src
    data['dst'] = dst
    data['data'] = msg
    data['time'] = time.asctime(time.localtime(time.time()))

    ip = query_state(dst)
    if ip == 'n':
        return False
    t = threading.Thread(target=send_msg_thread, args=(ip,port,data))
    t.start()
    return True

def send_group_msg(group_info, src, dst, port, msg):
    data = {}
    data['type'] = 'text'
    data['group_info'] = group_info
    data['src'] = src
    data['dst'] = dst
    data['data'] = msg
    data['time'] = time.asctime(time.localtime(time.time()))

    ip = query_state(dst)
    if ip == 'n':
        return False
    t = threading.Thread(target=send_msg_thread, args=(ip,port,data))
    t.start()
    return True


def send_file_thread(ip, port, data):
    filename = data['data']
    data['data'] = os.path.basename(filename)  # let the receiver know the basename, while I keep the whole path
    data = json.dumps(data)
    file_sender = socket(AF_INET, SOCK_STREAM)
    try:
        file_sender.connect((ip, port))
        file_sender.sendall(data.encode('utf-8'))
        print('文件发送1')
        reply = file_sender.recv(3)
        print('文件发送2')
        if reply != b'ACK':
            raise Exception("Bad Net State")
        print('文件发送3')
        with open (filename, 'rb') as f:
            while True:
                packet = f.read(1024)
                if packet == b'':
                    break
                file_sender.sendall(packet)
                print('文件发送ing'+str(packet))
        print('文件发送4')
    except Exception as e:
        print('fail to send file')
        print(e)
    finally:
        file_sender.close()
        print('文件发送完关闭线程')


def send_file(src, dst, port, filename):
    data = {}
    data['type'] = 'file'
    data['src'] = src
    data['dst'] = dst
    data['data'] = filename
    data['time'] = time.asctime(time.localtime(time.time()))
    ip = query_state(dst)
    if ip == 'n':
        return False
    t = threading.Thread(target=send_file_thread, args=(ip, port, data))
    t.start()
    return True


def send_group_file(group_info, src, dst, port, filename):
    data = {}
    data['type'] = 'file'
    data['src'] = src
    data['group_info'] = group_info
    data['dst'] = dst
    data['data'] = filename
    data['time'] = time.asctime(time.localtime(time.time()))
    ip = query_state(dst)
    if ip == 'n':
        return False
    t = threading.Thread(target=send_file_thread, args=(ip, port, data))
    t.start()
    return True


def rcv_data_thread(connectionSocket,rcv_msg):
    data = b''
    while True:
        packet = connectionSocket.recv(1024)
        data += packet
        if len(packet)<1024:
            break
    data = json.loads(data.decode('utf-8'))

    if data['type'] == 'file':
        connectionSocket.sendall(b'ACK')    # Delay!!!这样第一次只发一个data，处理好后开始发接文件
        #否则一口气发过来data和图片信息不好提出来data['type']
        filename = data['data']
        with open ('rcv_file/' + filename, 'wb') as f:
            packet = connectionSocket.recv(1024)
            while len(packet) == 1024:
                f.write(packet)
                packet = connectionSocket.recv(1024)
            f.write(packet)
        print('a new file received')
    else:
        print('a new msg received')
    rcv_msg.emit(data)

# 只是debug时用(用到时候上面的函数参数里没有信号)，最终在类里不能用，不然卡这儿了
def rcv_data(socket):
    while True:
        connectionSocket, addr = socket.accept()
        t = threading.Thread(target=rcv_data_thread, args=(connectionSocket,))
        t.start()

#为了发信号才写个类
class Chat_Receiver(QThread):
    rcv_msg = pyqtSignal(object)
    def __init__(self,port):
        super().__init__()
        self.endEvent = threading.Event()
        self.port = port

    def run(self):
        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind(('', self.port))
        self.serverSocket.listen(5)
        while not self.endEvent.is_set():
            try:
                self.serverSocket.settimeout(0.3)  #为了关线程
                connectionSocket, addr = self.serverSocket.accept()
            except timeout:
                pass
            except:
                raise
            else:
                print('hhhhhhhhhhhhhhhhhhhhhere')
                t = threading.Thread(target = rcv_data_thread, args = (connectionSocket, self.rcv_msg))
                t.start()

    def end(self):
        self.endEvent.set()


if __name__ == '__main__':
    # logout('3017011534')
    print(query_state('2017011534'))
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.bind(('', 11111))
    serverSocket.listen(5)
    # rcv_t = threading.Thread(target=rcv_data, args=(serverSocket,))
    # rcv_t.start()
    times = 1
    # test if msg is OK
    test_msg = 'Please input the msg you wanna send:'
    send_msg('2017011534', '2017011534', 11111, test_msg)
    # test if file is OK
    test_filename = 'D:\PyCharm Community Edition 2019.3\PyCharm-Projects\First_GUI\web.jpg'
    send_file('2017011534', '2017011534', 11111, test_filename)






