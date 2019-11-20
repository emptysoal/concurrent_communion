"""
    多线程客户端测试代码
"""
from threading import Thread
from socket import *

# 创建套接字
sockfd = socket()  # 默认参数就是tcp

# 连接服务端程序
server_addr = ("127.0.0.1", 32802)
sockfd.connect(server_addr)


# 发消息函数
def send_msg():
    while True:
        try:
            msg = input(">>")
            sockfd.send(("C Tom " + msg).encode())
        except KeyboardInterrupt:
            return


# 收消息函数
def recv_msg():
    while True:
        data = sockfd.recv(1024)
        if not data:
            return
        print("GET:", data.decode())


t_send = Thread(target=send_msg)
t_recv = Thread(target=recv_msg)
t_send.start()
t_recv.start()
t_send.join()
t_recv.join()

# 关闭套接字
sockfd.close()
