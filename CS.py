"""
communicate with the server
3 functions: log in, log out, query the state of other users
"""

from socket import *

HOST = '166.111.140.57'
PORT = 8000


def login(id, passport='net2019'):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))
    data = id + '_' + passport
    s.sendall(data.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    s.close()
    return data == 'lol'


def logout(id):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))
    data = 'logout' + id
    s.sendall(data.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    s.close()
    return data == 'loo'


def query_state(id):
    s = socket(AF_INET, SOCK_STREAM)
    s.connect((HOST, PORT))
    data = 'q' + id
    s.sendall(data.encode('utf-8'))
    data = s.recv(1024).decode('utf-8')
    s.close()
    return data

if __name__ == '__main__':
    myid = '4017011534'
    print(login(myid))
    print(query_state(myid))
    print(logout(myid))
    print(query_state('123'))
