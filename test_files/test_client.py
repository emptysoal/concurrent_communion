"""
    多线程客户端测试代码
"""
from threading import Thread
from socket import *
from time import sleep

# 创建套接字
sockfd = socket()  # 默认参数就是tcp

# 连接服务端程序
server_addr = ("127.0.0.1", 32802)
sockfd.connect(server_addr)

file_path = ""
file_name = ""


# 上传文件函数
def file_put(path):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(("127.0.0.1", 32803))
    file_name = path.split("/")[-1]
    sock.send(file_name.encode())
    sleep(2)
    f = open(path, "rb")
    while True:
        data = f.read(2048)
        if not data:
            sleep(2)
            sock.send(b"###")
            f.close()
            sock.close()
            break
        sock.send(data)


# 下载文件函数
def file_get():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.connect(("127.0.0.1", 32804))
    target_dir = "/home/tarena/PycharmProjects/第二阶段/elusive"
    sock.send(file_name.encode())
    f = open(("%s/%s" % (target_dir, file_name)), "wb")
    while True:
        data = sock.recv(2048)
        if data == b"$$":
            f.close()
            sock.close()
            break
        f.write(data)


# 发消息函数
def send_msg():
    while True:
        try:
            # name = input(">>")
            # global file_path
            # file_path = input("path:")
            # sockfd.send(("F %s %s" % (name, file_path)).encode())  # 文件上传请求:F name file_path
            global file_name
            file_name = input("file name:")
            sockfd.send(("L %s" % file_name).encode())  # 文件下载请求:L file_name
        except KeyboardInterrupt:
            return


# 收消息函数
def recv_msg():
    while True:
        data = sockfd.recv(1024)
        if data == b"ALLOW":
            file_put_thread = Thread(target=file_put, args=(file_path,))
            file_put_thread.start()
        if data == b"AGREE":
            file_get_thread = Thread(target=file_get)
            file_get_thread.start()
        if data == b"##":
            print(123)
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
